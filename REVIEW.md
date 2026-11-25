# Review instructions — agents-template-public

## Cause-first bug fixes

Fix at the cause; never with a workaround that leaves the cause in place. A guard or check at the boundary where the cause lives is a cause-level fix. If a fix adds a maintained path or net complexity, explain why removing the cause directly is insufficient. No stopgaps: they promote brittle, confusing, unreliable code. Ship the fix at the cause. Required rollout sequencing (staged removals, compatibility windows) and authorized incident containment, labeled with when it's removed, are not stopgaps. When the bug comes from a duplicated source or identity, remove the duplicate rather than bridging the two. Limits a REVIEW.md already records as accepted stay out of review unless the diff widens them.

Repo-specific reviewer policy. The universal review policy is prepended by the reviewer and is not restated here.

## What this repo is

Public, owner-neutral role templates for a kitchen of Claude Code agents: each agent's folder under `templates/` holds its `CLAUDE.md` (instructions with `{{PLACEHOLDER}}` fields an installer fills) and the skills copied beside it. The product is prose an agent follows, so a rule is the unit of code.

**Stage:** early, installed on a handful of customer machines.

## Review priority

**#1: low complexity.** Pre-PMF, a short set of clear rules that meets the need beats a complete one. Weigh every finding against this first.

- **Cut scope creep.** Flag a change that grows past its stated ask, or a rule added for a case nobody has hit. The remedy is a smaller change, not more text.
- **DRY.** Flag a second statement of a rule or fact that already has an owner in the same file. The remedy is to reuse that owner or delete the copy.
- **Few exceptions.** Each new special case, carve-out or "unless" is a finding unless it handles a failure that actually happens. Limits on money, credentials and what leaves the company are not special cases.
- **Model decision over regex.** Judging the meaning of a message belongs to the agent's own judgment, never a keyword list or pattern the agent must match. Exact formats an installer or tool parses (a placeholder, an id shape) stay exact and are not findings.

Prefer subtractive remedies (delete, collapse, reuse) over additive ones at any severity.

## Accepted limits

- The shared "Base instructions (every agent)" block is copied into each agent's `CLAUDE.md` on purpose, so each file installs alone. The copies are not a DRY finding; a change that makes them differ is.

## Where the real risks are

- **Public repo.** Flag any name, email, id, room, host, customer or internal detail of a real person or company. Owner specifics belong in placeholders.
- **Placeholders.** A placeholder used in a template but not listed in `templates/README.md`, or listed in a different format, breaks installs.
- **Authority rules.** A change that widens who can direct an agent, or what it may do without its owner (money, sending outside the company, credentials), is High however small the edit.
