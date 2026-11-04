# OnAir Dock

A live dock for streamers on Windows 10/11. One slim bar at the top or bottom of the screen shows:

| Widget | Free | Pro |
|---|:-:|:-:|
| Clock, CPU + RAM | ✓ | ✓ |
| Run of show (tick off your stream segments) | ✓ | ✓ |
| Stream timer | ✓ | ✓ |
| **OBS**: LIVE / REC badges with uptime, one-click scene switching | | ✓ |
| **Now playing**: Spotify, browser, any Windows media, with play/pause/skip | | ✓ |
| **BRB**: full-bar break countdown | | ✓ |

Pro is one payment through a Stripe Payment Link and unlocks with an offline license key.

---

## Launch checklist (one time, about 20 minutes)

### 1. Install the tools
Install [Node.js 22](https://nodejs.org) on your computer, then run:
```bash
cd onair-dock
npm install
npm test          # 10 tests should pass
npm start         # opens the dock (on Windows you see the real thing)
```

### 2. Create your license keys
```bash
npm run license:init
```
This creates two files:
- `keys/private.pem` is **secret**. Back it up in your password manager. It's git-ignored, and if you lose it you can't issue keys that match the app anymore.
- `src/license-public.pem` ships inside the app. **Commit it.**

### 3. Create the Stripe Payment Link
1. In your Stripe dashboard, go to **Product catalog → Add product**: "OnAir Dock Pro", one-time price (for example $9).
2. Go to **Payment Links → New**, choose that product, and under *After payment* add a confirmation message such as "Your license key arrives by email within 12 hours."
3. Copy the link (`https://buy.stripe.com/...`) into `src/config.json` as `buyUrl`.

### 4. Build the Windows installer
Commit, then push a version tag:
```bash
git add -A && git commit -m "OnAir Dock: release setup"
git tag onair-v0.1.0 && git push origin onair-v0.1.0
```
GitHub Actions (`.github/workflows/onair-dock-release.yml`) builds `OnAir Dock Setup 0.1.0.exe` on Windows and attaches it to a GitHub Release. The build **refuses to run** if step 2 or 3 is missing, so you can't accidentally ship a free-for-everyone build.

### 5. When someone buys
Stripe emails you the payment and shows the buyer's email. Run:
```bash
npm run license:issue -- buyer@example.com
```
Email them the key it prints. They paste it in **Settings → Activate**, and Pro unlocks instantly, offline.
(Once sales are steady, automate this with a Stripe webhook that runs the same signing code.)

---

## How it works
- **Electron** app (`src/main.js`): a frameless, always-on-top bar sized to the primary screen's work area, with acrylic blur on Windows 11 and a tray icon (Settings, Top/Bottom, Hide, Quit).
- **OBS** (`src/renderer/obs-client.mjs`): talks to obs-websocket v5, which is built into OBS 28+. It handles password auth, auto-reconnects every 5s, and stops retrying on a wrong password. To set it up, in OBS go to **Tools → WebSocket Server Settings → Enable**, then copy the port and password into the dock's Settings.
- **Now playing** (`src/media.ps1`): a background PowerShell process reads the Windows media session (the same source as the Windows volume flyout). No extra install.
- **Licenses** (`src/license.js`): Ed25519-signed keys. The app holds only the public key, so keys can't be forged from the app.
- **Settings** are stored in `%APPDATA%\OnAir Dock\settings.json`.

## What has and hasn't been tested
- ✅ Unit tests: licenses (valid, forged, wrong key, garbage), settings, CPU math, media parsing, and the OBS client against a fake OBS server (auth, scene list, scene switch, events, wrong password).
- ✅ Ran the real Electron app (on Linux) against a fake OBS server: LIVE/REC uptime, scene switching, run of show, BRB overlay, settings window, and the Free → Pro unlock with a real key.
- ⚠️ **Not yet run on Windows itself.** The acrylic blur, tray icon, "start with Windows" and the Now Playing PowerShell script only work on Windows. Test the installer from step 4 on your PC before selling.
- ⚠️ The installer is **unsigned**, so Windows SmartScreen will say "Windows protected your PC → More info → Run anyway". A code-signing certificate (about $100–300 a year) removes that warning later.
