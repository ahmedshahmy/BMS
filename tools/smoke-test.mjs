#!/usr/bin/env node
/**
 * Headless smoke test for the BMS newsletter.
 *
 *   node tools/smoke-test.mjs [baseUrl]
 *
 * Drives real Chrome over the DevTools Protocol against a locally served copy
 * of the site and asserts the things that are easy to break: the tile grid,
 * deep links into an issue, the article view, the archive, image and video
 * loading, and horizontal overflow at phone width.
 *
 * Requires google-chrome (or chromium) on PATH and a static server, e.g.
 *   python3 -m http.server 8099 --bind 127.0.0.1
 */

import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const BASE = (process.argv[2] || 'http://127.0.0.1:8099/index.html').replace(/#.*$/, '');
const CHROME = process.env.CHROME_BIN || 'google-chrome';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const results = [];
function check(name, ok, detail = '') {
  results.push({ name, ok: !!ok, detail });
  console.log(`${ok ? '  \u2713' : '  \u2717'} ${name}${detail ? `  ${detail}` : ''}`);
}

/* ------------------------------------------------------------ CDP plumbing */

const port = 9400 + Math.floor(Math.random() * 400);
const profile = mkdtempSync(join(tmpdir(), 'bms-cdp-'));
const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--no-sandbox', '--no-first-run',
  '--disable-dev-shm-usage', '--mute-audio',
  `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
  'about:blank',
], { stdio: 'ignore' });

const pageErrors = [];
let ws;
let nextId = 1;
const pending = new Map();

function send(method, params = {}) {
  const id = nextId++;
  ws.send(JSON.stringify({ id, method, params }));
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
}

async function connect() {
  for (let i = 0; i < 80; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/list`);
      if (res.ok) {
        const list = await res.json();
        const target = list.find((t) => t.type === 'page');
        if (target) return target.webSocketDebuggerUrl;
      }
    } catch { /* not up yet */ }
    await sleep(250);
  }
  throw new Error('Chrome DevTools endpoint never became available');
}

function openSocket(url) {
  return new Promise((resolve, reject) => {
    ws = new WebSocket(url);
    ws.addEventListener('open', () => resolve());
    ws.addEventListener('error', reject);
    ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && pending.has(msg.id)) {
        const { resolve: res, reject: rej } = pending.get(msg.id);
        pending.delete(msg.id);
        if (msg.error) rej(new Error(`${msg.error.message}`));
        else res(msg.result);
        return;
      }
      if (msg.method === 'Runtime.exceptionThrown') {
        const d = msg.params.exceptionDetails;
        pageErrors.push(d.exception?.description || d.text || 'unknown exception');
      }
      if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
        pageErrors.push(msg.params.args.map((a) => a.value ?? a.description).join(' '));
      }
    });
  });
}

async function evaluate(expression) {
  const { result, exceptionDetails } = await send('Runtime.evaluate', {
    expression, returnByValue: true, awaitPromise: true,
  });
  if (exceptionDetails) {
    throw new Error(exceptionDetails.exception?.description || exceptionDetails.text);
  }
  return result.value;
}

/** Cold-load a URL (about:blank in between so the hash route really reloads). */
async function open(url) {
  await send('Page.navigate', { url: 'about:blank' });
  await sleep(120);
  await send('Page.navigate', { url });
  await sleep(1100);
  await settleImages();
}

/**
 * Tiles use loading="lazy", so images below the fold are not fetched until the
 * reader scrolls. Walk the page the way a reader would and wait for every image
 * to finish (or fail) before asserting anything about them -- otherwise the
 * test only measures network speed.
 */
