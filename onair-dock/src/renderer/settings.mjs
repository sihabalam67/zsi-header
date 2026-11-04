const $ = (id) => document.getElementById(id);
const api = window.dock;

const WIDGET_LABELS = {
  obs: 'OBS scenes + live status',
  nowPlaying: 'Now playing',
  runOfShow: 'Run of show',
  streamTimer: 'Stream timer',
  breakTimer: 'BRB break timer',
  system: 'CPU + RAM',
  clock: 'Clock',
};

const LICENSE_ERRORS = {
  malformed: 'That doesn’t look like a license key. Copy the whole key from your email.',
  'bad-signature': 'This key isn’t valid. Check you copied all of it.',
  'wrong-plan': 'This key isn’t for OnAir Dock Pro.',
  'not-configured': 'This build has no licensing set up (developer build), so Pro is already on.',
};

let state = null;

function render(s) {
  state = s;
  const { settings, isPro, proWidgets, version } = s;
  $('plan').textContent = isPro ? 'Pro' : 'Free';
  $('plan').classList.toggle('pro', isPro);
  $('version').textContent = `v${version}`;
  $('pro-box').classList.toggle('hidden', isPro);

  $('position').value = settings.position;
  $('height').value = settings.height;
  $('launchAtLogin').checked = settings.launchAtLogin;
  $('obs-host').value = settings.obs.host;
  $('obs-port').value = settings.obs.port;
  $('obs-password').value = settings.obs.password;
  $('ros').value = settings.runOfShow.join('\n');
  $('breakMinutes').value = settings.breakMinutes;

  $('widgets').replaceChildren(
    ...Object.entries(WIDGET_LABELS).map(([key, label]) => {
      const l = document.createElement('label');
      l.className = 'check';
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.dataset.widget = key;
      cb.checked = Boolean(settings.widgets[key]);
      l.append(cb, ` ${label}`);
      if (proWidgets.includes(key)) {
        const chip = document.createElement('span');
        chip.className = 'pro-chip';
        chip.textContent = 'PRO';
        l.append(' ', chip);
      }
      return l;
    })
  );
}

function collect() {
  const widgets = {};
  for (const cb of document.querySelectorAll('#widgets input[data-widget]')) widgets[cb.dataset.widget] = cb.checked;
  return {
    position: $('position').value,
    height: Number($('height').value),
    launchAtLogin: $('launchAtLogin').checked,
    widgets,
    obs: { host: $('obs-host').value.trim(), port: Number($('obs-port').value), password: $('obs-password').value },
    runOfShow: $('ros').value.split('\n'),
    breakMinutes: Number($('breakMinutes').value),
  };
}

$('save').addEventListener('click', async () => {
  render(await api.setSettings(collect()));
  $('saved').textContent = 'Saved ✓';
  setTimeout(() => ($('saved').textContent = ''), 2000);
});

$('buy').addEventListener('click', () => api.openBuy());

$('activate').addEventListener('click', async () => {
  const msg = $('license-msg');
  const res = await api.activateLicense($('license').value);
  if (res.valid) {
    msg.className = 'msg ok';
    msg.textContent = `Pro unlocked${res.email ? ` for ${res.email}` : ''}. Thank you!`;
  } else {
    msg.className = 'msg bad';
    msg.textContent = LICENSE_ERRORS[res.reason] || 'Couldn’t activate this key.';
  }
});

api.onState(render);
api.getState().then(render);
