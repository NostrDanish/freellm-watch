#!/usr/bin/env bash
# Updater + change detector for the freellm-watch cron job.
# Fast-forwards both local clones, reinstalls/restarts the freellmapi gateway
# when its code changed, and prints the new HEAD SHAs — cron skips the agent
# run when stdout is unchanged.
set -u

pull() { # dir
  git -C "$1" fetch -q origin || return 0
  local old new
  old=$(git -C "$1" rev-parse HEAD); new=$(git -C "$1" rev-parse origin/main)
  [ "$old" = "$new" ] || git -C "$1" merge --ff-only -q origin/main
  echo "$new"
}

GW=~/Work/freellmapi
old_gw=$(git -C "$GW" rev-parse HEAD)
pull "$GW"
pull ~/Work/awesome-free-llm-apis

# restart gateway only when it actually moved; deps only when lockfile moved
new_gw=$(git -C "$GW" rev-parse HEAD)
if [ "$new_gw" != "$old_gw" ]; then
  git -C "$GW" diff --name-only "$old_gw" "$new_gw" | grep -q package-lock.json \
    && npm --prefix "$GW" ci --omit=dev -s
  systemctl --user restart freellmapi.service
fi
