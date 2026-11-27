"""python3 -m unittest test_kw_allow (in this folder): runs .claude/hooks/kw-allow on PreToolUse events."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent / ".claude" / "hooks" / "kw-allow"


class Hook(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "home"
        agent = self.tmp / "agent" / ".claude" / "hooks"
        agent.mkdir(parents=True)
        shutil.copy(HOOK, agent / "kw-allow")
        (agent.parent / "knightwatch.json").write_text(json.dumps({"company": "acme"}))
        self.hook = agent / "kw-allow"
        self.state = self.home / ".local/share/knightwatch/acme"
        self.folder = self.state / "tickets" / "kw-1"
        (self.folder / "base").mkdir(parents=True)
        (self.folder / "base" / "app.py").write_text("x = 1\n")
        (self.state / "tickets" / "kw-0").mkdir()
        (self.state / "tickets" / "kw-0" / "review.md").write_text("earlier\n")
        (self.tmp / "secret").write_text("token\n")
        os.symlink(self.tmp / "secret", self.folder / "base" / "link")
        self.current({"ticket": "kw-1", "folder": str(self.folder)})

    def tearDown(self):
        for root, dirs, files in os.walk(str(self.tmp), topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                path = os.path.join(root, name)
                os.remove(path) if os.path.islink(path) else os.rmdir(path)
        self.tmp.rmdir()

    def current(self, cur):
        (self.state / "current.json").write_text(json.dumps(cur))

    def decide(self, tool, args, sub=False):
        event = {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": args, "cwd": str(self.tmp / "agent")}
        if sub:
            event.update(agent_id="a1", agent_type="kw-specialist")
        r = subprocess.run(["/usr/bin/python3", str(self.hook)], input=json.dumps(event), capture_output=True, text=True,
                           env={"HOME": str(self.home), "PATH": "/usr/bin:/bin"})
        if r.returncode:
            return "error"
        return json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"]

    def test_read_only_inside_the_current_ticket(self):
        self.assertEqual(self.decide("Read", {"file_path": str(self.folder / "base/app.py")}), "allow")
        self.assertEqual(self.decide("Read", {"file_path": str(self.tmp / "secret")}), "deny")
        self.assertEqual(self.decide("Read", {"file_path": str(self.folder / "base/link")}), "deny")
        self.assertEqual(self.decide("Read", {"file_path": str(self.folder / "../kw-0/review.md")}), "deny")
        self.assertEqual(self.decide("Read", {"file_path": str(self.state / "tickets/kw-0/review.md")}), "deny")
        self.assertEqual(self.decide("Read", {"file_path": str(self.state / "current.json")}), "deny")

    def test_grep_and_glob_need_a_path_in_the_folder(self):
        self.assertEqual(self.decide("Grep", {"pattern": "x", "path": str(self.folder)}), "allow")
        self.assertEqual(self.decide("Grep", {"pattern": "x"}), "deny")
        self.assertEqual(self.decide("Grep", {"pattern": "x", "path": str(self.folder), "glob": "../../*"}), "deny")
        self.assertEqual(self.decide("Glob", {"pattern": "**/*.py", "path": str(self.folder)}), "allow")
        self.assertEqual(self.decide("Glob", {"pattern": "/etc/*", "path": str(self.folder)}), "deny")
        self.assertEqual(self.decide("Glob", {"pattern": "*", "path": str(self.state / "tickets")}), "deny")

    def test_write_only_the_review_and_notes(self):
        self.assertEqual(self.decide("Write", {"file_path": str(self.folder / "review.md")}), "allow")
        self.assertEqual(self.decide("Write", {"file_path": str(self.folder / "notes/security.md")}, sub=True), "allow")
        self.assertEqual(self.decide("Write", {"file_path": str(self.folder / "notes/a/b.md")}), "deny")
        self.assertEqual(self.decide("Write", {"file_path": str(self.folder / "base/app.py")}), "deny")
        self.assertEqual(self.decide("Write", {"file_path": str(self.tmp / "agent/.claude/settings.json")}), "deny")

    def test_skill_and_agent(self):
        self.assertEqual(self.decide("Skill", {"skill": "knightwatch-review"}), "allow")
        self.assertEqual(self.decide("Skill", {"skill": "other"}), "deny")
        self.assertEqual(self.decide("Agent", {"subagent_type": "kw-specialist", "prompt": "p"}), "allow")
        self.assertEqual(self.decide("Agent", {"subagent_type": "kw-critic", "prompt": "p"}), "allow")
        self.assertEqual(self.decide("Agent", {"subagent_type": "general-purpose", "prompt": "p"}), "deny")
        self.assertEqual(self.decide("Agent", {"subagent_type": "kw-specialist", "isolation": "worktree"}), "deny")
        self.assertEqual(self.decide("Agent", {"subagent_type": "kw-specialist", "run_in_background": True}), "deny")
        self.assertEqual(self.decide("Agent", {"subagent_type": "kw-specialist"}, sub=True), "deny")
        self.assertEqual(self.decide("Skill", {"skill": "knightwatch-review"}, sub=True), "deny")

    def test_everything_else_is_denied(self):
        for tool, args in (("Bash", {"command": "gh auth token"}), ("WebFetch", {"url": "https://x"}),
                           ("mcp__swarm__send", {}), ("Edit", {"file_path": str(self.folder / "review.md")}),
                           ("TodoWrite", {})):
            self.assertEqual(self.decide(tool, args), "deny", tool)

    def test_no_review_running_denies_all(self):
        self.current({})
        self.assertEqual(self.decide("Read", {"file_path": str(self.folder / "base/app.py")}), "deny")
        self.current({"ticket": "kw-1", "folder": str(self.tmp)})
        self.assertEqual(self.decide("Read", {"file_path": str(self.tmp / "secret")}), "deny")
