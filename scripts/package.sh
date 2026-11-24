#!/usr/bin/env bash
# Zip skills for upload to claude.ai / Claude Desktop (Settings > Capabilities).
# Each zip contains a top-level <name>/ folder holding SKILL.md and its files.
#
# Usage: scripts/package.sh [name...]   (default: all skills)
# Output: dist/<name>.zip

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_dir="$repo_root/skills"
dist="$repo_root/dist"

if command -v zip >/dev/null; then
  make_zip() { (cd "$skills_dir" && zip -qr "$1" "$2" -x '*/.DS_Store' '*/.gitkeep' '*/__pycache__/*'); }
elif command -v python3 >/dev/null; then
  make_zip() { (cd "$skills_dir" && python3 -I -m zipfile -c "$1" "$2"); }
else
  echo "zip or python3 is required" >&2; exit 1
fi

names=("$@")
if ((${#names[@]} == 0)); then
  for d in "$skills_dir"/*/; do
    [[ -d "$d" ]] && names+=("$(basename "$d")")
  done
fi
if ((${#names[@]} == 0)); then
  echo "no skills to package in $skills_dir"
  exit 0
fi

"$repo_root/scripts/check.sh" "${names[@]}"
echo

mkdir -p "$dist"
for name in "${names[@]}"; do
  out="$dist/$name.zip"
  rm -f "$out"
  make_zip "$out" "$name"
  echo "wrote ${out#"$repo_root"/}"
done
