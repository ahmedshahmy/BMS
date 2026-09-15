# British Muslim Society — Newsletter

A static, mobile-first newsletter for the British Muslim Society (BMS).

The title screen shows the society logo, the current issue's **tiles**, and
links to every previous issue. Tapping a tile opens the full article for that
tile, with its photo, its video and its text. No framework, no build step
required to view it, no server needed — it is plain HTML, CSS and JavaScript
that can be hosted anywhere.

---

## How it is laid out

```
bms/
├── index.html                 the whole app shell (one page, hash routed)
├── logo.png                   BMS logo — used in the header, footer and icons
├── manifest.webmanifest       "add to home screen" details for phones
├── css/style.css              mobile-first stylesheet, BMS navy/red palette
├── js/app.js                  hash router, tile grid, article view, archive
│
├── issues/
│   ├── index.js               generated catalogue of every issue
│   ├── 2025-11-autumn/        ← one folder per issue
│   │   ├── cover.jpg          cover image for the title screen / archive
│   │   ├── issue.js           generated manifest for this issue
│   │   ├── imams-message/     ← one folder per tile in the issue
│   │   │   ├── photo.jpg      the tile's photograph (also the video poster)
│   │   │   ├── video.mp4      the tile's clip (H.264 — plays on iOS + Android)
│   │   │   └── text.md        the tile's article text
│   │   ├── prayer-timetable/
│   │   │   ├── photo.jpg
│   │   │   ├── video.mp4
│   │   │   └── text.md
│   │   └── … one folder per tile
│   ├── 2025-08-summer/
│   └── 2025-03-ramadan/
│
├── tools/
│   ├── content.py             ← the articles: edit this
│   ├── build.py               generates media + manifests from content.py
│   └── smoke-test.mjs         headless-Chrome test of the whole site
└── serve.sh                   local preview server
```

Every issue folder contains **a folder for every tile in that issue**, and
every tile folder contains **a photo, a video and a text file**. That structure
is what the site reads, so an issue can be published by dropping files in and
running one command.

### Routes

| URL | Shows |
| --- | --- |
| `#/` | Title screen: logo, current issue hero, its tiles, previous issues |
| `#/archive` | Every published issue, newest first |
| `#/issue/<issue>/` | All tiles in one issue |
| `#/issue/<issue>/<tile>/` | One tile: photo, video and article |

Routes are deep-linkable, so `…/index.html#/issue/2025-03-ramadan/community-iftar`
can be texted to a member or shared on WhatsApp. The browser back button works
as expected on phones.

---

## Previewing it locally

```bash
./serve.sh            # then open http://127.0.0.1:8099/index.html
./serve.sh 8080       # or pick a port
```

Opening `index.html` directly off disk also works — the article text is inlined
into each issue's `issue.js`, so nothing needs a server except the browser's
normal file access.

---

## Publishing a new issue

1. **Add the issue to `tools/content.py`.** Add a new dict at the *top* of the
   `ISSUES` list (newest first — the first entry is the current issue):

   ```python
   {
       "slug": "2026-01-winter",          # becomes issues/2026-01-winter/
       "number": 13,
       "edition": "Winter 2026",
       "title": "Winter Newsletter",
       "published": "2026-01-05",         # newest wins if the list is unordered
       "date_label": "January 2026",
       "summary": "One or two sentences shown on the title screen.",
       "tiles": [
           {
               "slug": "imams-message",   # becomes a folder inside the issue
               "title": "Message from the Imam",
               "icon": "\U0001f54c",      # shown as a badge on the tile
               "blurb": "One line shown on the tile.",
               "text": "## Heading\n\nBody text…",
           },
           # … as many tiles as this issue needs
       ],
   },
   ```

   Each issue has its own tiles and its own articles — nothing is shared
   between issues, so every issue can cover whatever BMS did that period.

2. **Build the folders, placeholders and manifests:**

   ```bash
   python3 tools/build.py
   ```

   This creates `issues/<issue>/<tile>/` with `photo.jpg`, `video.mp4` and
   `text.md`, generates the issue cover, and rewrites `issues/index.js` and
   every `issue.js`.

3. **Drop in the real media.** Replace any `photo.jpg` (`1280×720`, 16:9) and
   `video.mp4` (`H.264`, `.mp4`) with the real files. Rebuilds never overwrite
   media that already exists.

4. **Test and commit:**

   ```bash
   ./serve.sh &                       # in another terminal
   node tools/smoke-test.mjs          # 26 checks in headless Chrome
   git add -A && git commit -m "Add Winter 2026 issue"
   ```

### Writing the article text

`text.md` supports a small, deliberate subset of Markdown — enough for a
newsletter, not enough to break the layout:

`## Heading` · `### Subheading` · paragraphs · `- bullets` · `1. numbered` ·
`> pull quotes` · `**bold**` · `*italic*` · `` `code` `` · `[links](https://…)`
· `---` rules · and pipe tables:

```
| Event | When |
| --- | --- |
| Community kitchen | Fridays after Maghrib |
```

The text is rendered with everything escaped first, so a stray `<` in an
article can never inject markup into the page.

---

## Publishing to the web

`.github/workflows/pages.yml` deploys the site to GitHub Pages on every push to
`main`. To switch it on:

```bash
git remote add origin git@github.com:<org-or-user>/<repo>.git
git push -u origin main
```

Then in the repository: **Settings → Pages → Build and deployment → Source:
GitHub Actions**. The workflow also re-runs the build and fails the deploy if
`issues/` is out of date, so the site can never quietly drift from
`tools/content.py`.

Any other static host works too — Netlify, Cloudflare Pages or plain nginx.
Just serve this folder; there is no server-side code.

---

## Notes for maintainers

- **Colour palette** is taken from `logo.png`: navy `#01237d`, red `#d0142b`,
  white. It lives in the `:root` block of `css/style.css`.
- **Dark mode** follows the reader's system setting automatically.
- **Accessibility:** skip link, focus moved on every navigation, `aria-current`
  on the active nav item, decorative icons hidden from screen readers,
  `prefers-reduced-motion` respected.
- **Video format:** tiles use H.264 MP4 in an `isom` container, `yuv420p`,
  `+faststart`, with `playsinline` on the element — this is the combination that
  plays inline on iOS Safari and everywhere else. Placeholder clips are a five
  second slow push over the tile photo, roughly 150–170 KB each.
- **Placeholder media** is only produced when a file is missing. Use
  `python3 tools/build.py --force-media` to deliberately regenerate it, or
  `--skip-media` to rewrite only the text and manifests.
- **Adding tiles to an *older* issue** works the same way: add the tile to that
  issue's `tiles` list and rebuild. The tile folder is created inside that
  issue's folder and nothing else changes.

---

© British Muslim Society. Newsletter content is published by the BMS
communications team.
