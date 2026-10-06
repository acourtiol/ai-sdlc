#!/bin/sh
# List open intents and the next gate for each. Run from the product repo root,
# or pass the root: sh status.sh [repo-root]. Read-only.
set -eu

root=${1:-.}
dir="$root/intent"

# Value of a frontmatter key (first match between the opening and closing ---).
fm() {
  [ -f "$2" ] || return 0
  awk -v key="$1" '
    { sub(/\r$/, "") }
    NR == 1 && $0 != "---" { exit }
    NR > 1 && $0 == "---" { exit }
    index($0, key ":") == 1 {
      v = substr($0, length(key) + 2)
      sub(/[ \t]*#.*/, "", v)
      gsub(/^[ \t]+|[ \t]+$/, "", v)
      gsub(/^["'"'"']|["'"'"']$/, "", v)
      print v
      exit
    }' "$2"
}

# "ticked/total" of checkboxes under "## Steps" (or whole file if no such heading).
steps() {
  [ -f "$1" ] || { echo "0/0"; return 0; }
  awk '
    /^## / { in_steps = ($0 ~ /^## Steps/); seen = seen || in_steps }
    /^[ \t]*- \[[ xX]\]/ { all_total++; if ($0 ~ /\[[xX]\]/) all_done++
      if (in_steps) { total++; if ($0 ~ /\[[xX]\]/) done++ } }
    END { if (seen) printf "%d/%d", done, total; else printf "%d/%d", all_done, all_total }' "$1"
}

found=0
for d in "$dir"/*/; do
  [ -d "$d" ] || continue
  slug=$(basename "$d")
  [ "$slug" = "archive" ] && continue
  found=1
  intent="$d/intent.md"
  if [ ! -f "$intent" ]; then
    echo "$slug | no intent.md | next: sdlc-plan (or delete if abandoned)"
    continue
  fi
  status=$(fm status "$intent"); status=${status:-draft}
  tier=$(fm tier "$intent"); tier=${tier:-change}
  [ -z "$(fm tier "$intent")" ] && [ -f "$d/spec.md" ] && tier=critical
  verdict=$(fm verdict "$d/report.md"); verdict=${verdict:--}
  progress=$(steps "$intent")
  [ "$progress" = "0/0" ] && [ -f "$d/plan.md" ] && progress=$(steps "$d/plan.md")
  ticked=${progress%/*}; total=${progress#*/}

  case "$status" in
    draft) next="accept or correct the intent (sdlc-plan)" ;;
    done) next="close: delete the folder (sdlc-apply)" ;;
    *)
      if [ "$total" -eq 0 ]; then
        next="write the steps and build (sdlc-apply)"
      elif [ "$ticked" -lt "$total" ]; then
        next="continue steps (sdlc-apply)"
      elif [ "$verdict" = "fail" ]; then
        next="repair the findings (sdlc-apply), then delta re-review (sdlc-verify)"
      elif [ "$verdict" = "blocked" ]; then
        next="restore a fresh review route, then sdlc-verify"
      elif [ "$verdict" != "pass" ]; then
        next="independent review (sdlc-verify)"
      else
        next="user acceptance, then close (sdlc-apply)"
      fi
      ;;
  esac
  echo "$slug | tier $tier | $status | steps $progress | report $verdict | next: $next"
done

[ "$found" -eq 1 ] || echo "no open intents"
