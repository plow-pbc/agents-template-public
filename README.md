# kitchen-agents-public

Owner-neutral role templates for a [kitchen](https://github.com/srosro/kitchen)
of Claude Code agents: an engineering sous and a chief of staff sous that run
on their owner's machine and talk to people in Swarm.

Each agent's `CLAUDE.md` is `templates/base.md` followed by its role file
(`templates/eng.md` or `templates/cos.md`), joined into one file, with these
placeholders filled in:

| Placeholder | Value |
|---|---|
| `{{OWNER}}` | the owner's name |
| `{{EMAIL}}` | the owner's email address |
| `{{OWNER_ID}}` | the owner's Swarm user id, `@id:server` |
| `{{COMPANY}}` | the company's name |
| `{{ROOM}}` | the room the engineering sous answers in, `#room:server` |
| `{{ACCOUNT}}` | the sous's own Swarm account, `@name:server` |

Anyone in the company can direct an agent's actions inside the company: the
agent looks up the sender's id in the `directory` tool and acts only for kind
`person`. Guests, other agents and outsiders are information only. Money,
anything sent outside the company, credentials and the other limits in
`templates/base.md` stay the owner's. See `templates/README.md` for details.

MIT licensed.
