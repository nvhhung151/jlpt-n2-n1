#!/usr/bin/env bash
# Validate, commit and push progress of the cloud/ part. Usage: bash cloud/push.sh "message"
set -e
cd "$(dirname "$0")/.."
python3 -I cloud/validate.py --all --quiet || { echo "VALIDATE FAILED - not pushing"; exit 1; }
git pull -q --no-rebase origin main
git add n2-n1-handoff cloud TIEN-DO.md
if git diff --cached --quiet; then echo "nothing to commit"; exit 0; fi
total=$(python3 -I cloud/status.py | tail -1)
git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "$1 ($total)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01RY1veSQW6x6hKC4ogAsdF8"
git push -q origin HEAD:main
git log --oneline -1