async function settleImages(timeout = 20000) {
  await evaluate(`(async () => {
    const step = Math.max(200, window.innerHeight);
    for (let y = 0; y < document.body.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 120));
    }
    window.scrollTo(0, 0);
    await new Promise((r) => setTimeout(r, 200));
  })()`);
  return evaluate(`(async () => {
    const imgs = [...document.querySelectorAll('img')];
    const deadline = Date.now() + ${timeout};
    while (!imgs.every((i) => i.complete) && Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, 200));
    }
    return {
      total: imgs.length,
      loaded: imgs.filter((i) => i.complete && i.naturalWidth > 0).length,
    };
  })()`);
}

/* ------------------------------------------------------------- assertions */

const COLLECT = `(() => {
  const q = (s) => document.querySelector(s);
  const qa = (s) => [...document.querySelectorAll(s)];
  return {
    title: document.title,
    h1: qa('h1').map((h) => h.textContent.trim().replace(/\\s+/g, ' ')),
    tiles: qa('.tile').length,
    tileTitles: qa('.tile-title').map((t) => t.textContent.trim()),
    issueCards: qa('.issue-card').length,
    archiveNotice: !!q('.notice'),
    heroTag: q('.hero-tag')?.textContent.trim() || null,
    logoInHeader: (() => {
      const img = q('.brand-logo');
      return img ? { src: img.getAttribute('src'), loaded: img.complete && img.naturalWidth > 0 } : null;
    })(),
    video: (() => {
      const v = q('video');
      if (!v) return null;
      return {
        sources: qa('video source').map((s) => s.getAttribute('src')),
        poster: v.getAttribute('poster'),
        playsinline: v.hasAttribute('playsinline'),
        controls: v.hasAttribute('controls'),
      };
    })(),
    prose: {
      h2: qa('.prose h2').length,
      h3: qa('.prose h3').length,
      p: qa('.prose p').length,
      li: qa('.prose li').length,
      tables: qa('.prose table').length,
      quotes: qa('.prose blockquote').length,
      text: (q('.prose')?.textContent || '').slice(0, 120),
    },
    pager: qa('.pager a').length,
    images: qa('.tile-media img, .hero-img, .article-hero img, .issue-card-img img')
      .map((i) => ({ src: i.getAttribute('src'), loaded: i.complete && i.naturalWidth > 0 })),
    overflowPx: Math.max(0, document.documentElement.scrollWidth - window.innerWidth),
    error: !!q('.empty h1'),
  };
})()`;

/* ---------------------------------------------------- catalogue fixtures */
/*
 * Expectations are read from the generated manifests rather than hard-coded,
 * so adding issues or tiles never breaks the test -- only real regressions do.
 */

function parseManifest(js, marker) {
  const start = js.indexOf(marker);
  if (start === -1) throw new Error(`marker "${marker}" not found in manifest`);
  const rest = js.slice(start + marker.length);
  const json = rest.slice(rest.indexOf('=') + 1).trim().replace(/;\s*$/, '');
  return JSON.parse(json);
}

async function loadJson(path, marker) {
  const res = await fetch(new URL(path, BASE).href);
  if (!res.ok) throw new Error(`${path} -> HTTP ${res.status}`);
  return parseManifest(await res.text(), marker);
}

async function fixtures() {
  const catalog = await loadJson('issues/index.js', 'window.BMS_ISSUES');
  if (!catalog.length) throw new Error('the catalogue is empty');

  const issues = [];
  for (const meta of catalog) {
    const data = await loadJson(
      `issues/${meta.slug}/issue.js`, `window.BMS_ISSUE_DATA["${meta.slug}"]`,
    );
    issues.push(data);
  }

  const current = issues[0];
  const archived = issues.length > 1 ? issues[issues.length - 1] : null;
  const allTiles = issues.flatMap((issue) => issue.tiles.map((tile) => ({ issue, tile })));

  return {
    catalog,
    issues,
    current,
    archived,
    allTiles,
    // a tile that exercises tables, a tile with a clip, and one from an old issue
    tableTile: allTiles.find((x) => /\|\s*:?-{2,}/.test(x.tile.text)) || null,
    videoTile: allTiles.find((x) => x.tile.video) || null,
  };
}

