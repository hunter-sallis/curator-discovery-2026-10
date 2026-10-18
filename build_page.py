#!/usr/bin/env python3
"""Render curator_candidates_2026-10-17.csv into the Keyman single-page report (index.html)."""
import csv, html, re, sys, pathlib

HERE = pathlib.Path(__file__).parent
CSV = HERE / "curator_candidates_2026-10-17.csv"
OUT = HERE / "index.html"
REV = sys.argv[1] if len(sys.argv) > 1 else "1"
DATE = "2026-10-17"
STYLE = pathlib.Path.home() / "Code/km-report-kit/reference/keyman_style_block.html"

rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
assert len(rows) == len({r["spotify_profile"] for r in rows}), "duplicate Spotify owner"

def esc(s): return html.escape(s or "", quote=True)

def status_key(r):
    s = r["verification_status"].upper()
    if s.startswith("CONFIRMED"): return "confirmed"
    if s.startswith("PROBABLE"): return "probable"
    return "none"

def lane(r):
    g = r["genre_mood"].lower()
    rap = bool(re.search(r"rap|trap|r&b|rnb|soul|hip.?hop|drill|afro|gospel|house", g))
    indie = bool(re.search(r"indie|folk|country|surf|acoustic|alt|americana|blues|retro|colour|pop", g))
    if rap and indie: return "Both"
    if rap: return "Rap / R&B"
    if indie: return "Indie / folk"
    return "Other"

def handle(url):
    if not url: return ""
    m = re.search(r"(instagram\.com/|tiktok\.com/@)([A-Za-z0-9_.]+)", url)
    return "@" + m.group(2) if m else url

def link(url, text=None, cls=""):
    if not url: return "<span class=faint>—</span>"
    u = url.split(" ")[0]
    return f'<a href="{esc(u)}" target=_blank rel=noopener class="{cls}">{esc(text or u)}</a>'

def social_cell(r, key):
    v = r[key]
    if not v: return "<span class=faint>—</span>"
    if v.startswith("http"):
        extra = v[v.find(" "):].strip() if " " in v else ""
        out = link(v, handle(v))
        if extra: out += f' <span class=sm>{esc(extra)}</span>'
        return out
    return f'<span class=sm>{esc(v)}</span>'

PILL = {"confirmed": ("green", "Confirmed"), "probable": ("amber", "Probable"), "none": ("grey", "No social found")}

counts = {k: sum(1 for r in rows if status_key(r) == k) for k in PILL}
seeds = [r for r in rows if "(SEED)" in r["curator_name"]]
others = [r for r in rows if "(SEED)" not in r["curator_name"]]
order = {"confirmed": 0, "probable": 1, "none": 2}
others.sort(key=lambda r: (order[status_key(r)], r["curator_name"].lower()))

def table_rows(rs):
    out = []
    for r in rs:
        k = status_key(r)
        pc, pt = PILL[k]
        name = r["curator_name"].replace(" (SEED)", "")
        pl = r["relevant_playlist_url"]
        plt = pl.rsplit("/", 1)[-1][:10] + "…" if pl else ""
        contact = r["public_submission_or_contact_link"]
        ccell = link(contact.split(" ")[0], "Submission / contact") if contact.startswith("http") else (f'<span class=sm>{esc(contact)}</span>' if contact else "<span class=faint>—</span>")
        out.append(
            f'<tr data-status="{k}" data-lane="{esc(lane(r))}" data-q="{esc((name + " " + r["genre_mood"] + " " + r["instagram"] + " " + r["tiktok"]).lower())}">'
            f'<td data-label="Curator"><b>{esc(name)}</b><div class=sm>{esc(r["genre_mood"])}</div></td>'
            f'<td data-label="Lane"><span class="pill blue">{esc(lane(r))}</span></td>'
            f'<td data-label="Spotify">{link(r["spotify_profile"], "Profile")}' + (f' · {link(pl, "Playlist")}' if pl else "") + '</td>'
            f'<td data-label="Instagram">{social_cell(r, "instagram")}</td>'
            f'<td data-label="TikTok">{social_cell(r, "tiktok")}</td>'
            f'<td data-label="Status"><span class="pill {pc}">{pt}</span></td>'
            f'<td data-label="Reach" class=sm>{esc(r["reported_metrics"])}</td>'
            f'<td data-label="Contact">{ccell}</td>'
            f'<td data-label="Evidence" class=sm>{esc(r["verification_evidence_url"])}<div class=faint style="margin-top:4px">Source: {esc(r["discovery_source"])}' + (f' · <a href="{esc(r["chartmetric_url"])}" target=_blank rel=noopener>Chartmetric</a>' if r["chartmetric_url"] else "") + (f'<br>{esc(r["notes"])}' if r["notes"] else "") + '</div></td>'
            '</tr>')
    return "\n".join(out)

