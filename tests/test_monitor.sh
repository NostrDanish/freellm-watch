#!/usr/bin/env bash
# Integration test: monitor.sh must follow each repository's advertised default branch.
set -Eeuo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

init_repo() {
  local path="$1" branch="$2"
  mkdir -p "$path"
  git -C "$path" init -q --initial-branch="$branch"
  git -C "$path" config user.email test@example.invalid
  git -C "$path" config user.name Test
  printf 'initial\n' > "$path/file.txt"
  git -C "$path" add file.txt
  git -C "$path" commit -qm initial
}

make_remote() {
  local name="$1" branch="$2"
  init_repo "$TMP/$name-seed" "$branch"
  git clone -q --bare "$TMP/$name-seed" "$TMP/$name.git"
  git clone -q "$TMP/$name.git" "$TMP/$name"
  git -C "$TMP/$name" remote set-head origin "$branch"
}

make_remote gateway main
make_remote awesome master
# Add a new commit to both remote default branches.
for name in gateway awesome; do
  branch=main
  [[ "$name" == awesome ]] && branch=master
  printf 'updated\n' >> "$TMP/$name-seed/file.txt"
  git -C "$TMP/$name-seed" add file.txt
  git -C "$TMP/$name-seed" commit -qm updated
  git -C "$TMP/$name-seed" push -q "$TMP/$name.git" "$branch"
done

mkdir -p "$TMP/bin"
cat > "$TMP/bin/systemctl" <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$SYSTEMCTL_LOG"
SH
cat > "$TMP/bin/npm" <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$NPM_LOG"
SH
chmod +x "$TMP/bin/"*

PATH="$TMP/bin:$PATH" \
FREELLMAPI_DIR="$TMP/gateway" \
AWESOME_APIS_DIR="$TMP/awesome" \
SYSTEMCTL_LOG="$TMP/systemctl.log" \
NPM_LOG="$TMP/npm.log" \
  bash "$ROOT/monitor.sh" > "$TMP/output"

grep -q 'freellmapi=' "$TMP/output"
grep -q 'awesome-free-llm-apis=' "$TMP/output"
[[ "$(git -C "$TMP/gateway" rev-parse HEAD)" == "$(git -C "$TMP/gateway" rev-parse origin/main)" ]]
[[ "$(git -C "$TMP/awesome" rev-parse HEAD)" == "$(git -C "$TMP/awesome" rev-parse origin/master)" ]]
grep -q 'restart freellmapi.service' "$TMP/systemctl.log"
! grep -q 'ci --omit=dev' "$TMP/npm.log"
echo "monitor.sh integration test: PASS"
