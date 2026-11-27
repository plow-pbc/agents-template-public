# Role templates

Each agent has its own folder here, holding what install.sh puts in that agent's folder on the owner's machine:

| Agent | Folder |
|---|---|
| Engineering | `eng/` |
| Chief of staff | `cos/` |
| An agent the owner added later, with a one-line job | `base-agent/` |

- `CLAUDE.md` is the agent's instructions. install.sh fills its placeholders (below) and writes it as the agent's
  `CLAUDE.md`. A rerun keeps a `CLAUDE.md` it wrote before. The rules every agent shares come first in each file, from
  "# Base instructions (every agent)" to the agent's own heading, so a change to them is made in every agent's file.
- `first-turn.md`, where an agent has one, is what it is told once: install.sh fills its placeholders as in
  `CLAUDE.md` and sends it in the agent's first turn, when the agent is created. Onboarding goes there, never in
  `CLAUDE.md`, which the agent reads every turn.
- `.claude/skills/` holds the agent's skills, copied as they are on every install run (no placeholders filled). Today
  that's `latch`: the agent uses Plow Latch for the owner's mail, calendar, texts, contacts, files on their Macs and a
  real browser, and tells the owner how to set it up when it isn't.

Placeholders install.sh fills in `CLAUDE.md`, in these exact formats:

- `{{OWNER}}`: the owner's name, as plain text
- `{{EMAIL}}`: the owner's email address
- `{{OWNER_ID}}`: the owner's Swarm user id, `@id:server`, from the `owner`
  field of `swarm accounts add`'s JSON; for an added agent, the owner the server
  recorded for its account
- `{{COMPANY}}`: the company's name
- `{{ROOM}}`: the room the sous answers in, `#room:server`
- `{{ACCOUNT}}`: the sous's own Swarm account, `@name:server`
- `{{AGENT_NAME}}`: the agent's own first name
- `{{JOB}}`: an added agent's job, the one line its owner gave it: plain words
  and punctuation, no markdown (`base-agent/` only)

`knightwatch/knightwatch-poll.plist` is the poller's LaunchAgent: `knightwatch-poll enable` fills its placeholders,
not install.sh.

These are owner-neutral starting points for a customer's machine. The
operator's own roles live in the folders beside this one.
