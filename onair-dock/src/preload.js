'use strict';
const { contextBridge, ipcRenderer } = require('electron');

const listen = (channel) => (fn) => {
  const handler = (_e, payload) => fn(payload);
  ipcRenderer.on(channel, handler);
  return () => ipcRenderer.removeListener(channel, handler);
};

contextBridge.exposeInMainWorld('dock', {
  getState: () => ipcRenderer.invoke('state:get'),
  setSettings: (patch) => ipcRenderer.invoke('settings:set', patch),
  openSettings: () => ipcRenderer.invoke('settings:open'),
  activateLicense: (key) => ipcRenderer.invoke('license:activate', key),
  openBuy: () => ipcRenderer.invoke('buy:open'),
  mediaCommand: (cmd) => ipcRenderer.invoke('media:command', cmd),
  onState: listen('state'),
  onStats: listen('stats'),
  onMedia: listen('media'),
});
