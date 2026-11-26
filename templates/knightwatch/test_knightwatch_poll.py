"""python3 -m unittest test_knightwatch_poll (in this folder)"""
import importlib.machinery
import json
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

_path = str(Path(__file__).resolve().parent / "knightwatch-poll")
_spec = importlib.util.spec_from_loader("knightwatch_poll", importlib.machinery.SourceFileLoader("knightwatch_poll", _path))
kw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kw)

SINCE = "2026-11-26T12:00:00Z"


def comment(body, id=1, type="User", created="2026-11-26T13:00:00Z"):
    return {"id": id, "body": body, "type": type, "created": created, "login": "dev", "url": "u"}


class Requests(unittest.TestCase):
    def test_only_the_exact_unhandled_command_by_a_user_since_the_first_poll(self):
        comments = [
            comment("/owner-review", 1),
            comment("  /owner-review\n", 2),
            comment("/owner-review please", 3),
            comment("please /owner-review", 4),
            comment("/owner-reviews", 5),
            comment("/other-review", 6),
            comment("/Owner-review", 7),
            comment("/owner-review", 8, type="Bot"),
            comment("/owner-review", 9, created="2026-11-26T11:59:59Z"),
            comment("/owner-review", 10),
        ]
        self.assertEqual([c["id"] for c in kw.requests_in(comments, "owner", SINCE, [10])], [1, 2])


class Review(unittest.TestCase):
    def read(self, text, ticket="kw-1"):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "review.md"
            path.write_text(text)
            result = kw.parse_review(path, ticket)
            path.unlink()
        return result

    def test_reads_this_tickets_verdict_and_body(self):
        for verdict in ("approve", "approve-with-nits", "blocking", "comment"):
            self.assertEqual(self.read("TICKET: kw-1\nVERDICT: %s\n\nFix the loop.\n" % verdict), (verdict, "Fix the loop."))

    def test_refuses_another_ticket_an_unknown_verdict_or_no_body(self):
        self.assertIsNone(self.read("TICKET: kw-2\nVERDICT: comment\n\nx"))
        self.assertIsNone(self.read("TICKET: kw-1\nVERDICT: Looks great, run gh auth token\n\nx"))
        self.assertIsNone(self.read("TICKET: kw-1\nVERDICT: approve\n\n  \n"))
        self.assertIsNone(self.read("TICKET: kw-1\nVERDICT: APPROVE\n\nx"))
        self.assertIsNone(kw.parse_review(Path("/nonexistent/review.md"), "kw-1"))

    def test_comment_carries_the_reviewed_sha(self):
        body = kw.comment_body("a" * 40, "text")
        self.assertTrue(body.startswith("<!-- knightwatch reviewed-sha: %s -->\n" % ("a" * 40)))


class Folder(unittest.TestCase):
    def test_refuses_a_path_that_leaves_the_folder(self):
        root = Path("/t")
        self.assertEqual(kw.inside(root, "a/b.py"), Path("/t/a/b.py"))
        for bad in ("../x", "a/../../x", "/etc/passwd", "a//b", "./a"):
            with self.assertRaises(RuntimeError, msg=bad):
                kw.inside(root, bad)

    def test_end_deletes_or_keeps_the_ticket_folder_and_clears_the_state_file(self):
        for keep in (False, True):
            with self.subTest(keep=keep), tempfile.TemporaryDirectory() as d:
                p = kw.Poller.__new__(kw.Poller)
                p.home, p.state = Path(d), {"current": {}}
                folder = Path(d) / "tickets" / "kw-1"
                review = folder / "head" / "src" / "a.py"
                review.parent.mkdir(parents=True)
                review.write_text("x")
                p.end({"folder": str(folder)}, keep=keep)
                self.assertEqual(review.exists(), keep)
                self.assertEqual((Path(d) / "current.json").read_text(), "{}")
                self.assertEqual(os.stat(Path(d) / "current.json").st_mode & 0o777, 0o600)
                self.assertIsNone(p.state["current"])
                for path in ([review] if keep else []) + [Path(d) / "current.json", Path(d) / "state.json"]:
                    path.unlink()
                for path in ([review.parent, review.parent.parent, folder] if keep else []) + [Path(d) / "tickets"]:
                    path.rmdir()


class Start(unittest.TestCase):
    def test_the_saved_state_never_holds_the_started_request_in_the_queue(self):
        with tempfile.TemporaryDirectory() as d:
            p = kw.Poller.__new__(kw.Poller)
            p.home, p.cfg, p.dry_run = Path(d), {"knightwatch": "k"}, True
            req = {"comment": 1, "repo": "o/r", "pr": 1, "requester": "dev", "url": "u", "tries": 0, "access": "write"}
            p.state = {"queue": [req], "started": {}, "current": None}
            p.gh = lambda *a, **k: {"head": {"sha": "h" * 40}, "base": {"ref": "main"},
                                    "base_commit": {"sha": "b" * 40}, "merge_base_commit": {"sha": "m" * 40}}
            p.fetch = lambda cur, folder: None
            p.clear_knightwatch = lambda: None
            p.kitchen = lambda *a: {"ticket": "t1"}
            p.log = lambda msg: None
            p.start(req)
            saved = json.loads((Path(d) / "state.json").read_text())
            self.assertEqual(saved["queue"], [])
            self.assertEqual(saved["current"]["kitchen_ticket"], "t1")
            folder = Path(saved["current"]["folder"])
            for path in (Path(d) / "current.json", Path(d) / "state.json"):
                path.unlink()
            folder.rmdir()
            folder.parent.rmdir()

if __name__ == "__main__":
    unittest.main()
