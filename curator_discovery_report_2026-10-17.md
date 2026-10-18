# Curator discovery — seeds kendallxcel + Brett Wolkey
Date checked: 2026-10-17. Deliverable: `curator_candidates_2026-10-17.csv` (31 rows, 31 unique Spotify owner URLs). No one was contacted and no music was submitted.

## 1. Tools actually used
| Tool | Status | Used for |
|---|---|---|
| Web search (WebSearch) | available | PlaylistSupply / isitagoodplaylist / article discovery, handle lookups |
| Web fetch (WebFetch) | available, but **403 on isitagoodplaylist.com, tiktok.com, instagram.com** | PlaylistSupply pages, link-in-bio pages (linktr.ee, beacons, link.me, fanlink), rapgemzmedia.com, trabbey.com |
| Built-in browser (signed-out) | available | open.spotify.com profiles + playlist headers (in-app pushState walk, ~100 pages), Instagram bios (meta description renders signed-out), TikTok bios, isitagoodplaylist curator pages |
| Claude in Chrome (Hunter's Chrome) | available, **logged into Chartmetric as Hunter Sallis** | all Chartmetric work |
| Chartmetric API | **not available** — no API key/client in this environment; subscription API entitlement not verified | — |
| Apify / paid scraping | not used (per instructions) | — |

## 2. Chartmetric access actually observed (Chrome session)
- Account badge shows **"Free"** with "Upgrade to Ultra" prompts; Flow Lite "20 credits · 22d". The built-in browser hits the Chartmetric login wall, so only the Chrome session works.
- Features that opened: global search (playlists/artists/tracks), Playlist pages (`/playlist/spotify/<id>/about`), **Curator pages** (`/curator/spotify/<id>/about|social|playlists|audience`), **Curators list** (`/curators`, 23,464,540 curators) with filters: keyword, playlist keyword, **Link Availability (All / With Social Links)**, Genre, **Curator Type (Spotify / Major Label / Commercial Brand / Popular Independent Curator / Independent Curator)**, plus a CSV export icon on the list. Artist pages → Playlists tab (placement data).
- Chartmetric-reported metrics (not my judgment):
  - kendallxcel — curator 14477186: total playlist followers 522,214; curator followers 103,582; 101 playlists; Trap Trackin playlist 2433308 = 23,991 followers (as of Sep 26, 2026), 393 tracks. **No social links exposed** on the About/Social tab (Social tab = follower trend charts only).
  - Brett Wolkey — curator 24290612: total playlist followers 43.9K; curator followers 12.5K; most popular playlist 14.3K; 19 playlists. Rap Cooks playlist 16948557 = 4.8K followers, stats last updated Jun 25, 2024. **No social links exposed.**
  - Curator social links DO appear when Chartmetric has tied the curator to an artist entity (example: 🇬🇧 Stewart Harding, curator 1145499210 → instagram.com/stewysongs, facebook, twitter, youtube). That Instagram link is dead ("Profile isn't available"), so Chartmetric-reported socials still need a live check.
  - "Related Curators" on both seed pages are genre-based and surfaced platform/brand accounts (PlayStation, Spotify, Soundbase…) — not useful for independent discovery.
  - Curators list filtered to Independent + Popular Independent, Hip-Hop/Rap, With Social Links = **1,661 curators**, but the top of that list is brands (Lofi Girl, Trap Nation, Chillhop, Promoting Sounds…) and the social icons in the Socials column are not readable as links through the DOM (output blocked). The **CSV export** of that filtered list is the export I would ask for if you want Chartmetric-sourced socials at scale (see §6).
- Chartmetric playlist pages give a link to the Spotify playlist and the curator name; the curator name click resolves to the Chartmetric curator page. That chain (seed playlist → Chartmetric curator → Spotify owner) is what I used to confirm both seed owner identities inside Chartmetric.

## 3. Seed inspection
**kendallxcel** (`open.spotify.com/user/kendallxw`) — 71 public playlists, 103,582 followers. Themes (from playlist names/descriptions): trap & melodic rap (Trap Trackin, Automatic Aux, Ballistic Bass, Hood Melodies), underground/underrated rap (Underground Wave, Underrated & Underground, Abstractics), dark/alt R&B & neo-soul (Toxic Tracks, Beds & Backseats, New Age R&B, Neo Soulful, Dark R&B Dimension), UK R&B/rap (British & B, Rap Innit), house (Hypnotic House, R&B House), gospel, afrobeats, workout. Descriptions repeatedly say "Follow My Music IG @Kendallxcel", "UNDERRATED series on TikTok & IG @kendallxcel", "Follow My YouTube @Kendallxcel". IG bio: LA · Digital Marketing · "Music Discovery + DM for promo" · Kendallxcel@solacetalent.com · linktr.ee/Kendallxw (linktree lists the Spotify profile and ~20 playlists). TikTok @kendallxcel 771.8K, bio "Playlist Curator · 180k on IG · Promo: IG or Kendallxcel@solacetalent.com". Four playlists on the profile are owned by others — **Rap Gemz Daily, Nj.terry (co-owner on Underrated & Underground), Selfmadeballer, Eddy B** — the first two became candidates (Selfmadeballer 14 followers / Eddy B 8 followers were dropped).

**Brett Wolkey** (`open.spotify.com/user/31x2ckbqq74jdlw7losjtmipdahm`) — 12,529 followers; the signed-out profile renders no playlists. isitagoodplaylist.com lists 11 playlists: Rap Cooks (2,352; rap/melodic rap/west coast), Modern Ambience (851; alt R&B/bedroom pop), Pumpkin Spice (813; indie folk/red dirt), The Weather's Getting Chilly (714), Brett's Rotation (609; indie folk/red dirt/surf rock/southern gothic), Songs That Make You Feel Like You're In A Movie (594), Take You To Space (435). TikTok @brettwolkey 1.2M ("The best suggestions from every genre", brett@wolkeycreative.com, beacons.ai/brettwolkey); beacons page links the exact Spotify user URL, IG @brettwolkey (483K, Nashville), YouTube, Snapchat.

## 4. Results
- **Unique candidates: 31** (deduplicated by Spotify owner URL; all 30 resolved to a Spotify owner URL).
- **Confirmed social accounts: 13** — kendallxcel, Brett Wolkey, Rap Gemz Daily, DJ Falkor, @trabbey, Skeud Rap, kasey's playlist, Fuegostine, lienneay, AfroDaPlug, zarasmixtapes, Sacha/@sachanostalgia (TikTok only), The Weisest Band/@theweisest (TikTok + playlist evidence). Each has a direct link chain (bio → link page → Spotify profile) or a playlist description naming the handle plus the social bio pointing back.
- **Probable (name match or curator-stated handle, not independently linked): 3** — threesixtymusic, Lux Thugs, earthtozariahh.
- **Spotify curator confirmed but no public social found: 15** — Tommy Craze (DripDrop, from Chartmetric placement data), Nj.terry, cowpenguin1, Jeff Shelby, awills, New Noise Dept., Retro Tones, josie, Indie Space Records, Emillyy, Ben Jammin, Bedroom Jams, caitlinvst, Michael Patrick, kristif1228 (three of these expose an email or a paid submission link instead).
- Best fits by lane: kendallxcel lane → Nj.terry, awills, cowpenguin1 (trap soul), AfroDaPlug (Drip/Soul Mode), Rap Gemz Daily, Sacha (UK R&B), Skeud Rap (FR rap); Brett Wolkey lane → kasey's playlist, Fuegostine, zarasmixtapes, The Weisest Band, Ben Jammin, lienneay, Retro Tones, cowpenguin1 (country rap), Jeff Shelby.

## 5. Pages / platforms blocked or degraded
- WebFetch: 403 on isitagoodplaylist.com, instagram.com, tiktok.com (worked in the built-in browser instead); linktr.ee/theweisestband renders labels but no destination URLs in either tool.
- Chartmetric in the built-in browser: login wall (not bypassed; used the already-authorized Chrome session). Chartmetric Socials-column HTML was blocked by the tool's output filter.
- PlaylistSupply: curator email/Instagram are paywalled (masked) — not bypassed.
- Instagram "Profile isn't available": @luxthugs, @indiespacerecords, @stewysongs (Chartmetric-listed), @nj.terry, @theweisestband. @earthtozariahh exists but is empty.
- Spotify: Brett Wolkey's profile shows no playlists signed-out; three PlaylistSupply-indexed playlists are deleted/private (0eiBLLgDc3gdczMPloRQDu, 0637zquklF4CeOcZ0FRnJ1, 2D5CLab7HqVEHtB0WC3RWq). "LATE NIGHT DRIVES 🖤" (79K) shown on Nj.terry's profile is owned by "AZ", not Nj.terry.
- dripdrop.tv (Tommy Craze's contact site): WebFetch socket error and the built-in browser navigation was denied, so his IG/TikTok handles stay unresolved.
- Chartmetric API: not used (no key); Chartmetric "Curators" filtered list not exported.

## 6. Were the tools sufficient? What remains incomplete
Sufficient for the 25-candidate target and for social verification of the TikTok/IG-forward curators. Not sufficient for: (a) socials of the PlaylistSupply-style "network" curators (cowpenguin1, Jeff Shelby, awills, Emillyy) whose contacts exist only behind PlaylistSupply's paywall; (b) Chartmetric-sourced socials at scale.
Exports that would close the gaps:
1. Chartmetric → Marketing → Curators → filters: Curator Type = Independent Curator + Popular Independent Curator; Genre = Hip-Hop/Rap (then R&B/Soul, then Alternative); Link Availability = Curators With Social Links → **CSV export** (download icon at top-right of the list). Columns needed: Curator, Spotify URL, Playlists, Playlist Followers, Socials.
2. Chartmetric → artist pages for representative underground artists (Nine Vicious, B7!, Eli G, JaWill, Pz', millkzy for kendallxcel; Noah Kahan-adjacent folk acts for Brett) → Playlists tab → Spotify → **export** of current placements with the "Curator" column, filtered to non-editorial playlists.
3. Optional: PlaylistSupply membership reveal for the 14 no-social rows (their own contact fields).
Placement walk done for one artist only: Chartmetric → Nine Vicious (artist 12902373) → Playlists/Spotify listed current placements (Most Necessary, No Cap, New Music Friday = editorial; Hip-Hop and Play = PlayStation; KANYE WEST BANGERS by 'dog standing up'; CLEAN RAP 2026 by DYNAMIX 78.1K; DripDrop by Tommy Craze 76K; Lyrical Lemonade Summer Smash). DripDrop resolved to Spotify user 12159044814 and is in the CSV; 'dog standing up' and DYNAMIX were not resolved. Remaining artists (B7!, Eli G, JaWill, Pz', millkzy) not walked.

## 7. Discovery sources used
Seed profiles (followed/co-owned playlists) · PlaylistSupply genre pages (trap, R&B, hip-hop, neo-soul) and curator pages · isitagoodplaylist.com curator pages · Music Directory substack (musicdirectory.substack.com/p/playlist-curators) · hellothematic.com TikTok-curator article · TikTok /discover/playlist-curators · Chartmetric Curators list + curator/playlist pages · Hypebot curator lists (2017/2020; no usable independent names).
