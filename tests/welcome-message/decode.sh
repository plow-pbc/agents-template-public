#!/bin/bash
# message.sh gives the prompt a survey's words as typed. Swarm hands a message's text over with < and > as &lt; and
# &gt;, and & as itself, so message.sh turns those two back and leaves & alone. A stand-in claude on PATH prints the
# block it is given; no model runs.
#   usage: tests/welcome-message/decode.sh
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
stub=$(mktemp -d)
trap 'rm -f "$stub/claude"; rmdir "$stub"' EXIT
printf '#!/bin/bash\ncat\n' >"$stub/claude"
chmod +x "$stub/claude"
block=$(PATH="$stub:$PATH" bash "$here/../../templates/cos/.claude/skills/welcome-message/message.sh" <<'EOF'
{"survey": {"slowdowns": {"selected": [], "text": "&lt;b&gt; tags break R&D's export, and so does &amp;nbsp;"}}, "available_now": {}}
EOF
)
want="<b> tags break R&D's export, and so does &amp;nbsp;"
got=$(jq -r .survey.slowdowns.text <<<"$block")
[ "$got" = "$want" ] || { printf 'FAIL: the prompt would read %s\n  instead of %s\n' "$got" "$want" >&2; exit 1; }
echo ok
