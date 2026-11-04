/** 75_000 -> "1:15", 3_723_000 -> "1:02:03" */
export function fmtDuration(ms) {
  const total = Math.max(0, Math.floor(ms / 1000));
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const s = total % 60;
  const pad = (n) => String(n).padStart(2, '0');
  return h > 0 ? `${h}:${pad(m)}:${pad(s)}` : `${m}:${pad(s)}`;
}

export function fmtClock(date, locale) {
  return date.toLocaleTimeString(locale, { hour: '2-digit', minute: '2-digit' });
}

/** Next unfinished item index in a run-of-show, or -1 when everything is done. */
export function nextItem(items, doneCount) {
  return doneCount < items.length ? doneCount : -1;
}
