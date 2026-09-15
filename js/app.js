/* ==========================================================================
   British Muslim Society — Newsletter
   Hash router + views. No build step, no dependencies.

   Routes
     #/                       title screen (current issue tiles + past issues)
     #/archive                every published issue
     #/issue/<issue>          the tiles for one issue
     #/issue/<issue>/<tile>   one tile: photo, video and the article
   ========================================================================== */

(function () {
  'use strict';

  var SITE = {
    name: 'British Muslim Society',
    short: 'BMS',
    email: 'newsletter@britishmuslimsociety.org.uk'
  };

  var main = document.getElementById('main');
  var header = document.getElementById('siteHeader');
  var issueCache = window.BMS_ISSUE_DATA || {};
  var issuePromises = {};
  var catalog = Array.isArray(window.BMS_ISSUES) ? window.BMS_ISSUES.slice() : [];

  // newest first; tolerates a hand-edited catalog that is out of order
  catalog.sort(function (a, b) {
    return String(b.published).localeCompare(String(a.published));
  });

  /* ---------------------------------------------------------------- utils */

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function attr(s) { return esc(s); }

  function issueBySlug(slug) {
    for (var i = 0; i < catalog.length; i++) {
      if (catalog[i].slug === slug) return catalog[i];
    }
    return null;
  }

  function currentIssue() { return catalog[0] || null; }

  /** Load and cache issues/<slug>/issue.js (works from file:// too). */
  function loadIssue(slug) {
    if (issueCache[slug]) return Promise.resolve(issueCache[slug]);
    if (issuePromises[slug]) return issuePromises[slug];

    issuePromises[slug] = new Promise(function (resolve, reject) {
      var el = document.createElement('script');
      el.src = 'issues/' + encodeURIComponent(slug) + '/issue.js';
      el.async = true;
      el.onload = function () {
        var data = (window.BMS_ISSUE_DATA || {})[slug];
        if (data) { issueCache[slug] = data; resolve(data); }
        else { reject(new Error('Issue manifest for "' + slug + '" is empty.')); }
      };
      el.onerror = function () {
        reject(new Error('Could not load issues/' + slug + '/issue.js'));
      };
      document.head.appendChild(el);
    });

    return issuePromises[slug];
  }

  /* ------------------------------------------------------ markdown -> html */

  function inline(text) {
    var s = esc(text);
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    s = s.replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>');
    s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, function (m, label, href) {
      var safe = /^(https?:|mailto:|tel:|#|\/)/i.test(href) ? href : '#';
      var ext = /^https?:/i.test(safe)
        ? ' target="_blank" rel="noopener noreferrer"' : '';
      return '<a href="' + attr(safe) + '"' + ext + '>' + label + '</a>';
    });
    return s;
  }

  function splitRow(row) {
    return row.trim().replace(/^\|/, '').replace(/\|$/, '').split('|')
      .map(function (c) { return c.trim(); });
  }

  function renderMarkdown(md) {
    var lines = String(md || '').replace(/\r\n?/g, '\n').split('\n');
    var out = [];
    var i = 0;

    function blank(l) { return !l.trim(); }
    function startsBlock(l) {
      return blank(l) ||
        /^\s*(#{1,6}\s|>|\||[-*+]\s|\d+[.)]\s)/.test(l) ||
        /^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(l);
    }

    while (i < lines.length) {
      var line = lines[i];

      if (blank(line)) { i++; continue; }

      if (/^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(line)) {
        out.push('<hr>'); i++; continue;
      }

      var h = /^(#{1,6})\s+(.*)$/.exec(line);
      if (h) {
        var level = Math.max(2, Math.min(h[1].length, 4));
        out.push('<h' + level + '>' + inline(h[2].trim()) + '</h' + level + '>');
        i++; continue;
      }

      if (/^\s*\|/.test(line)) {
        var rows = [];
        while (i < lines.length && /^\s*\|/.test(lines[i])) { rows.push(splitRow(lines[i])); i++; }
        var head = rows[0] || [];
        var body = rows.slice(1);
        if (body.length && body[0].every(function (c) { return /^:?-{2,}:?$/.test(c); })) {
          body = body.slice(1);
        } else {
          head = [];
        }
        var hasHead = head.length && head.some(function (c) { return c !== ''; });
        var html = '<div class="table-scroll"><table>';
        if (hasHead) {
          html += '<thead><tr>' + head.map(function (c) {
            return '<th scope="col">' + inline(c) + '</th>';
          }).join('') + '</tr></thead>';
        }
        html += '<tbody>' + body.map(function (r) {
          return '<tr>' + r.map(function (c, ci) {
            var tag = (hasHead && ci === 0) ? 'th' : 'td';
            var scope = (hasHead && ci === 0) ? ' scope="row"' : '';
            return '<' + tag + scope + '>' + inline(c) + '</' + tag + '>';
          }).join('') + '</tr>';
        }).join('') + '</tbody></table></div>';
        out.push(html);
        continue;
      }

      if (/^\s*>\s?/.test(line)) {
        var quote = [];
        while (i < lines.length && /^\s*>\s?/.test(lines[i])) {
          quote.push(lines[i].replace(/^\s*>\s?/, ''));
          i++;
        }
        out.push('<blockquote>' + renderMarkdown(quote.join('\n')) + '</blockquote>');
        continue;
      }

      if (/^\s*[-*+]\s+/.test(line) || /^\s*\d+[.)]\s+/.test(line)) {
        var ordered = /^\s*\d+[.)]\s+/.test(line);
        var items = [];
        while (i < lines.length &&
               (/^\s*[-*+]\s+/.test(lines[i]) || /^\s*\d+[.)]\s+/.test(lines[i]))) {
          items.push(lines[i].replace(/^\s*(?:[-*+]|\d+[.)])\s+/, ''));
          i++;
        }
        var tag2 = ordered ? 'ol' : 'ul';
        out.push('<' + tag2 + '>' + items.map(function (t) {
          return '<li>' + inline(t) + '</li>';
        }).join('') + '</' + tag2 + '>');
        continue;
      }

      var para = [];
      while (i < lines.length && !startsBlock(lines[i])) { para.push(lines[i]); i++; }
      if (!para.length) { para.push(lines[i]); i++; }
      var text = para.map(function (l, idx) {
        var hard = /\s{2,}$/.test(l);
        var chunk = inline(l.trim());
        return idx < para.length - 1 ? chunk + (hard ? '<br>' : ' ') : chunk;
      }).join('');
      out.push('<p>' + text + '</p>');
    }

    return out.join('\n');
  }

  /* -------------------------------------------------------------- markup */

  function tileCards(tiles, issueSlug) {
    return '<ul class="tile-grid">' + tiles.map(function (t) {
      return '<li>' +
        '<a class="tile" href="#/issue/' + encodeURIComponent(issueSlug) + '/' +
          encodeURIComponent(t.slug) + '">' +
          '<span class="tile-media">' +
            '<img src="' + attr(t.photo) + '" alt="" loading="lazy" decoding="async" ' +
              'width="1280" height="720">' +
            (t.icon ? '<span class="tile-badge" aria-hidden="true">' + esc(t.icon) + '</span>' : '') +
            (t.video ? '<span class="tile-play">Video</span>' : '') +
          '</span>' +
          '<span class="tile-body">' +
            '<span class="tile-title">' + esc(t.title) + '</span>' +
            '<span class="tile-blurb">' + esc(t.blurb) + '</span>' +
          '</span>' +
        '</a></li>';
    }).join('') + '</ul>';
  }

  function issueCards(issues, latestSlug) {
    return '<ul class="issue-list">' + issues.map(function (it) {
      return '<li><a class="issue-card" href="#/issue/' + encodeURIComponent(it.slug) + '">' +
        '<span class="issue-card-img">' +
          '<img src="' + attr(it.cover) + '" alt="" loading="lazy" decoding="async" ' +
            'width="1280" height="560">' +
        '</span>' +
        '<span class="issue-card-body">' +
          '<span class="issue-card-num">Issue ' + esc(it.number) +
            (it.slug === latestSlug ? ' &middot; Latest' : '') + '</span>' +
          '<h3>' + esc(it.edition) + '</h3>' +
          '<p>' + esc(it.summary) + '</p>' +
          '<span class="issue-card-meta">' + esc(it.dateLabel) + ' &middot; ' +
            esc(it.tileCount) + ' tiles</span>' +
        '</span>' +
      '</a></li>';
    }).join('') + '</ul>';
  }

  function loading(label) {
    return '<div class="shell"><div class="loading" role="status">' +
      '<div class="spinner" aria-hidden="true"></div>' +
      '<p>' + esc(label || 'Loading\u2026') + '</p></div></div>';
  }

  function emptyState(title, body) {
    return '<div class="shell"><div class="empty"><h1>' + esc(title) + '</h1>' +
      '<p>' + body + '</p>' +
      '<p><a class="btn" href="#/">Back to the title screen</a></p></div></div>';
  }

  function notFound(what) {
    return emptyState('Not found', 'We could not find ' + esc(what) +
      '. It may belong to an issue that has not been published yet.');
  }

  function setTitle(t) {
    document.title = t ? t + ' \u00b7 ' + SITE.name : SITE.name + ' \u00b7 Newsletter';
  }

  function markNav(view) {
    var links = document.querySelectorAll('.header-nav a');
    for (var i = 0; i < links.length; i++) {
      var isHome = links[i].getAttribute('data-nav') === 'home';
      var active = (view === 'home' && isHome) ||
                   (view !== 'home' && !isHome);
      if (active) links[i].setAttribute('aria-current', 'page');
      else links[i].removeAttribute('aria-current');
    }
  }

  /* --------------------------------------------------------------- views */

  function viewHome() {
    var latest = currentIssue();
    if (!latest) {
      main.innerHTML = emptyState(
        'No issues published yet',
        'Run <code>python3 tools/build.py</code> to generate the newsletter ' +
        'from the content in <code>tools/content.py</code>.'
      );
      setTitle('');
      return Promise.resolve();
    }

    main.innerHTML = loading('Loading the latest issue\u2026');

    return loadIssue(latest.slug).then(function (issue) {
      var past = catalog.filter(function (i) { return i.slug !== latest.slug; });

      var html =
        '<div class="shell">' +
          '<section class="hero">' +
            '<img class="hero-img" src="' + attr(issue.cover) + '" alt="" ' +
              'width="1280" height="560" fetchpriority="high" decoding="async">' +
            '<div class="hero-body">' +
              '<span class="hero-tag">Issue ' + esc(issue.number) + ' &middot; Latest</span>' +
              '<h1>' + esc(issue.edition) + '</h1>' +
              '<p>' + esc(issue.summary) + '</p>' +
              '<div class="hero-actions">' +
                '<a class="btn" href="#/issue/' + encodeURIComponent(issue.slug) + '">' +
                  'Open this issue</a>' +
                (past.length
                  ? '<a class="btn btn-ghost" href="#/archive">Past issues (' +
                    past.length + ')</a>'
                  : '') +
              '</div>' +
            '</div>' +
          '</section>' +

          '<section class="section" id="tiles">' +
            '<div class="section-head">' +
              '<h2 class="section-title">In this issue</h2>' +
              '<span class="issue-card-num">' + esc(issue.dateLabel) + '</span>' +
            '</div>' +
            '<p class="eyebrow">Tap a tile to read more</p>' +
            tileCards(issue.tiles, issue.slug) +
          '</section>' +

          (past.length
            ? '<section class="section">' +
                '<div class="section-head">' +
                  '<h2 class="section-title">Previous issues</h2>' +
                  (past.length > 2
                    ? '<a href="#/archive">View all ' + past.length + ' &rarr;</a>' : '') +
                '</div>' +
                issueCards(past.slice(0, 2), latest.slug) +
              '</section>'
            : '') +
        '</div>';

      main.innerHTML = html;
      setTitle('');
    }).catch(function (err) {
      main.innerHTML = emptyState('Could not load the newsletter', esc(err.message));
      setTitle('Error');
    });
  }

  function viewArchive() {
    if (!catalog.length) { return viewHome(); }
    var latest = currentIssue();
    main.innerHTML = '<div class="shell">' +
      '<div class="page-head">' +
        '<p class="eyebrow">Archive</p>' +
        '<h1 class="page-title">Every issue</h1>' +
        '<p class="lede">All ' + catalog.length + ' published issues of the ' +
          esc(SITE.short) + ' newsletter, newest first.</p>' +
      '</div>' +
      '<section class="section">' +
        issueCards(catalog, latest ? latest.slug : null) +
      '</section></div>';
    setTitle('Every issue');
    return Promise.resolve();
  }

  function viewIssue(slug) {
    var meta = issueBySlug(slug) || { slug: slug, edition: slug };
    main.innerHTML = loading('Loading ' + (meta.edition || slug) + '\u2026');

    return loadIssue(slug).then(function (issue) {
      var latest = currentIssue();
      var isLatest = latest && latest.slug === issue.slug;

      main.innerHTML = '<div class="shell">' +
        '<nav class="breadcrumb" aria-label="Breadcrumb">' +
          '<a href="#/">Home</a><span aria-hidden="true">/</span>' +
          '<span>Issue ' + esc(issue.number) + '</span>' +
        '</nav>' +
        '<div class="page-head">' +
          '<p class="eyebrow">' + esc(issue.dateLabel) + ' &middot; Issue ' +
            esc(issue.number) + '</p>' +
          '<h1 class="page-title">' + esc(issue.edition) + '</h1>' +
          '<p class="lede">' + esc(issue.summary) + '</p>' +
        '</div>' +
        (isLatest ? '' :
          '<div class="notice"><span aria-hidden="true">\u2139\ufe0f</span><span>' +
          '<strong>You are reading an archived issue.</strong> ' +
          (latest ? '<a href="#/issue/' + encodeURIComponent(latest.slug) +
            '">Open the latest issue (' + esc(latest.edition) + ')</a>.' : '') +
          '</span></div>') +
        '<section class="section">' +
          '<div class="section-head">' +
            '<h2 class="section-title">In this issue</h2>' +
            '<span class="issue-card-num">' + issue.tiles.length + ' tiles</span>' +
          '</div>' +
          '<p class="eyebrow">Tap a tile to read more</p>' +
          tileCards(issue.tiles, issue.slug) +
        '</section>' +
        '<p><a class="link-back" href="#/archive">All issues</a></p>' +
        '</div>';

      setTitle(issue.edition);
    }).catch(function (err) {
      main.innerHTML = emptyState('Could not load that issue', esc(err.message));
      setTitle('Error');
    });
  }

  function viewTile(issueSlug, tileSlug) {
    main.innerHTML = loading('Loading\u2026');

    return loadIssue(issueSlug).then(function (issue) {
      var index = -1;
      for (var i = 0; i < issue.tiles.length; i++) {
        if (issue.tiles[i].slug === tileSlug) { index = i; break; }
      }
      if (index === -1) {
        main.innerHTML = notFound('that tile');
        setTitle('Not found');
        return;
      }

      var tile = issue.tiles[index];
      var prev = issue.tiles[index - 1];
      var next = issue.tiles[index + 1];
      var base = '#/issue/' + encodeURIComponent(issue.slug) + '/';
      var latest = currentIssue();
      var isLatestIssue = latest && latest.slug === issue.slug;

      function pagerLink(t, dir, cls) {
        if (!t) return '<span class="spacer"></span>';
        return '<a class="' + cls + '" href="' + base + encodeURIComponent(t.slug) + '">' +
          '<span class="pager-dir">' + dir + '</span>' +
          '<span>' + esc(t.title) + '</span></a>';
      }

      main.innerHTML =
        '<div class="shell">' +
          '<div class="back-bar">' +
            '<a class="link-back" href="#/issue/' + encodeURIComponent(issue.slug) + '">' +
              'All tiles</a>' +
            '<button class="share-btn" type="button" id="shareBtn">Share</button>' +
          '</div>' +

          '<figure class="article-hero">' +
            '<img src="' + attr(tile.photo) + '" alt="" width="1280" height="720" ' +
              'fetchpriority="high" decoding="async">' +
          '</figure>' +

          '<header class="article-head">' +
            '<p class="eyebrow">' + esc(issue.edition) + ' &middot; Issue ' +
              esc(issue.number) + (isLatestIssue ? ' &middot; Latest' : '') + '</p>' +
            '<h1>' + (tile.icon ? '<span class="article-icon" aria-hidden="true">' +
              esc(tile.icon) + '</span>' : '') +
              '<span>' + esc(tile.title) + '</span></h1>' +
            '<div class="article-meta">' +
              '<span>' + esc(issue.dateLabel) + '</span>' +
              '<span class="dot" aria-hidden="true">&bull;</span>' +
              '<span>Tile ' + (index + 1) + ' of ' + issue.tiles.length + '</span>' +
            '</div>' +
          '</header>' +

          (tile.video
            ? '<div class="video-block">' +
                '<video controls playsinline preload="metadata" ' +
                  'poster="' + attr(tile.photo) + '" width="1280" height="720">' +
                  '<source src="' + attr(tile.video) + '" type="video/mp4">' +
                  'Your browser cannot play this video. ' +
                  '<a href="' + attr(tile.video) + '">Download it instead</a>.' +
                '</video>' +
                '<p class="video-caption">Video: ' + esc(tile.title) + ' \u2014 ' +
                  esc(issue.edition) + '</p>' +
              '</div>'
            : '') +

          '<article class="prose">' + renderMarkdown(tile.text) + '</article>' +

          '<nav class="pager" aria-label="More tiles in this issue">' +
            pagerLink(prev, '\u2190 Previous', 'prev') +
            pagerLink(next, 'Next \u2192', 'next') +
          '</nav>' +

          '<p class="section"><a class="link-back" href="#/issue/' +
            encodeURIComponent(issue.slug) + '">Back to all tiles in ' +
            esc(issue.edition) + '</a></p>' +
        '</div>';

      setTitle(tile.title + ' \u2014 ' + issue.edition);
      wireShare(tile.title, issue.edition);
      revealFirstImage();
    }).catch(function (err) {
      main.innerHTML = emptyState('Could not load that tile', esc(err.message));
      setTitle('Error');
    });
  }

  function wireShare(title, edition) {
    var btn = document.getElementById('shareBtn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var url = location.href;
      var payload = { title: title + ' \u2014 ' + edition, text: title, url: url };
      if (navigator.share) {
        navigator.share(payload).catch(function () { /* dismissed */ });
        return;
      }
      var done = function () {
        btn.textContent = 'Link copied';
        setTimeout(function () { btn.textContent = 'Share'; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done).catch(function () {
          window.prompt('Copy this link:', url);
        });
      } else {
        window.prompt('Copy this link:', url);
      }
    });
  }

  function revealFirstImage() {
    var img = main.querySelector('.article-hero img');
    if (img) img.loading = 'eager';
  }

  /* -------------------------------------------------------------- router */

  function parseRoute() {
    var raw = String(location.hash || '').replace(/^#\/?/, '');
    var parts = raw.split('/').filter(Boolean).map(function (p) {
      try { return decodeURIComponent(p); } catch (e) { return p; }
    });

    if (parts[0] === 'archive' || parts[0] === 'issues') return { view: 'archive' };
    if (parts[0] === 'issue' && parts[1]) {
      return parts[2]
        ? { view: 'tile', issue: parts[1], tile: parts[2] }
        : { view: 'issue', issue: parts[1] };
    }
    return { view: 'home' };
  }

  function render() {
    var route = parseRoute();
    var result;

    if (route.view === 'archive') result = viewArchive();
    else if (route.view === 'issue') result = viewIssue(route.issue);
    else if (route.view === 'tile') result = viewTile(route.issue, route.tile);
    else result = viewHome();

    markNav(route.view);

    Promise.resolve(result).then(function () {
      if (header) header.classList.toggle('is-scrolled', window.scrollY > 8);
      // keep the reading position predictable on every navigation
      if (!window.__bmsSkipScroll) window.scrollTo(0, 0);
      window.__bmsSkipScroll = false;
      try { main.focus({ preventScroll: true }); } catch (e) { main.focus(); }
    });
  }

  /* --------------------------------------------------------------- boot */

  function boot() {
    var year = document.getElementById('year');
    if (year) year.textContent = new Date().getFullYear();

    // graceful fallback if a photo or clip is missing on disk
    document.addEventListener('error', function (ev) {
      var el = ev.target;
      if (el && el.tagName === 'IMG' && el.closest && el.closest('.tile-media')) {
        el.style.display = 'none';
      }
    }, true);

    window.addEventListener('hashchange', render);
    render();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
