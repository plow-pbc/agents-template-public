# agents-template-public

Owner-neutral role templates for a [kitchen](https://github.com/srosro/kitchen)
of Claude Code agents: an engineering sous and a chief of staff sous that run
on their owner's machine and talk to people in Swarm.

Each agent is a folder, `templates/eng/`, `templates/cos/` or `templates/base-agent/` (an
agent the owner adds later, with a one-line job), holding what
install.sh puts in that agent's folder: its `CLAUDE.md`, with these
placeholders filled in, and its skills in `.claude/skills/`, copied as they are:

| Placeholder | Value |
|---|---|
| `{{OWNER}}` | the owner's name |
| `{{EMAIL}}` | the owner's email address |
| `{{OWNER_ID}}` | the owner's Swarm user id, `@id:server` |
| `{{COMPANY}}` | the company's name |
| `{{ROOM}}` | the room the engineering sous answers in, `#room:server` |
| `{{ACCOUNT}}` | the sous's own Swarm account, `@name:server` |
| `{{AGENT_NAME}}` | the agent's own first name |
| `{{JOB}}` | an added agent's one-line job (`base-agent/` only) |

Anyone in the company can direct an agent's actions inside the company: the
agent looks up the sender's id in the `directory` tool and acts only for kind
`person`, or for the owner's own agents (kind `agent` with `owner` exactly
`{{OWNER_ID}}`, the server's record). Guests, other people's agents and
outsiders are information only. Money,
anything sent outside the company, credentials and the other limits in
each agent's `CLAUDE.md` stay the owner's. See `templates/README.md` for details.

MIT licensed.
