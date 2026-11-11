#!/usr/bin/env bash
# Fast-forward watched repositories without assuming their default branch is main.
# Configuration is environment-based so this works on different hosts.
set -Eeuo pipefail

FREELLMAPI_DIR="${FREELLMAPI_DIR:-$HOME/Work/freellmapi}"
AWESOME_APIS_DIR="${AWESOME_APIS_DIR:-$HOME/Work/awesome-free-llm-apis}"
SERVICE_NAME="${FREELLMAPI_SERVICE:-freellmapi.service}"

die() { printf 'freellm-watch: %s\n' "$*" >&2; exit 1; }

default_branch_ref() {
  local dir="$1" ref
  ref=$(git -C "$dir" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null || true)
  if [[ -n "$ref" ]]; then
    printf '%s\n' "$ref"
    return 0
  fi
  # A remote may not have origin/HEAD configured. Ask Git for its advertised HEAD.
  local branch
  branch=$(git -C "$dir" remote show origin 2>/dev/null | sed -n 's/^  HEAD branch: //p' | head -n1)
  [[ -n "$branch" && "$branch" != "(unknown)" ]] || return 1
  printf 'origin/%s\n' "$branch"
}

fast_forward_repo() {
  local dir="$1" ref old new
  [[ -d "$dir/.git" ]] || die "not a Git repository: $dir"
  git -C "$dir" remote get-url origin >/dev/null 2>&1 || die "missing origin remote: $dir"
  ref=$(default_branch_ref "$dir") || die "cannot determine origin default branch for $dir"
  git -C "$dir" fetch --prune origin
  old=$(git -C "$dir" rev-parse HEAD)
  new=$(git -C "$dir" rev-parse "$ref")
  if [[ "$old" != "$new" ]]; then
    git -C "$dir" merge --ff-only "$ref"
  fi
  printf '%s\n' "$new"
}

[[ -d "$FREELLMAPI_DIR" ]] || die "set FREELLMAPI_DIR to the freellmapi clone"
[[ -d "$AWESOME_APIS_DIR" ]] || die "set AWESOME_APIS_DIR to the awesome-free-llm-apis clone"

old_gateway=$(git -C "$FREELLMAPI_DIR" rev-parse HEAD)
fast_forward_repo "$FREELLMAPI_DIR" >/dev/null
fast_forward_repo "$AWESOME_APIS_DIR" >/dev/null
new_gateway=$(git -C "$FREELLMAPI_DIR" rev-parse HEAD)

if [[ "$new_gateway" != "$old_gateway" ]]; then
  if git -C "$FREELLMAPI_DIR" diff --name-only "$old_gateway" "$new_gateway" | grep -qx 'package-lock.json'; then
    command -v npm >/dev/null 2>&1 || die "npm is required because package-lock.json changed"
    npm --prefix "$FREELLMAPI_DIR" ci --omit=dev
  fi
  if command -v systemctl >/dev/null 2>&1; then
    systemctl --user restart "$SERVICE_NAME"
  else
    die "systemctl is unavailable; refusing to claim the gateway was restarted"
  fi
fi

# Stable output for cron/change detection, including both repositories.
printf 'freellmapi=%s\n' "$new_gateway"
printf 'awesome-free-llm-apis=%s\n' "$(git -C "$AWESOME_APIS_DIR" rev-parse HEAD)"
