#!/usr/bin/env bash
# Symlink each skill in skills/ into one or more agent skill directories.
#
# Usage: scripts/install.sh [--target DIR]... [--dry-run] [--uninstall] [--force] [name...]
#   --target DIR  install into DIR (repeatable; default: ~/.claude/skills)
#   --dry-run     print what would happen without changing anything
#   --uninstall   remove links in the targets that point into this repo
#   --force       replace an existing file, directory or foreign link
#   name...       only these skills (default: all)

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_dir="$repo_root/skills"
targets=()
names=()
dry_run=0
uninstall=0
force=0

while (($#)); do
  case "$1" in
    --target) targets+=("$2"); shift 2 ;;
    --dry-run) dry_run=1; shift ;;
    --uninstall) uninstall=1; shift ;;
    --force) force=1; shift ;;
    -h|--help) sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) names+=("$1"); shift ;;
  esac
done

((${#targets[@]})) || targets=("$HOME/.claude/skills")

run() {
  if ((dry_run)); then echo "    would run: $*"; else "$@"; fi
}

if ((uninstall)); then
  for target in "${targets[@]}"; do
    echo "$target"
    [[ -d "$target" ]] || { echo "  (does not exist)"; continue; }
    for link in "$target"/*; do
      [[ -L "$link" ]] || continue
      dest="$(readlink "$link")"
      [[ "$dest" == "$skills_dir/"* ]] || continue
      name="$(basename "$link")"
      if ((${#names[@]})) && [[ ! " ${names[*]} " == *" $name "* ]]; then continue; fi
      echo "  remove $name"
      run rm "$link"
    done
  done
  exit 0
fi

if ((${#names[@]} == 0)); then
  for d in "$skills_dir"/*/; do
    [[ -d "$d" ]] && names+=("$(basename "$d")")
  done
fi

if ((${#names[@]} == 0)); then
  echo "no skills to install in $skills_dir"
  exit 0
fi

status=0
for target in "${targets[@]}"; do
  echo "$target"
  if [[ ! -d "$target" ]]; then
    echo "  create directory"
    run mkdir -p "$target"
  fi
  for name in "${names[@]}"; do
    src="$skills_dir/$name"
    dest="$target/$name"
    if [[ ! -f "$src/SKILL.md" ]]; then
      echo "  skip $name: no SKILL.md in $src"; status=1; continue
    fi
    if [[ -L "$dest" && "$(readlink "$dest")" == "$src" ]]; then
      echo "  ok   $name"
      continue
    fi
    if [[ -e "$dest" || -L "$dest" ]]; then
      if ((force)); then
        echo "  replace $name (was: $( [[ -L "$dest" ]] && readlink "$dest" || echo 'real file/dir'))"
        run rm -rf "$dest"
      else
        echo "  skip $name: $dest exists and is not our link (use --force to replace)"
        status=1; continue
      fi
    else
      echo "  link $name"
    fi
    run ln -s "$src" "$dest"
  done
done
exit "$status"
