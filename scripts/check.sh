#!/usr/bin/env bash
# Validate every skill (or the named ones) against the Agent Skills spec
# (https://agentskills.io/specification) plus this repo's conventions.
#
# Usage: scripts/check.sh [--skills-dir DIR] [name...]
# Exit status is non-zero if any skill has an error. Warnings don't fail.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_dir="$repo_root/skills"
names=()

while (($#)); do
  case "$1" in
    --skills-dir) skills_dir="$2"; shift 2 ;;
    -h|--help) sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) names+=("$1"); shift ;;
  esac
done

if ((${#names[@]} == 0)); then
  for d in "$skills_dir"/*/; do
    [[ -d "$d" ]] && names+=("$(basename "$d")")
  done
fi

if ((${#names[@]} == 0)); then
  echo "no skills found in $skills_dir"
  exit 0
fi

errors=0
warnings=0
err()  { echo "  error: $*"; errors=$((errors + 1)); }
warn() { echo "  warn:  $*"; warnings=$((warnings + 1)); }

# Print the value of a top-level frontmatter key. Handles plain, quoted, and
# block-scalar (| or >) values; block lines are joined with spaces.
frontmatter_value() {
  local key="$1" file="$2"
  awk -v key="$key" '
    NR == 1 { if ($0 != "---") exit; next }
    $0 == "---" { exit }
    in_block {
      if ($0 ~ /^[ \t]/ || $0 == "") { sub(/^[ \t]+/, ""); val = val (val == "" ? "" : " ") $0; next }
      in_block = 0
    }
    $0 ~ "^" key ":" {
      v = $0; sub("^" key ":[ \t]*", "", v)
      if (v ~ /^[|>][-+]?$/) { in_block = 1; val = ""; found = 1; next }
      if (v ~ /^".*"$/ || v ~ /^\047.*\047$/) v = substr(v, 2, length(v) - 2)
      val = v; found = 1
    }
    END { if (found) { sub(/[ \t]+$/, "", val); print val } }
  ' "$file"
}

for name in "${names[@]}"; do
  dir="$skills_dir/$name"
  file="$dir/SKILL.md"
  echo "$name"

  if [[ ! -d "$dir" ]]; then err "no such skill directory: $dir"; continue; fi
  if [[ ! -f "$file" ]]; then err "missing SKILL.md"; continue; fi
  if [[ "$(head -n1 "$file")" != "---" ]]; then err "SKILL.md must start with '---' frontmatter"; continue; fi
  if [[ "$(awk 'NR > 1 && $0 == "---" { print "y"; exit }' "$file")" != "y" ]]; then
    err "frontmatter is not closed with '---'"; continue
  fi

  fm_name="$(frontmatter_value name "$file")"
  if [[ -z "$fm_name" ]]; then
    err "frontmatter 'name' is missing or empty"
  else
    [[ "$fm_name" == "$name" ]] || err "name '$fm_name' does not match directory '$name'"
    ((${#fm_name} <= 64)) || err "name is ${#fm_name} chars (max 64)"
    [[ "$fm_name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] \
      || err "name must be lowercase a-z, 0-9 and single hyphens, not starting or ending with '-'"
  fi

  desc="$(frontmatter_value description "$file")"
  if [[ -z "$desc" ]]; then
    err "frontmatter 'description' is missing or empty"
  elif ((${#desc} > 1024)); then
    err "description is ${#desc} chars (max 1024)"
  fi

  lines="$(wc -l < "$file")"
  ((lines <= 500)) || warn "SKILL.md is $lines lines; consider moving detail into references/"

  # Relative links in SKILL.md must resolve inside the skill directory.
  while IFS= read -r target; do
    target="${target%%#*}"
    [[ -z "$target" ]] && continue
    [[ -e "$dir/$target" ]] || err "broken link: $target"
  done < <(grep -oE '\]\([^)[:space:]]+\)' "$file" | sed -E 's/^\]\((.*)\)$/\1/' \
            | grep -vE '^([a-zA-Z][a-zA-Z0-9+.-]*:|#|/)' || true)
done

echo
echo "$errors error(s), $warnings warning(s)"
((errors == 0))
