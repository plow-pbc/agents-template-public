#!/bin/bash
# message.sh hands the prompt a survey's < and > as typed (Swarm sends them as &lt; and &gt;) and its & as is. A stand-in
# claude prints the block it gets; no model runs.   usage: tests/welcome-message/decode.sh
set -euo pipefail
stub=$(mktemp -d)
trap 'rm -f "$stub/claude"; rmdir "$stub"' EXIT
printf '#!/bin/bash\ncat\n' >"$stub/claude" && chmod +x "$stub/claude"
got=$(PATH="$stub:$PATH" bash "$(dirname "$0")/../../templates/cos/.claude/skills/welcome-message/message.sh" <<<'{"survey": {"text": "&lt;b&gt; breaks R&D, as does &amp;nbsp;"}}' | jq -r .survey.text)
[ "$got" = "<b> breaks R&D, as does &amp;nbsp;" ] || { echo "FAIL: the prompt would read: $got" >&2; exit 1; }
echo ok
