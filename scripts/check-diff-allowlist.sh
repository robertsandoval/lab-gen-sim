#!/usr/bin/env bash
# Fail if git diff touches paths outside the codegen allow-list.
# Usage: check-diff-allowlist.sh [base-ref]
# Default base-ref: HEAD~1 (or staged changes if STAGED=1)
set -euo pipefail

BASE_REF="${1:-HEAD~1}"
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
cd "$REPO_ROOT"

ALLOWED_PATTERNS=(
  '^domain/'
  '^tests/'
  '^src/ingestion/registry\.py$'
  '^helm/values-overlay\.yaml$'
  '^scripts/seed_[a-z0-9_]+\.py$'
  '^domain-brief\.yaml$'
  '^domain-spec\.json$'
)

if [[ "${STAGED:-0}" == "1" ]]; then
  CHANGED=$(git diff --cached --name-only)
else
  CHANGED=$(git diff --name-only "$BASE_REF" HEAD 2>/dev/null || git diff --name-only)
fi

if [[ -z "$CHANGED" ]]; then
  echo "OK: no changed files"
  exit 0
fi

violations=()
while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  allowed=0
  for pat in "${ALLOWED_PATTERNS[@]}"; do
    if [[ "$file" =~ $pat ]]; then
      allowed=1
      break
    fi
  done
  if [[ "$allowed" -eq 0 ]]; then
    violations+=("$file")
  fi
done <<< "$CHANGED"

if [[ ${#violations[@]} -gt 0 ]]; then
  echo "ERROR: changes outside codegen allow-list:" >&2
  for v in "${violations[@]}"; do
    echo "  - $v" >&2
  done
  echo "Allowed: domain/, tests/, src/ingestion/registry.py, helm/values-overlay.yaml, scripts/seed_*.py" >&2
  exit 1
fi

echo "OK: all ${#CHANGED} changed file(s) within allow-list"
exit 0
