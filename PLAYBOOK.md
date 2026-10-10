# Playbook for automatic runs

Read PLAN.md first. Everything here is for Claude runs started by a schedule. The founder approves every item before it goes live. Never schedule anything that is not approved on the Content Board.

## Fixed references
- Media repo: GitHub Rakshakid/rakshak-social (public). Attach it with the add_repo tool (owner Rakshakid, repo rakshak-social, access push), then `git clone --depth 1 https://github.com/Rakshakid/rakshak-social`.
- Public media URL pattern: https://raw.githubusercontent.com/Rakshakid/rakshak-social/main/weeks/<week>/<file>
- Content Board artifact: https://claude.ai/artifact/GoDCFv3tXwk6qbxy5fMVGh (one board, republished each week; read it with the Artifact tool before publishing to it, publish with `url`). Its db collection `decisions` holds one doc per item id: {status: pending|approved|changes|rejected, note, updatedAt, metricoolId?}.
- Metricool brand: blogId 7215456, timezone Asia/Calcutta. Networks: instagram (@rakshakid, connected via Instagram login), facebook (RakshakId Page), youtube.
- Week spec: weeks/<week>/posts.json (list of items: id, day, date, time, format, nets, title, why, media[], ig_type, fb_type, yt{title,tags} optional, en, hi, tags, status_note).
- Item ids: w<N>-p<k> for posts, w<N>-s<k> stories, w<N>-r<k> reels. Week folder names: 2026-w<N>.

## Design system
Black #07090D, gold #E8B547, gold-hi #F6DFA6, ivory #F6F1E7, muted #B9BDC7. Fonts: Playfair Display (headlines), DM Sans (body), DM Mono (labels), Tiro Devanagari Hindi (Hindi). Lion logo top-left at 112px, rounded frame. Feed images 1080x1350, stories/reels 1080x1920.
Setup: `mkdir -p ~/.fonts && cp tools/fonts/*.ttf ~/.fonts/ && fc-cache -f`. Copy tools/render_lib.py (helpers) and tools/render_week2.py (latest example: carousels, stories, LinkedIn cards and animated reels; tools/captions_week2.py shows the posts.json format) to a work folder with tools/assets, replace the `slides` dict with the new week's slides (keep page/top/foot/CTA_SLIDE helpers), render with Playwright, then look at a contact sheet once and fix overlaps. Animated-text reel: adapt tools/reel_week1.py (5 scenes, crossfades, soft pad audio, ~15 s).
Convert images to JPEG (quality 93) before upload: Instagram accepts only JPEG.

## Run A: weekly drafting (Saturday evening)
0. FIRST check whether next week is already drafted: list the board's published files (Artifact list scope files on the board URL). If data/w<N>_posts.json for next week exists, STOP and send nothing (the founder sometimes asks for an early draft).
1. Work out next week's number and dates (Mon to Sun). Read PLAN.md for the phase, the Culture of Gratitude part due, and any dated occasions.
2. Check last week's results with Metricool getAnalyticsDataByMetrics where available; prefer formats that did well.
3. Write about 7 items following "Weekly output". Captions in English and Hindi plus hashtags.
4. Render media. Do NOT push unapproved media to GitHub (the repo is public; only approved media goes there). Publish the media on the board under media/w<N>/ and the week spec as data/w<N>_posts.json.
5. Republish the Content Board: take tools/board_template.html, replace the header (week, dates, phase) and the POSTS array with the new week's items; the artifact blocks external images, so publish the week's media files alongside the page via `files` under media/ and point src at media/<file>. Keep the db capability declaration unchanged (omit `capabilities` on republish).
6. Tell the founder in one short message that Week N is ready for approval, with the 3-line summary of the week.

## Run B: approval sweep (twice daily)
1. Read the `decisions` collection from the board (ArtifactData list).
2. For each item of the current and next week whose status is approved and has no metricoolId: fetch the week spec and media from the board (Artifact read with path data/w<N>_posts.json and media/w<N>/<file>), convert PNG to JPEG (quality 93), commit those approved files to weeks/2026-w<N>/ and push, then schedule with createScheduledPost using raw GitHub URLs. Items whose nets include LinkedIn go to provider 'linkedin' (linkedinData type post; if the item has li_doc, set documentTitle=li_doc and publishImagesAsPDF true); LinkedIn text is the item's `en` only. Instagram/Facebook text = en + '\n\n—\n\n' + hi + '\n\n' + tags. ( Instagram/Facebook stories carry no text; reels: instagramData.type REEL, facebookData.type REEL, youtubeData type short, madeForKids false). Then update the decision doc with metricoolId (pin if_version).
3. For items with status changes: apply the founder's note, re-render, push, update posts.json, republish the board, and set the decision back to pending with note "Revised: <what changed>".
4. Rejected items: do nothing except note them in the Monday report.
5. If nothing to do, finish silently.

## Run C: Monday report
Pull last week's Instagram, Facebook and YouTube metrics from Metricool (reach, impressions, followers, top post). Send the founder a short report: numbers, top 2 posts, what to change this week. Under 150 words.