async function main() {
  const fx = await fixtures();
  console.log(
    `Catalogue: ${fx.catalog.length} issues, ` +
    `${fx.catalog.reduce((n, i) => n + i.tileCount, 0)} tiles ` +
    `(current: ${fx.current.edition}, issue ${fx.current.number})`,
  );

  await openSocket(await connect());
  await send('Page.enable');
  await send('Runtime.enable');
  await send('Log.enable');
  await send('Emulation.setDeviceMetricsOverride', {
    width: 390, height: 844, deviceScaleFactor: 2, mobile: true,
  });

  /* ---- 1. title screen ------------------------------------------------ */
  console.log('\nTitle screen  (iPhone 12 viewport, 390x844)');
  await open(`${BASE}#/`);
  let s = await evaluate(COLLECT);
  const firstTile = fx.current.tiles[0];

  check('current issue tiles render on the title screen',
    s.tiles === fx.current.tiles.length, `${s.tiles} of ${fx.current.tiles.length} tiles`);
  check('logo is in the header and loads', s.logoInHeader?.loaded === true,
    s.logoInHeader ? s.logoInHeader.src : 'no logo');
  check('hero shows the latest edition',
    (s.h1[0] || '').includes(fx.current.edition) && (s.heroTag || '').includes(`Issue ${fx.current.number}`),
    `${s.h1[0]} / ${s.heroTag}`);
  check('previous issues are reachable from the title screen',
    s.issueCards === Math.min(2, fx.catalog.length - 1),
    `${s.issueCards} cards`);
  check('every tile photo loaded', s.images.length > 0 && s.images.every((i) => i.loaded),
    `${s.images.filter((i) => i.loaded).length}/${s.images.length}`);
  check('no horizontal overflow at 390px', s.overflowPx === 0, `${s.overflowPx}px`);

  /* ---- 2. tap a tile (client-side routing) ---------------------------- */
  console.log('\nSelecting a tile  (real click, hash router)');
  await evaluate(`document.querySelector('.tile').click()`);
  await sleep(900);
  await settleImages();
  s = await evaluate(COLLECT);
  check('clicking a tile opens its detail view',
    s.tiles === 0 && (s.h1[0] || '').includes(firstTile.title), s.h1[0]);
  check('detail view shows the article prose', s.prose.p >= 1 && s.prose.h2 >= 1,
    `${s.prose.p} paragraphs, ${s.prose.h2} h2`);
  const expectsVideo = !!firstTile.video;
  check('detail view has a video with an mp4 source',
    s.video === null ? !expectsVideo
      : s.video.sources.some((x) => /video\.mp4$/.test(x)) && s.video.controls && s.video.playsinline,
    s.video ? s.video.sources.join(',') : 'no video in this tile');
  // the first tile of an issue has only a "next" link; a lone tile has neither
  const expectedPager = fx.current.tiles.length > 1 ? 1 : 0;
  check('pager links to the neighbouring tile', s.pager === expectedPager,
    `${s.pager} links, expected ${expectedPager}`);
  check('no horizontal overflow in the article', s.overflowPx === 0, `${s.overflowPx}px`);

  if (fx.videoTile) {
    await open(`${BASE}#/issue/${fx.videoTile.issue.slug}/${fx.videoTile.tile.slug}`);
    const video = await evaluate(`(async () => {
      const v = document.querySelector('video');
      if (!v) return null;
      if (v.readyState < 1) await new Promise((r) => {
        v.addEventListener('loadedmetadata', r, { once: true });
        setTimeout(r, 5000);
      });
      return { w: v.videoWidth, h: v.videoHeight, d: Math.round(v.duration * 10) / 10, err: v.error?.code || null };
    })()`);
    check('video metadata loads in the browser', video && video.w > 0 && video.d > 0 && !video.err,
      video ? `${video.w}x${video.h}, ${video.d}s` : 'no video');
  }

  /* ---- 3. cold deep link into an archived issue ----------------------- */
  if (fx.archived) {
    console.log('\nArchived issue  (cold deep link)');
    await open(`${BASE}#/issue/${fx.archived.slug}`);
    s = await evaluate(COLLECT);
    check('archived issue lists its own tiles',
      s.tiles === fx.archived.tiles.length, `${s.tiles} tiles`);
    check('archived issue is flagged as archived', s.archiveNotice === true);
    check('archived issue shows its own tiles, not the current ones',
      s.tileTitles[0] === fx.archived.tiles[0].title, s.tileTitles[0]);
  } else {
    console.log('\nArchived issue  -- skipped (only one issue published)');
  }

  /* ---- 4. cold deep link straight into a tile ------------------------- */
  const deep = fx.tableTile || fx.allTiles[0];
  console.log('\nCold deep link straight into a tile');
  await open(`${BASE}#/issue/${deep.issue.slug}/${deep.tile.slug}`);
  s = await evaluate(COLLECT);
  check('deep link renders the right article', (s.h1[0] || '').includes(deep.tile.title), s.h1[0]);
  check('deep link sets the document title', s.title.includes(deep.tile.title), s.title);
  check('deep link loads its photo', s.images.every((i) => i.loaded));
  if (fx.tableTile) {
    check('markdown table renders', s.prose.tables >= 1, `${s.prose.tables} tables`);
    check('table content is readable', /[A-Za-z]/.test(s.prose.text), s.prose.text.slice(0, 40));
  }
  check('no horizontal overflow on the deep link', s.overflowPx === 0, `${s.overflowPx}px`);

  /* ---- 5. archive ------------------------------------------------------ */
  console.log('\nArchive');
  await open(`${BASE}#/archive`);
  s = await evaluate(COLLECT);
  check('archive lists every published issue',
    s.issueCards === fx.catalog.length, `${s.issueCards} cards`);
  check('archive covers all loaded', s.images.every((i) => i.loaded));

  /* ---- 6. bad route ---------------------------------------------------- */
  console.log('\nUnknown tile');
  await open(`${BASE}#/issue/${fx.current.slug}/not-a-real-tile`);
  s = await evaluate(COLLECT);
  check('unknown tile shows a "not found" state', s.error === true);

  /* ---- 7. tablet / desktop width -------------------------------------- */
  console.log('\nDesktop width  (1280x900)');
  await send('Emulation.setDeviceMetricsOverride', {
    width: 1280, height: 900, deviceScaleFactor: 1, mobile: false,
  });
  await open(`${BASE}#/`);
  s = await evaluate(COLLECT);
  const cols = await evaluate(`getComputedStyle(document.querySelector('.tile-grid')).gridTemplateColumns.split(' ').length`);
  check('tile grid becomes multi-column on desktop', cols >= 4, `${cols} columns`);
  check('no horizontal overflow at 1280px', s.overflowPx === 0, `${s.overflowPx}px`);

  /* ---- page errors ----------------------------------------------------- */
  const realErrors = pageErrors.filter((e) => !/favicon/i.test(e));
  check('no uncaught page errors or console errors', realErrors.length === 0,
    realErrors.slice(0, 3).join(' | '));

  /* ---- summary --------------------------------------------------------- */
  const failed = results.filter((r) => !r.ok);
  console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
  if (failed.length) {
    console.log('FAILED:\n' + failed.map((f) => `  - ${f.name} ${f.detail}`).join('\n'));
  }
  return failed.length ? 1 : 0;
}

let code = 1;
try {
  code = await main();
} catch (err) {
  console.error('\nSmoke test crashed:', err.message);
  code = 2;
} finally {
  try { ws?.close(); } catch { /* ignore */ }
  chrome.kill('SIGKILL');
  try { rmSync(profile, { recursive: true, force: true }); } catch { /* ignore */ }
}
process.exit(code);
