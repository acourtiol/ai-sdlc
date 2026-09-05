#!/bin/sh
# List active intent slugs. Run from the product repo root.
# Usage: sh path/to/status.sh
set -eu

if [ ! -d intent ]; then
	echo "no intent/ directory"
	exit 0
fi

fm_status() {
	# Print top-level status from the first YAML frontmatter block, or "missing".
	_file=$1
	if [ ! -f "$_file" ]; then
		printf '%s\n' "missing"
		return 0
	fi
	_val=$(awk '
		BEGIN { in_fm = 0 }
		/^---[[:space:]]*$/ {
			if (in_fm == 0) { in_fm = 1; next }
			exit
		}
		in_fm && /^status:[[:space:]]*/ {
			sub(/^status:[[:space:]]*/, "")
			sub(/[[:space:]]+$/, "")
			print
			exit
		}
	' "$_file")
	if [ -z "$_val" ]; then
		printf '%s\n' "none"
	else
		printf '%s\n' "$_val"
	fi
}

count_boxes() {
	# Sets TICKED and TOTAL from ## Order of work in $1.
	_plan=$1
	TICKED=0
	TOTAL=0
	if [ ! -f "$_plan" ]; then
		return 0
	fi
	# shellcheck disable=SC2034
	eval "$(awk '
		BEGIN { on = 0; ticked = 0; total = 0 }
		/^## Order of work/ { on = 1; next }
		/^## / { on = 0 }
		on && /^- \[[xX]\]/ { ticked++; total++; next }
		on && /^- \[ \]/ { total++ }
		END { printf "TICKED=%d TOTAL=%d\n", ticked, total }
	' "$_plan")"
}

next_gate() {
	_dir=$1
	_intent_st=$2
	_spec_st=$3
	_plan_st=$4
	_ticked=$5
	_total=$6

	if [ ! -f "${_dir}intent.md" ]; then
		printf '%s\n' "sdlc-plan (no intent.md)"
		return 0
	fi
	if [ "$_intent_st" = "draft" ]; then
		printf '%s\n' "present intent; on accept set accepted"
		return 0
	fi
	if [ "$_spec_st" = "missing" ]; then
		printf '%s\n' "sdlc-design"
		return 0
	fi
	if [ "$_spec_st" = "draft" ]; then
		printf '%s\n' "approve spec; on approve set specified"
		return 0
	fi
	if [ "$_plan_st" = "missing" ]; then
		printf '%s\n' "sdlc-apply (plan step)"
		return 0
	fi
	if [ "$_plan_st" = "draft" ]; then
		printf '%s\n' "approve the plan"
		return 0
	fi
	if [ "$_plan_st" = "planned" ]; then
		if [ "$_total" -gt 0 ] && [ "$_ticked" -lt "$_total" ]; then
			printf '%s\n' "sdlc-apply implement (${_ticked}/${_total} boxes ticked)"
			return 0
		fi
		if [ ! -f "${_dir}report.md" ]; then
			printf '%s\n' "sdlc-verify"
			return 0
		fi
	fi
	if [ -f "${_dir}report.md" ]; then
		if [ "$_intent_st" = "done" ] &&
			{ [ "$_spec_st" = "done" ] || [ "$_spec_st" = "missing" ]; } &&
			{ [ "$_plan_st" = "done" ] || [ "$_plan_st" = "missing" ]; }; then
			printf '%s\n' "sdlc-archive"
			return 0
		fi
		printf '%s\n' "ask to mark done"
		return 0
	fi
	printf '%s\n' "sdlc-verify"
}

found=0
for dir in intent/*/; do
	[ -d "$dir" ] || continue
	slug=$(basename "$dir")
	if [ "$slug" = "archive" ]; then
		continue
	fi
	found=1

	intent_st=$(fm_status "${dir}intent.md")
	spec_st=$(fm_status "${dir}spec.md")
	plan_st=$(fm_status "${dir}plan.md")
	count_boxes "${dir}plan.md"
	gate=$(next_gate "$dir" "$intent_st" "$spec_st" "$plan_st" "$TICKED" "$TOTAL")

	printf 'slug: %s\n' "$slug"
	printf '  intent: %s\n' "$intent_st"
	printf '  spec: %s\n' "$spec_st"
	printf '  plan: %s\n' "$plan_st"
	if [ -f "${dir}plan.md" ]; then
		printf '  boxes: %s/%s\n' "$TICKED" "$TOTAL"
	fi
	printf '  next: %s\n' "$gate"
done

if [ "$found" -eq 0 ]; then
	echo "no active intent slugs"
fi
