#!/usr/bin/env bash
# Recreates the dropshipping stack from the "Next.js Dropshipping Repos" list,
# install steps 1–3: Medusa, Sparx, MarketOS, Hyperswitch.
# Works on your own computer or in a Claude Code cloud session.
#
# Needs: git, Node 22+, pnpm, Python 3.11+, Docker (running).
# Usage:  bash store-stack/setup.sh [target-folder]   (default: ~/dropship-stack)
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:-$HOME/dropship-stack}"
mkdir -p "$TARGET"
cd "$TARGET"

clone() { # repo [branch]
  local name="${1#*/}"
  if [ -d "$name/.git" ]; then echo "• $name already cloned"; return; fi
  if [ -n "${2:-}" ]; then
    git clone --depth 1 --branch "$2" "https://github.com/$1.git"
  else
    git clone --depth 1 "https://github.com/$1.git"
  fi
}

echo "== 1. Medusa (medusajs/dtc-starter: backend + Next.js storefront)"
clone medusajs/dtc-starter
(cd dtc-starter && pnpm install)

echo "== 2. Sparx (SupplierAdapter package only)"
# The full repo needs Node 24 and a private FontAwesome token; the dropship
# adapter package does not.
clone brandonkorous/sparx
(cd sparx && pnpm install --filter "@wizeworksllc/dropship..." --config.engine-strict=false)

echo "== 3. MarketOS (Python)"
clone ChristianV997/MarketOS
(cd MarketOS && python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt)

echo "== 4. Hyperswitch (Docker, release branch 'latest')"
clone juspay/hyperswitch latest
cd hyperswitch
cp "$HERE/hyperswitch/docker-compose.override.yml" .
FILES=(-f docker-compose.yml -f docker-compose.override.yml)
if [ -f /root/.ccr/ca-bundle.crt ]; then
  cp "$HERE/hyperswitch/docker-compose.cloud-ca.yml" .
  FILES+=(-f docker-compose.cloud-ca.yml)
fi
dc() { ONE_CLICK_SETUP=true docker compose "${FILES[@]}" "$@"; } # ONE_CLICK_SETUP skips usage pings

# Database first, then the one config row the server needs at startup
# (Hyperswitch's own CI loads it from .github/data/payment_callback_config.sql).
dc up -d --wait pg redis-standalone   # migration_runner doesn't wait for the DB itself
dc up -d migration_runner
# `docker compose wait` exits with the container's exit code.
dc wait migration_runner >/dev/null || { echo "Database migrations failed: run 'docker compose logs migration_runner'"; exit 1; }
dc exec -T pg psql -U db_user -d hyperswitch_db -v ON_ERROR_STOP=1 < .github/data/payment_callback_config.sql
dc exec -T redis-standalone redis-cli DEL payment_callback >/dev/null
dc up -d || true   # the two usage-ping hooks may fail; that's harmless

echo
for url in http://localhost:8080/health http://localhost:9000 http://localhost:9050; do
  printf '%-32s %s\n' "$url" "$(curl -s -o /dev/null -w '%{http_code}' "$url" || echo down)"
done
echo "Control Center: http://localhost:9000  (demo@hyperswitch.com / Hyperswitch@123)"
echo "Stack installed in $TARGET"
