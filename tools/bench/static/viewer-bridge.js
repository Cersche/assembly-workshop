// Added to served responses only; saved viewer pages stay untouched.
(() => {
  'use strict';
  function start() {
    const rows = [...document.querySelectorAll('#parts label.part')];
    const names = rows.map(row => row.querySelector('.name')?.textContent ?? '');
    function solo(name) {
      if (name !== null && !names.includes(name)) return;
      rows.forEach((row, i) => {
        const checkbox = row.querySelector('input[type="checkbox"]');
        if (!checkbox) return;
        checkbox.checked = name === null || names[i] === name;
        checkbox.dispatchEvent(new Event('change', {bubbles: true}));
      });
      document.querySelector('#reset')?.click();
    }
    window.addEventListener('message', event => {
      const data = event.data;
      if (event.source !== parent || !data || typeof data !== 'object' ||
          Object.keys(data).length !== 2 || data.bench !== 'solo' ||
          !(data.name === null || typeof data.name === 'string')) return;
      solo(data.name);
    });
    if (location.hash.startsWith('#solo=')) {
      try { solo(decodeURIComponent(location.hash.slice(6))); } catch {}
    }
    if (parent !== window) parent.postMessage({bench: 'parts', names}, '*');
  }
  if (document.readyState === 'complete') start();
  else window.addEventListener('load', start, {once: true});
})();