seed_cards = ""
for r in seeds:
    name = r["curator_name"].replace(" (SEED)", "")
    seed_cards += f'''<div class=card><p class=eyebrow>Seed curator</p><h3>{esc(name)}</h3>
<p class=sm style="margin:0 0 8px">{esc(r["genre_mood"])}</p>
<div class=kv2><span>Spotify</span><span>{link(r["spotify_profile"], r["spotify_profile"].replace("https://open.spotify.com/", ""))}</span>
<span>Instagram</span><span>{social_cell(r, "instagram")}</span><span>TikTok</span><span>{social_cell(r, "tiktok")}</span>
<span>Reach</span><span class=sm>{esc(r["reported_metrics"])}</span>
<span>Contact</span><span class=sm>{esc(r["public_submission_or_contact_link"])}</span>
<span>Evidence</span><span class=sm>{esc(r["verification_evidence_url"])}</span></div>
<span class="pill green" style="margin-top:10px">Confirmed</span></div>'''

style = STYLE.read_text()

page = f'''<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<meta name=robots content="noindex,nofollow">
<title>Playlist Curator Discovery &mdash; Keyman</title>
<meta property="og:title" content="Playlist Curator Discovery — Keyman">
<meta property="og:description" content="31 independent Spotify curators discovered from the kendallxcel and Brett Wolkey seeds · social accounts verified by link chain · Chartmetric metrics as reported · {DATE}">
<link rel=preconnect href="https://fonts.googleapis.com"><link rel=preconnect href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Manrope:wght@400;500;600;700&display=swap" rel=stylesheet>
{style}
<style>
.kpis{{grid-template-columns:repeat(5,1fr)}}
.kv2{{display:grid;grid-template-columns:90px 1fr;gap:4px 12px;font-size:13px}} .kv2>span:nth-child(odd){{color:var(--sub);font-weight:600}}
.grid2s{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:22px}}
#cur td{{font-size:12.5px}} #cur td:first-child{{min-width:190px}} #cur td:last-child{{min-width:260px;max-width:420px}}
.srcs{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px}}
.srcs .card{{padding:14px 16px}} .srcs .card b{{display:block;font-size:13px}} .srcs .card span{{font-size:12px;color:var(--sub)}}
@media(max-width:900px){{.grid2s,.srcs{{grid-template-columns:1fr}} .kpis{{grid-template-columns:repeat(2,1fr)}} .kpi:nth-child(2n+1){{border-left:0}} .kpi:nth-child(n+3){{border-top:1px solid var(--line)}}
 table.stack thead{{display:none}} table.stack tr{{display:block;border-bottom:1px solid var(--line);padding:10px 0}} table.stack td{{display:block;border:0;padding:4px 8px}} table.stack td:before{{content:attr(data-label);display:block;font:700 9px/1.3 "Manrope",sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--sub);margin-bottom:2px}}}}
</style></head><body>
<header class=hdr><div class="wrap top">
<div><div class=wm>KEYMAN</div><div class=wm-sub>Publishing Administration</div></div>
<div class=hdr-r>Playlist Curator Discovery<br><span class=badge>Draft &middot; {DATE} &middot; rev {REV}</span></div>
</div></header>
<main class=wrap>
<section class=panel style="display:block">
<div class=hero style="grid-template-columns:1fr">
<div><p class=eyebrow>Prepared by Keyman · internal working list</p>
<h1>Playlist Curator Discovery<small>Independent Spotify curators discovered from two seed profiles — kendallxcel (trap / underground rap / R&amp;B) and Brett Wolkey (TikTok-first, indie folk / rap) — with Instagram and TikTok accounts verified by link chain, not by matching usernames.</small></h1>
<div class=rule></div>
<p class=legal>Seeds: <b>open.spotify.com/user/kendallxw</b> and <b>open.spotify.com/user/31x2ckbqq74jdlw7losjtmipdahm</b> · Sources: signed-out Spotify web player, Instagram and TikTok bios, link-in-bio pages, PlaylistSupply, isitagoodplaylist, TikTok discover, Chartmetric (Hunter's account, browser session) · No Apify or paid scraping · No one was contacted and no music was submitted · Data as at {DATE}.</p>
</div></div>

<div class=finding><p>{len(rows)} unique curators, deduplicated by Spotify owner URL. {counts["confirmed"]} have a confirmed Instagram or TikTok account — a bio, link-in-bio page or playlist description that points at the same Spotify profile. {counts["probable"]} are probable (a curator-stated handle or a same-name account with no link back). {counts["none"]} are real Spotify curators with no public social account found; several expose an email or a paid submission link instead.</p>
<div class=n>Chartmetric ran through the existing browser login (plan badge "Free"); it supplied playlist and curator follower metrics for both seeds and one placement-sourced lead, but exposed no social links for either seed. Figures labelled "reported" are Chartmetric's or Spotify's own display values, not estimates.</div></div>

<div class=kpis>
<div class=kpi><div class=l>Unique curators</div><div class=v>{len(rows)}</div><div class=d>dedup by Spotify owner URL · 2 seeds + {len(others)} discoveries</div></div>
<div class=kpi><div class=l>Confirmed socials</div><div class=v style="color:var(--green)">{counts["confirmed"]}</div><div class=d>direct link chain to the Spotify profile</div></div>
<div class=kpi><div class=l>Probable</div><div class=v style="color:var(--amber)">{counts["probable"]}</div><div class=d>handle named by curator or name match only</div></div>
<div class=kpi><div class=l>No social found</div><div class=v style="color:var(--red)">{counts["none"]}</div><div class=d>Spotify curator confirmed; contact via email / paid form or none</div></div>
<div class=kpi><div class=l>Chartmetric-sourced</div><div class=v>1</div><div class=d>Tommy Craze via the Nine Vicious placement table · 2 seeds measured</div></div>
</div>

<h2 style="margin-top:44px">Seed curators</h2><div class=rule></div>
<div class=grid2s>{seed_cards}</div>

<h2 style="margin-top:44px">Curator candidates</h2><div class=rule></div>
<p class=sub>Confirmed first, then probable, then no-social. <b>Lane</b> is a judgment call from playlist names: Rap / R&amp;B follows kendallxcel, Indie / folk follows Brett Wolkey. Reach figures are reported values from Spotify, PlaylistSupply or Chartmetric on the date checked.</p>
<div class=tools><input type=search id=q placeholder="Search curator, genre or handle…" aria-label="Search">
<select class=f id=fs aria-label="Status"><option value="">All statuses</option><option value=confirmed>Confirmed</option><option value=probable>Probable</option><option value=none>No social found</option></select>
<select class=f id=fl aria-label="Lane"><option value="">All lanes</option><option>Rap / R&amp;B</option><option>Indie / folk</option><option>Both</option><option>Other</option></select></div>
<div class=count><b id=cnt>{len(others)}</b> of {len(others)} discovered curators shown</div>
<div class=tblwrap><table id=cur class=stack><thead><tr><th>Curator</th><th>Lane</th><th>Spotify</th><th>Instagram</th><th>TikTok</th><th>Status</th><th>Reach (reported)</th><th>Contact</th><th>Evidence · source</th></tr></thead>
<tbody>{table_rows(others)}</tbody></table></div>

<h2 style="margin-top:44px">Chartmetric: what the account actually exposed</h2><div class=rule></div>
<div class=grid2s>
<div class=card><h3>Access observed</h3><p class=sm>Logged in through the existing Chrome session as Hunter Sallis. Plan badge reads <b>Free</b> with "Upgrade to Ultra" prompts; no API key or client exists in this environment, so the API entitlement was not tested. The built-in browser hits the login wall.</p>
<p class=sm>Open and usable: global search → playlist pages (<b>Curated By</b> + Spotify link) → curator pages (About / Stats &amp; Trends / Playlists / Social / Audience); the <b>Curators</b> list (23,464,540 rows) with Link Availability, Genre and Curator Type filters and a CSV export icon; artist pages → Playlists tab (placement data).</p></div>
<div class=card><h3>Reported metrics</h3>
<div class=kv2><span>kendallxcel</span><span class=sm>curator 14477186 · total playlist followers 522,214 · curator followers 103,582 · 101 playlists · Trap Trackin (playlist 2433308) 23,991 followers, 393 tracks</span>
<span>Brett Wolkey</span><span class=sm>curator 24290612 · total playlist followers 43.9K · curator followers 12.5K · 19 playlists · Rap Cooks (playlist 16948557) 4.8K followers, stats last updated Jun 25 2024</span>
<span>Tommy Craze</span><span class=sm>DripDrop (playlist 1714884) 76K followers, 60 tracks, stats Oct 17 2026 · surfaced from the Nine Vicious placement table</span></div>
<p class=sm style="margin-top:10px">Curator social links appear only where Chartmetric has tied the curator to an artist entity (example: Stewart Harding, curator 1145499210, whose listed Instagram is dead). "Related Curators" on both seed pages returned platform brands (PlayStation, Spotify) — not useful for independent discovery.</p></div>
</div>

<h2 style="margin-top:44px">Coverage gaps</h2><div class=rule></div>
<ol class=find>
<li><b>Paywalled contacts.</b> PlaylistSupply masks curator email and Instagram; not bypassed. This is where cowpenguin1, Jeff Shelby, awills, Emillyy and Nj.terry's contacts most likely sit.</li>
<li><b>Fetch blocks.</b> WebFetch returned 403 for isitagoodplaylist, Instagram and TikTok (the browser was used instead); dripdrop.tv would not load; linktr.ee/theweisestband hides its destination URLs.</li>
<li><b>Dead or unrelated accounts.</b> Instagram "Profile isn't available" for @luxthugs, @indiespacerecords, @stewysongs, @nj.terry, @theweisestband; same-name accounts for awills, retrotones, theweisest and tommycraze are unrelated people.</li>
<li><b>Spotify rendering.</b> Brett Wolkey's profile shows no playlists signed-out; three PlaylistSupply-indexed playlists are deleted or private; "LATE NIGHT DRIVES" on Nj.terry's profile is owned by "AZ".</li>
<li><b>Chartmetric placement walk.</b> Only Nine Vicious was walked (editorial lists plus KANYE WEST BANGERS by "dog standing up", CLEAN RAP 2026 by DYNAMIX, DripDrop by Tommy Craze). B7!, Eli G, JaWill, Pz' and millkzy were not walked; "dog standing up" and DYNAMIX were not resolved.</li>
</ol>

<h2 style="margin-top:44px">What happens next</h2><div class=rule></div>
<ol class=plan>
<li><h3>Export the Chartmetric Curators list</h3><p>Marketing → Curators → filters: Curator Type = Independent + Popular Independent; Genre = Hip-Hop/Rap, then R&amp;B/Soul, then Alternative; Link Availability = Curators With Social Links → CSV export. Columns needed: Curator, Spotify URL, Playlists, Playlist Followers, Socials. That export is the only way to read Chartmetric's social links at scale.</p></li>
<li><h3>Export placement tables for representative artists</h3><p>Artist → Playlists → Spotify for Nine Vicious, B7!, Eli G, JaWill, Pz', millkzy (kendallxcel lane) and Noah Kahan-adjacent folk acts (Brett Wolkey lane). Keep the Curator column; drop editorial and platform-owned rows.</p></li>
<li><h3>Decide on PlaylistSupply reveal</h3><p>A membership would expose the masked email / Instagram fields for the {counts["none"]} no-social rows. Verify each reveal against the Spotify profile before use.</p></li>
<li><h3>Pick the pitch set</h3><p>Rap / R&amp;B lane: Nj.terry, awills, cowpenguin1, AfroDaPlug, Rap Gemz Daily, Skeud Rap, Sacha. Indie / folk lane: kasey's playlist, Fuegostine, zarasmixtapes, The Weisest Band, Ben Jammin, lienneay, Retro Tones. Paid-placement accounts (DripDrop, Indie Space Records, lienneay) are flagged in the Contact column.</p></li>
<li><h3>Re-check before outreach</h3><p>Follower counts and bios were read on {DATE}; recheck the Spotify profile and the social bio on the day of contact. Nothing on this page was sent to anyone.</p></li>
</ol>

<h2 style="margin-top:44px">Discovery sources</h2><div class=rule></div>
<div class=srcs>
<div class=card><b>Seed profiles</b><span>followed and co-owned playlists on kendallxcel's profile (Rap Gemz Daily, Nj.terry)</span></div>
<div class=card><b>PlaylistSupply</b><span>genre pages (trap, R&amp;B, hip-hop, neo-soul) and curator pages — playlist lists and follower counts; contacts masked</span></div>
<div class=card><b>isitagoodplaylist</b><span>curator pages with per-playlist genre tags (browser only)</span></div>
<div class=card><b>TikTok</b><span>/discover/playlist-curators and creator bios with bio links</span></div>
<div class=card><b>Articles</b><span>hellothematic.com TikTok-curator piece; Music Directory substack curator list</span></div>
<div class=card><b>Chartmetric</b><span>Curators list, curator and playlist pages, Nine Vicious placement table</span></div>
</div>
</section></main>
<footer><div class=wrap><div class=wm>KEYMAN</div><div class=wm-sub>Publishing Administration</div>
<p class=fs>Basis: public Spotify, Instagram, TikTok and link-in-bio pages read on {DATE}; PlaylistSupply and isitagoodplaylist indexes; Chartmetric data as displayed in Hunter Sallis's account. "Confirmed" means a curator-authored link or description ties the social account to the Spotify profile; "Probable" means the tie rests on a stated handle or a name match. Follower figures are the platforms' displayed values on the date checked. Internal working document — not for distribution.</p></div></footer>
<script>
const q=document.getElementById('q'),fs=document.getElementById('fs'),fl=document.getElementById('fl'),cnt=document.getElementById('cnt');
const trs=[...document.querySelectorAll('#cur tbody tr')];
function run(){{const s=q.value.trim().toLowerCase(),st=fs.value,ln=fl.value;let n=0;
 for(const tr of trs){{const ok=(!s||tr.dataset.q.includes(s))&&(!st||tr.dataset.status===st)&&(!ln||tr.dataset.lane===ln);tr.style.display=ok?'':'none';if(ok)n++;}}
 cnt.textContent=n;}}
q.addEventListener('input',run);fs.addEventListener('change',run);fl.addEventListener('change',run);
</script>
</body></html>'''
OUT.write_text(page, encoding="utf-8")
print(f"wrote {OUT} ({len(page):,} chars) · rows={len(rows)} · {counts}")
