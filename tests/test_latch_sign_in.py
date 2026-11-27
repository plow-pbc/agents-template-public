"""python3 -m unittest discover tests (from the repo root): each agent's latch sign-in script, run on a fake latch."""
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
AGENTS = ["cos", "eng", "base-agent"]

# A latch that logs each call, one line of arguments, and answers as the test sets it up: `app` opens or fails,
# `status --local` says logged in from its Nth call on (never with LOGIN_AFTER unset), `login --events` prints
# the lines of a login by text.
LATCH = r"""#!/bin/sh
echo "$*" >>"$FAKE/calls"
case $1 in
	app)
		[ "$APP" = opens ] || { echo '{"error":{"code":"app_broken"}}' >&2; exit 5; }
		echo '{"app":"/Applications/Plow Latch.app"}' ;;
	status)
		n=$(($(cat "$FAKE/status" 2>/dev/null || echo 0) + 1)); echo "$n" >"$FAKE/status"
		if [ -n "${LOGIN_AFTER:-}" ] && [ "$n" -ge "$LOGIN_AFTER" ]; then
			echo '{"login":{"kind":"device"},"this_machine":{"name":"studio"}}'
		else
			echo '{"login":null,"this_machine":{"name":null}}'
		fi ;;
	login)
		echo '{"type":"hello","schema":1}'
		echo '{"type":"code","code":"FAKE1","send_to":"+15550000001","send_to_display":"+1 555-000-0001"}'
		echo '{"type":"waiting"}'
		echo '{"type":"verified","peer":{"name":"studio"}}' ;;
esac
"""
SW_VERS = r"""#!/bin/sh
[ -n "${MACOS:-}" ] || exit 1
echo "$MACOS"
"""
SLEEP = "#!/bin/sh\n"


class SignIn(unittest.TestCase):
    def setUp(self):
        self.fake = Path(tempfile.mkdtemp())
        for name, body in [("latch", LATCH), ("sw_vers", SW_VERS), ("sleep", SLEEP)]:
            path = self.fake / name
            path.write_text(body)
            path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def tearDown(self):
        for path in self.fake.iterdir():
            path.unlink()
        self.fake.rmdir()

    def run_sign_in(self, agent="cos", **env):
        script = TEMPLATES / agent / ".claude" / "skills" / "latch" / "sign-in"
        env = {"PATH": f"{self.fake}:/usr/bin:/bin", "FAKE": str(self.fake), "APP": "fails", **env}
        r = subprocess.run(["/bin/sh", str(script)], capture_output=True, text=True, env=env, timeout=120)
        calls = (self.fake / "calls").read_text().splitlines() if (self.fake / "calls").exists() else []
        return r.returncode, r.stdout.splitlines(), calls

    def test_the_app_opens_and_the_login_is_waited_for(self):
        for agent in AGENTS:
            with self.subTest(agent=agent):
                (self.fake / "calls").unlink(missing_ok=True)
                (self.fake / "status").unlink(missing_ok=True)
                code, out, calls = self.run_sign_in(agent, MACOS="26.1", APP="opens", LOGIN_AFTER="3")
                self.assertEqual(code, 0)
                self.assertEqual(out, ['{"type":"app"}', '{"type":"verified"}'])
                self.assertEqual(calls, ["app", "status --local", "status --local", "status --local"])

    def test_no_code_is_asked_for_while_the_app_shows_its_own(self):
        code, out, calls = self.run_sign_in(MACOS="26.0", APP="opens")
        self.assertEqual(code, 1)
        self.assertEqual(out, ['{"type":"app"}', '{"type":"expired"}'])
        self.assertEqual(calls[0], "app")
        self.assertEqual(set(calls[1:]), {"status --local"})
        self.assertEqual(len(calls) - 1, 900)  # every 2 seconds for 30 minutes, as long as a login code lasts

    def test_a_code_to_text_where_the_app_cannot_open(self):
        # Before macOS 26 the app only says so and quits; "" is not a Mac.
        text = ["login --events"]
        for macos, app, expected in [("26.1", "fails", ["app"] + text), ("15.7", "opens", text),
                                     ("13.0", "opens", text), ("", "opens", text)]:
            with self.subTest(macos=macos, app=app):
                (self.fake / "calls").unlink(missing_ok=True)
                code, out, calls = self.run_sign_in(MACOS=macos, APP=app)
                self.assertEqual(code, 0)
                self.assertEqual(calls, expected)
                self.assertIn('"type":"code"', out[1])
                self.assertEqual(out[-1], '{"type":"verified","peer":{"name":"studio"}}')

    def test_every_agent_has_the_same_script(self):
        scripts = {(TEMPLATES / a / ".claude" / "skills" / "latch" / "sign-in").read_bytes() for a in AGENTS}
        self.assertEqual(len(scripts), 1)


if __name__ == "__main__":
    unittest.main()
