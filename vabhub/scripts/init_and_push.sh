#!/usr/bin/env bash
set -euo pipefail

ORG="strmforge"
REPO="vabhub"
DEFAULT_BRANCH="main"

git init
git checkout -b "$DEFAULT_BRANCH" || true
git add .
git -c user.name="github-actions[bot]" -c user.email="41898282+github-actions[bot]@users.noreply.github.com" commit -m "chore: init vabhub portal"

git remote add origin "git@github.com:${ORG}/${REPO}.git" || git remote set-url origin "git@github.com:${ORG}/${REPO}.git"
git push -u origin "$DEFAULT_BRANCH"

echo "Done. Go to: https://github.com/${ORG}/${REPO}"