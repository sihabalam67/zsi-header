# Dropshipping stack setup

One script that recreates install steps 1–3 from the "Next.js Dropshipping Repos" list.
It clones the repos fresh; they are **not** copied into this repository.

| Step | Repo | What gets installed |
|---|---|---|
| 1 | medusajs/dtc-starter | Medusa backend + Next.js storefront |
| 2 | brandonkorous/sparx | Only the `@wizeworksllc/dropship` SupplierAdapter package |
| 3 | ChristianV997/MarketOS | Python environment (supplier quoting, margin model) |
| 4 | juspay/hyperswitch | Payments server, Control Center and payment widget, run with Docker |

## Run it

On your own computer, install these first:
- Git
- Node 22+ with pnpm (`corepack enable`)
- Python 3.11+
- Docker Desktop: give it about 8 GB of RAM and keep it running

Then:

```
bash store-stack/setup.sh            # installs into ~/dropship-stack
```

When it finishes:
- **Hyperswitch Control Center:** http://localhost:9000
- **Login:** `demo@hyperswitch.com` / `Hyperswitch@123`

## Why the Hyperswitch override files exist
The upstream `latest` Docker setup doesn't start cleanly as of Nov 2026. `hyperswitch/docker-compose.override.yml` fixes it without changing Hyperswitch's own files:
- runs a bash seed script with bash
- runs the database migrations without a broken developer-only patch step

`setup.sh` also loads one config row that the server needs at startup. It's the same file Hyperswitch's own CI loads.

`docker-compose.cloud-ca.yml` is only used inside Claude Code cloud sessions, so containers can trust that session's network proxy.

Hyperswitch's usage-ping hooks are skipped (`ONE_CLICK_SETUP=true`).

## Stop / start Hyperswitch later
```
cd ~/dropship-stack/hyperswitch
docker compose down        # stop (data kept)
docker compose up -d       # start again
```
