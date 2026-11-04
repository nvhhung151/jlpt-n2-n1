#!/usr/bin/env bash
# Commit + push progress of the cloud/ part. Packs that still have validate ERRORs (e.g. an agent is mid-fix)
# are left out of the commit and picked up by a later run. Usage: bash cloud/push.sh "message"
set -e
cd "$(dirname "$0")/.."
git pull -q --no-rebase origin main
python3 -I cloud/validate.py --all --json > /tmp/jlpt_validate.json 2>/dev/null || true
bad=$(python3 -I -c "
import json
d=json.load(open('/tmp/jlpt_validate.json',encoding='utf-8'))
print('\n'.join(sorted({'n2-n1-handoff/'+p['file'] for p in d if p['severity']=='ERROR' and p['file']})))")
git add n2-n1-handoff cloud TIEN-DO.md
if [ -n "$bad" ]; then
  echo "Bỏ qua (còn ERROR):"; echo "$bad"
  echo "$bad" | xargs -r git reset -q --
fi
if git diff --cached --quiet; then echo "nothing to commit"; exit 0; fi
total=$(python3 -I cloud/status.py | tail -1)
git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "$1 ($total)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01RY1veSQW6x6hKC4ogAsdF8"
git push -q origin HEAD:main
git log --oneline -1
