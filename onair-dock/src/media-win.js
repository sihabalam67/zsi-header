'use strict';
// Runs media.ps1 in a long-lived PowerShell process and turns its JSON lines into events.
const { spawn } = require('child_process');
const path = require('path');
const readline = require('readline');

function scriptPath() {
  // Inside a packaged app the script is unpacked next to app.asar.
  return path.join(__dirname, 'media.ps1').replace(`app.asar${path.sep}`, `app.asar.unpacked${path.sep}`);
}

function parseLine(line) {
  try {
    const d = JSON.parse(line);
    if (d.error) return { available: false };
    if (!d.title) return { available: true, playing: false, title: '', artist: '' };
    return {
      available: true,
      playing: d.status === 'Playing',
      title: String(d.title).slice(0, 120),
      artist: String(d.artist || '').slice(0, 120),
    };
  } catch {
    return null;
  }
}

function startMediaWatcher(onUpdate) {
  if (process.platform !== 'win32') {
    onUpdate({ available: false });
    return { send() {}, stop() {} };
  }
  let child = null;
  let stopped = false;
  let restarts = 0;

  const launch = () => {
    child = spawn('powershell.exe', ['-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', scriptPath()], {
      windowsHide: true,
      stdio: ['pipe', 'pipe', 'ignore'],
    });
    readline.createInterface({ input: child.stdout }).on('line', (line) => {
      const parsed = parseLine(line);
      if (parsed) {
        restarts = 0;
        onUpdate(parsed);
      }
    });
    child.on('exit', () => {
      if (stopped) return;
      restarts += 1;
      if (restarts > 5) return onUpdate({ available: false });
      setTimeout(launch, 3000 * restarts);
    });
  };
  launch();

  return {
    send(cmd) {
      if (['toggle', 'next', 'prev'].includes(cmd) && child && child.stdin.writable) child.stdin.write(cmd + '\n');
    },
    stop() {
      stopped = true;
      if (child) child.kill();
    },
  };
}

module.exports = { startMediaWatcher, parseLine };
