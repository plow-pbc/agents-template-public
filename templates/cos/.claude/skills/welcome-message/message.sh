#!/bin/bash
# The message answering a welcome survey: prompt.md, beside this file, with NAME (this agent's own first name) for its
# {{AGENT_NAME}}, run on the JSON block on stdin, and printed. Claude runs it on the model this agent runs on, with none
# of this agent's instructions, skills, hooks, MCP servers or tools (--safe-mode, no tools): the survey's answers reach a
# model that can only write.
#   usage: message.sh NAME <block.json
set -euo pipefail
name=$1
prompt=$(cat "$(dirname "$0")/prompt.md")
questions=("Where should we get started?" "What do you want to tackle first?" "What can we get started on?" "Where can we get started?")
block=$(jq -c --arg q "${questions[RANDOM % ${#questions[@]}]}" '.closing_question //= $q')
claude -p --safe-mode --tools "" --no-session-persistence --system-prompt "${prompt//\{\{AGENT_NAME\}\}/"$name"}" <<<"$block"
