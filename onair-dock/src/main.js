'use strict';
const { app, BrowserWindow, ipcMain, screen, shell, Tray, Menu, nativeImage } = require('electron');
const path = require('path');
const { SettingsStore } = require('./settings-store');
const { createSampler } = require('./stats');
const { startMediaWatcher } = require('./media-win');
const license = require('./license');
const config = require('./config.json');

const PRO_WIDGETS = new Set(['obs', 'nowPlaying', 'breakTimer']);
const MARGIN = 8;

let store;
let dock = null;
let settingsWin = null;
let tray = null;
let media = null;
let statsTimer = null;
let isPro = false;

if (!app.requestSingleInstanceLock()) {
  app.quit();
}

function computePro(settings) {
  const pub = license.loadPublicKey();
  // No public key = developer build: everything unlocked. check-release blocks shipping like that.
  if (!pub) return true;
  return license.verify(settings.license, pub).valid;
}

function publicState() {
  const s = store.get();
  return { settings: s, isPro, proWidgets: [...PRO_WIDGETS], buyUrl: config.buyUrl, version: app.getVersion() };
}

function dockBounds(settings) {
  const display = screen.getPrimaryDisplay();
  const wa = display.workArea;
  const height = settings.height;
  return {
    x: wa.x + MARGIN,
    width: wa.width - MARGIN * 2,
    height,
    y: settings.position === 'bottom' ? wa.y + wa.height - height - MARGIN : wa.y + MARGIN,
  };
}

function createDock() {
  const s = store.get();
  dock = new BrowserWindow({
    ...dockBounds(s),
    frame: false,
    transparent: process.platform !== 'win32',
    backgroundColor: process.platform === 'win32' ? '#00000000' : undefined,
    backgroundMaterial: process.platform === 'win32' ? 'acrylic' : undefined,
    resizable: false,
    movable: false,
    minimizable: false,
    maximizable: false,
    fullscreenable: false,
    skipTaskbar: true,
    alwaysOnTop: true,
    hasShadow: false,
    show: false,
    title: 'OnAir Dock',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });
  dock.setAlwaysOnTop(true, 'floating');
  dock.setVisibleOnAllWorkspaces(true);
  dock.loadFile(path.join(__dirname, 'renderer', 'dock.html'));
  dock.once('ready-to-show', () => dock.showInactive());
  dock.on('closed', () => (dock = null));
  lockNavigation(dock);
}

function openSettings() {
  if (settingsWin) return settingsWin.focus();
  settingsWin = new BrowserWindow({
    width: 560,
    height: 720,
    title: 'OnAir Dock Settings',
    autoHideMenuBar: true,
    backgroundColor: '#14141b',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });
  settingsWin.loadFile(path.join(__dirname, 'renderer', 'settings.html'));
  settingsWin.on('closed', () => (settingsWin = null));
  lockNavigation(settingsWin);
}

function lockNavigation(win) {
  win.webContents.on('will-navigate', (e) => e.preventDefault());
  win.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
}

function broadcast(channel, payload) {
  for (const w of [dock, settingsWin]) if (w && !w.isDestroyed()) w.webContents.send(channel, payload);
}

function relayout() {
  if (dock && !dock.isDestroyed()) dock.setBounds(dockBounds(store.get()));
}

function applySettings(patch) {
  const before = store.get();
  const after = store.set(patch);
  isPro = computePro(after);
  if (before.position !== after.position || before.height !== after.height) relayout();
  if (before.launchAtLogin !== after.launchAtLogin && app.isPackaged) {
    app.setLoginItemSettings({ openAtLogin: after.launchAtLogin });
  }
  syncMedia(after);
  rebuildTrayMenu();
  broadcast('state', publicState());
  return publicState();
}

function syncMedia(s) {
  const wanted = s.widgets.nowPlaying && isPro;
  if (wanted && !media) media = startMediaWatcher((m) => broadcast('media', m));
  if (!wanted && media) {
    media.stop();
    media = null;
  }
}

function trayIcon() {
  const img = nativeImage.createFromPath(path.join(__dirname, 'renderer', 'icon.png'));
  return img.isEmpty() ? img : img.resize({ width: 16, height: 16 });
}

function rebuildTrayMenu() {
  if (!tray) return;
  const s = store.get();
  tray.setContextMenu(
    Menu.buildFromTemplate([
      { label: 'Settings…', click: openSettings },
      {
        label: 'Position',
        submenu: ['top', 'bottom'].map((p) => ({
          label: p === 'top' ? 'Top of screen' : 'Bottom of screen',
          type: 'radio',
          checked: s.position === p,
          click: () => applySettings({ position: p }),
        })),
      },
      { label: dock && dock.isVisible() ? 'Hide dock' : 'Show dock', click: toggleDock },
      { type: 'separator' },
      { label: 'Quit OnAir Dock', click: () => app.quit() },
    ])
  );
}

function toggleDock() {
  if (!dock) return createDock();
  if (dock.isVisible()) dock.hide();
  else dock.showInactive();
  rebuildTrayMenu();
}

app.on('second-instance', openSettings);

app.whenReady().then(() => {
  store = new SettingsStore(app.getPath('userData'));
  isPro = computePro(store.get());

  ipcMain.handle('state:get', () => publicState());
  ipcMain.handle('settings:set', (_e, patch) => applySettings(patch));
  ipcMain.handle('settings:open', () => openSettings());
  ipcMain.handle('license:activate', (_e, key) => {
    const result = license.verify(key, license.loadPublicKey());
    if (result.valid) applySettings({ license: String(key).trim() });
    return { valid: result.valid, reason: result.reason || null, email: result.payload ? result.payload.email : null };
  });
  ipcMain.handle('buy:open', () => {
    if (/^https:\/\/(buy\.stripe\.com|checkout\.stripe\.com)\//.test(config.buyUrl)) shell.openExternal(config.buyUrl);
  });
  ipcMain.handle('media:command', (_e, cmd) => media && media.send(cmd));

  createDock();
  tray = new Tray(trayIcon());
  tray.setToolTip('OnAir Dock');
  tray.on('click', toggleDock);
  rebuildTrayMenu();

  const sample = createSampler();
  statsTimer = setInterval(() => broadcast('stats', sample()), 2000);
  syncMedia(store.get());

  screen.on('display-metrics-changed', relayout);
  screen.on('display-added', relayout);
  screen.on('display-removed', relayout);
});

app.on('window-all-closed', (e) => e.preventDefault()); // keep running in the tray
app.on('before-quit', () => {
  clearInterval(statsTimer);
  if (media) media.stop();
});
