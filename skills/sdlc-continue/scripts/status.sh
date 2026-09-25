#!/bin/sh
# List active intent slugs. Run from the product repo root.
# Usage: sh path/to/status.sh
set -eu

if [ ! -d intent ]; then
	echo "no intent/ directory"
	exit 0
fi

fm_field() {
	# Print top-level YAML frontmatter field from the first --- block.
	# Missing file → "missing". Key absent → "none".
	_file=$1
	_key=$2
	if [ ! -f "$_file" ]; then
		printf '%s\n' "missing"
		return 0
	fi
	_val=$(awk -v key="$_key" '
		BEGIN { in_fm = 0 }
		/^---[[:space:]]*$/ {
			if (in_fm == 0) { in_fm = 1; next }
			exit
		}
		in_fm && $0 ~ ("^" key ":[[:space:]]*") {
			sub("^" key ":[[:space:]]*", "")
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

fm_status() {
	fm_field "$1" "status"
}

findings_have_critical() {
	# 0 if ## Findings contains a CRITICAL finding entry, else 1.
	_file=$1
	[ -f "$_file" ] || return 1
	awk '
		BEGIN { on = 0; found = 0 }
		/^## Findings[[:space:]]*$/ { on = 1; next }
		/^## / { on = 0 }
		on && /^[[:space:]]*[-*][[:space:]]+(\*\*)?CRITICAL(\*\*)?([[:space:]:]|$)/ { found = 1; exit }
		END { exit found ? 0 : 1 }
	' "$_file"
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
		if [ -f "${_dir}context.md" ]; then
			printf '%s\n' "sdlc-explore (context.md only), then sdlc-plan when ready"
		else
			printf '%s\n' "sdlc-plan (no intent.md)"
		fi
		return 0
	fi
	if [ "$_intent_st" = "draft" ]; then
		printf '%s\n' "present intent; on accept set accepted, then sdlc-design"
		return 0
	fi
	case "$_intent_st" in
		accepted|done) ;;
		*) printf '%s\n' "inspect invalid intent status ($_intent_st)"; return 0 ;;
	esac
	if [ "$_spec_st" = "missing" ]; then
		printf '%s\n' "sdlc-design"
		return 0
	fi
	if [ "$_spec_st" = "draft" ]; then
		printf '%s\n' "sdlc-design (review draft and readiness before approval)"
		return 0
	fi
	case "$_spec_st" in
		specified|done) ;;
		*) printf '%s\n' "inspect invalid spec status ($_spec_st)"; return 0 ;;
	esac
	if [ "$_plan_st" = "missing" ]; then
		printf '%s\n' "sdlc-apply (plan step)"
		return 0
	fi
	if [ "$_total" -eq 0 ]; then
		printf '%s\n' "repair plan (0 boxes)"
		return 0
	fi
	if [ "$_plan_st" = "draft" ]; then
		printf '%s\n' "sdlc-apply (reconcile draft plan with approved spec before approval)"
		return 0
	fi
	case "$_plan_st" in
		planned|done) ;;
		*) printf '%s\n' "inspect invalid plan status ($_plan_st)"; return 0 ;;
	esac
	if [ "$_plan_st" = "done" ] && [ "$_ticked" -lt "$_total" ]; then
		printf '%s\n' "repair inconsistent plan (done with unticked boxes)"
		return 0
	fi
	if [ "$_ticked" -lt "$_total" ]; then
		printf '%s\n' "sdlc-apply implement (${_ticked}/${_total} boxes ticked)"
		return 0
	fi
	if [ ! -f "${_dir}report.md" ]; then
		printf '%s\n' "sdlc-verify"
		return 0
	fi

	_verdict=$(fm_field "${_dir}report.md" "verdict" | tr '[:upper:]' '[:lower:]')
	_critical=0
	if findings_have_critical "${_dir}report.md"; then
		_critical=1
	fi
	if [ "$_verdict" = "fail" ] || [ "$_critical" -eq 1 ]; then
		printf '%s\n' "sdlc-apply (fix findings) then sdlc-verify"
		return 0
	fi
	if [ "$_verdict" != "pass" ]; then
		printf '%s\n' "sdlc-verify"
		return 0
	fi
	_isolation=$(fm_field "${_dir}report.md" "isolation")
	case "$_isolation" in
		subagent|subagent-different-model|subagent-same-model) ;;
		*) printf '%s\n' "sdlc-verify (invalid isolation)"; return 0 ;;
	esac
	if [ "$_intent_st" = "done" ] &&
		{ [ "$_spec_st" = "done" ] || [ "$_spec_st" = "missing" ]; } &&
		{ [ "$_plan_st" = "done" ] || [ "$_plan_st" = "missing" ]; }; then
		printf '%s\n' "sdlc-archive"
		return 0
	fi
	printf '%s\n' "ask to mark done"
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
	if [ -f "${dir}report.md" ]; then
		printf '  verdict: %s\n' "$(fm_field "${dir}report.md" "verdict")"
	fi
	printf '  next: %s\n' "$gate"
done

if [ "$found" -eq 0 ]; then
	echo "no active intent slugs"
fi
