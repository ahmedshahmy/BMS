## This tile is ready for a real article

This issue and this tile were generated as a starting point, so the folder
structure is already in place and publishing works end to end. Nothing here
is real news yet — replace it whenever you are ready.

### Putting the real article in

1. Open `tools/content.py` and edit the `text` of the `new-article` tile in
   the `2026-09-autumn` issue. It is ordinary Markdown: `##` headings,
   `-` bullets, `>` pull quotes and pipe tables all work.
2. Replace `issues/2026-09-autumn/new-article/photo.jpg` with the real
   photograph, and `video.mp4` with the real clip (H.264 `.mp4`).
3. Run `python3 tools/build.py`, then commit and push.

The build only creates media that is missing, so a real photograph dropped
into a tile folder is never overwritten.

### Adding more tiles

Give each tile a `slug`, a `title`, an `icon` and a `blurb` in
`tools/content.py`, and `tools/build.py` creates its folder complete with a
photo, a video and a text file.
