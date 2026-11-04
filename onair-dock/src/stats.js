'use strict';
const os = require('os');

function snapshot(cpus = os.cpus()) {
  let idle = 0;
  let total = 0;
  for (const c of cpus) {
    for (const v of Object.values(c.times)) total += v;
    idle += c.times.idle;
  }
  return { idle, total };
}

/** Percentage of CPU busy between two snapshots (0–100). */
function cpuPercent(prev, next) {
  const total = next.total - prev.total;
  const idle = next.idle - prev.idle;
  if (total <= 0) return 0;
  return Math.round(Math.min(100, Math.max(0, (1 - idle / total) * 100)));
}

function createSampler() {
  let prev = snapshot();
  return function sample() {
    const next = snapshot();
    const cpu = cpuPercent(prev, next);
    prev = next;
    const total = os.totalmem();
    const used = total - os.freemem();
    return { cpu, ram: Math.round((used / total) * 100), ramUsedGb: +(used / 1024 ** 3).toFixed(1) };
  };
}

module.exports = { snapshot, cpuPercent, createSampler };
