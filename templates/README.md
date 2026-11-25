# Role templates

Each agent has its own folder here, holding what install.sh puts in that agent's folder on the owner's machine:

| Agent | Folder |
|---|---|
| Engineering | `eng/` |
| Chief of staff | `cos/` |

- `CLAUDE.md` is the agent's instructions. install.sh fills its placeholders (below) and writes it as the agent's
  `CLAUDE.md`. A rerun keeps a `CLAUDE.md` it wrote before. The rules every agent shares come first in each file, from
  "# Base instructions (every agent)" to the agent's own heading, so a change to them is made in every agent's file.
- `.claude/skills/` holds the agent's skills, copied as they are on every install run (no placeholders filled). Today
  that's `latch`: the agent uses Plow Latch for the owner's mail, calendar, texts, contacts, files on their Macs and a
  real browser, and tells the owner how to set it up when it isn't. The chief of staff also has `welcome-message`:
  its answer to the owner's welcome survey, written by `prompt.md` from the owner's answers.

Placeholders install.sh fills in `CLAUDE.md`, in these exact formats:

- `{{OWNER}}`: the owner's name, as plain text
- `{{EMAIL}}`: the owner's email address
- `{{OWNER_ID}}`: the owner's Swarm user id, `@id:server`, from the `owner`
  field of `swarm accounts add`'s JSON
- `{{COMPANY}}`: the company's name
- `{{ROOM}}`: the room the sous answers in, `#room:server`
- `{{ACCOUNT}}`: the sous's own Swarm account, `@name:server`
- `{{FIRST_RUN}}`: `survey` when the workspace's Plow has the welcome survey, else `question` (`cos/`
  only). Any other value, an unfilled placeholder included, runs the `question` first run
- `{{AGENT_NAME}}`: the agent's own first name

These are owner-neutral starting points for a customer's machine. The
operator's own roles live in the folders beside this one.
