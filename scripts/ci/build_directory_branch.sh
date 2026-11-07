#!/bin/sh
# Commit a copy of HEAD with only the file types Anthropic's directory accepts
# from unverified organizations (Markdown, text, JSON, YAML, images), and print its id.
# The skill works without its scripts folder. Example: sh scripts/ci/build_directory_branch.sh
set -eu
index=$(mktemp)
trap 'rm -f "$index"' EXIT
rm -f "$index"
git ls-tree -r HEAD -- LICENSE README.md .claude-plugin skills |
  grep -E '	(LICENSE|.*\.(md|txt|json|ya?ml|png))$' |
  GIT_INDEX_FILE=$index git update-index --index-info
tree=$(GIT_INDEX_FILE=$index git write-tree)
git commit-tree "$tree" -m "Directory build of $(git rev-parse --short HEAD)"
