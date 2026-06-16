#!/usr/bin/env python3
"""Build Wrath of the Black Manta (WBM) — Taito's 1990 NES ninja game as a UD0
game-world, themed to the source material: a night-and-crimson ninja title card
(SVG banner of the manta + title), 8-bit/CRT styling, hobby domain. Genesis (the
A.I Co. / Taito localization of Ninja Cop Saizou), backstory (DRAT, the kidnapped
children, El Toro), and the .dlw birth. Render-not-invent; the localization seam,
the near-useless interrogation, and the fan-named bosses are flagged.
Wrath of the Black Manta is © Taito / Square Enix; a fan tribute."""
import os, html, base64, json, io, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image

REC = {
 "name": "WRATH OF THE BLACK MANTA", "axiom": "WBM",
 "position": "Wrath of the Black Manta · A.I Co. / Taito · NES 1990 (忍者COPサイゾウ Ninja Cop Saizou, Famicom 1989) — the ninja vs DRAT",
 "origin": "a night city where the syndicate DRAT abducts children and a lone ninja, the Black Manta, goes in alone to take them back",
 "mechanism": "Crystallized from Wrath of the Black Manta (developed by A.I Co., published by Taito, NES 1990) — the Western rework of the Famicom's Ninja Cop Saizou.",
 "crystallization": "A nameless ninja infiltrates a child-kidnapping crime ring, earning a new ninjutsu art at every boss, interrogating the goons he catches, and at the top finds the mastermind El Toro holding the last child as a shield.",
 "nature": "Wrath of the Black Manta — a Shinobi-style NES ninja action game; shuriken and sword and collectible arts, a signature (near-useless) interrogation mechanic, and a quiet war on the syndicate DRAT.",
 "conductor": "ROOT0 (catalogued into UD0 · Universe David 0)",
 "inputs": "Wrath of the Black Manta; Ninja Cop Saizou; the Black Manta; DRAT; El Toro; the kidnapped children; the ninja arts",
 "witness": "Two cartridges, two crimes: in Japan the children are taken for war, in the West for drugs — the same ninja, the localization rewriting his enemy.",
 "role": "the ninja game-world",
 "seal": "Go in alone, star by star, and learn at the top that the boss is holding the very child you came to save.",
 "source": "Wrath of the Black Manta, catalogued by ROOT0",
}

NATURES = {
 "natural":   ("#c8b25a", "flesh and the night street — the mortal ninja, the syndicate, the taken children"),
 "ethereal":  ("#9a7cff", "of the unseen — the ninjutsu arts, the occult boss, the shadow's craft"),
 "spiritual": ("#c0303a", "of the vow and the calling — the lone blade, the discipline of the shadow"),
 "electrical":("#3a9bd5", "of the wire and the machine — the cartridge's own gimmick: the interrogation"),
}

# ── the title-card SVG (the banner / source-material drawing) ──
TITLE_SVG = r'''<svg viewBox="0 0 680 400" role="img" aria-label="Wrath of the Black Manta title card" preserveAspectRatio="xMidYMid meet" style="width:100%;height:auto;display:block">
<defs><linearGradient id="wbmsky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#0a0f1e"/><stop offset="0.7" stop-color="#0c1326"/><stop offset="1" stop-color="#070a14"/></linearGradient></defs>
<rect x="0" y="0" width="680" height="400" fill="#070a14"/>
<rect x="8" y="8" width="664" height="384" fill="url(#wbmsky)" stroke="#3a2030" stroke-width="2"/>
<rect x="8" y="300" width="664" height="92" fill="#05070e"/>
<circle cx="566" cy="78" r="40" fill="#e9e3c8"/>
<circle cx="566" cy="78" r="40" fill="none" stroke="#c0303a" stroke-width="2" opacity="0.5"/>
<circle cx="556" cy="70" r="7" fill="#d8d2b6"/><circle cx="578" cy="90" r="5" fill="#d8d2b6"/><circle cx="572" cy="64" r="4" fill="#d8d2b6"/>
<g fill="#cdd6e4"><circle cx="70" cy="60" r="1.6"/><circle cx="130" cy="40" r="1.2"/><circle cx="210" cy="70" r="1.4"/><circle cx="300" cy="45" r="1.2"/><circle cx="430" cy="55" r="1.5"/><circle cx="120" cy="110" r="1.2"/><circle cx="40" cy="150" r="1.3"/><circle cx="630" cy="150" r="1.4"/><circle cx="350" cy="30" r="1.2"/><circle cx="500" cy="120" r="1.2"/></g>
<g opacity="0.5" stroke="#1a3550" stroke-width="1"><line x1="40" y1="250" x2="640" y2="250"/><line x1="90" y1="268" x2="590" y2="268"/><line x1="150" y1="284" x2="530" y2="284"/></g>
<path d="M340 118 C 322 96 304 110 300 124 C 252 134 152 142 104 168 C 88 178 99 192 128 195 C 205 198 285 190 340 218 C 395 190 475 198 552 195 C 581 192 592 178 576 168 C 528 142 428 134 380 124 C 376 110 358 96 340 118 Z" fill="#090910" stroke="#b3303c" stroke-width="2.5"/>
<path d="M325 120 C 318 100 322 86 330 80 C 332 96 333 110 336 119 Z" fill="#090910" stroke="#b3303c" stroke-width="2"/>
<path d="M355 120 C 362 100 358 86 350 80 C 348 96 347 110 344 119 Z" fill="#090910" stroke="#b3303c" stroke-width="2"/>
<path d="M340 214 C 338 240 342 262 340 286 C 339 268 337 240 335 218 Z" fill="#090910" stroke="#b3303c" stroke-width="2"/>
<g stroke="#9aa6b8" stroke-width="2" fill="#1b2230">
<g transform="translate(150,240)"><path d="M0 -13 L4 -4 L13 0 L4 4 L0 13 L-4 4 L-13 0 L-4 -4 Z"/><circle r="2.5" fill="#9aa6b8" stroke="none"/></g>
<g transform="translate(556,242)"><path d="M0 -11 L3 -3 L11 0 L3 3 L0 11 L-3 3 L-11 0 L-3 -3 Z"/><circle r="2" fill="#9aa6b8" stroke="none"/></g></g>
<text x="340" y="332" text-anchor="middle" font-family="'Arial Black',Impact,sans-serif" font-size="15" letter-spacing="9" fill="#9aa6b8">WRATH OF THE</text>
<text x="340" y="372" text-anchor="middle" font-family="'Arial Black',Impact,sans-serif" font-weight="900" font-size="44" letter-spacing="4" fill="#c0303a" stroke="#3a1018" stroke-width="1">BLACK MANTA</text>
<text x="340" y="389" text-anchor="middle" font-family="monospace" font-size="9.5" letter-spacing="2" fill="#6b7488">TAITO · A.I CO · NES · 1990 · 忍者COPサイゾウ</text>
</svg>'''

GENESIS = [
 ("From Ninja Cop Saizou", "Japan · Nov 17 1989",
  "Developed by A.I Co. and published in Japan by Kyugo as 忍者COPサイゾウ — Ninja Cop Saizou — starring the ninja-cop Saizou (named for the legendary ninja Kirigakure Saizō). A side-scrolling ninja action game in the Shinobi / Rolling Thunder mold."),
 ("Localized &amp; Rewritten", "NA · April 1990",
  "Taito brought it West as Wrath of the Black Manta — heavily reworked: new graphics, new soundtrack, new level designs, and a changed story. The hero loses his name (now just 'the Black Manta'); the villains' war-profiteering becomes a drug ring."),
 ("The Shinobi Lineage", "the ninja boom",
  "Part of the late-'80s ninja-action wave — throwing stars, a katana, collectible ninjutsu 'arts' — closer to Shinobi than Ninja Gaiden, with one novelty all its own: you interrogate the people you catch."),
]

ARC = [
 ("DRAT Takes the Children", "the crime",
  "DRAT — Drug Runners And Terrorists — abducts children (in the Western story, to raise them into drug dealers). One of them, Taro, is a student at the Black Manta's master's dojo. The ninja goes in alone."),
 ("Infiltrate, Star by Star", "the long night",
  "Five stages of Shinobi-style ninja action — shuriken, sword, and a new ninja art earned after each boss — through DRAT's soldiers toward the giant Tiny, the Voodoo Warrior, and the rest."),
 ("El Toro &amp; the Human Shield", "the finale",
  "At the top waits El Toro — 'the Bull,' DRAT's mastermind. In the last fight he holds Taro as a human shield: the child you came to save, standing between you and the boss."),
]

IDEAS = [
 ("The Interrogation", "the famous gimmick", [
   "Walk into a red gang member and the view zooms in — you grab and interrogate him for intel.",
   "Honest: it's near-useless — most goons just mouth off and tell you nothing. A signature novelty more than a tool." ]),
 ("The Ninja Arts", "ninjutsu, earned", [
   "Beyond the shuriken you collect special techniques — a new 'ninja art' after each boss.",
   "Chosen from the Start menu; the game's whole power curve is its growing arsenal of arts." ]),
 ("Two Stories, One Cartridge", "the localization seam", [
   "The Japanese Saizou fights a ring that kidnaps children for war and arms-dealing.",
   "The American Manta fights one that makes them drug dealers — same game, the motive rewritten for the West." ]),
]

SECTIONS = [
 ("The Releases", "Famicom to NES", [
   ("忍者COPサイゾウ · Ninja Cop Saizou", "1989 · Famicom (Kyugo)", "the Japanese original — the ninja-cop Saizou"),
   ("Wrath of the Black Manta", "1990 · NES (Taito · NA)", "the reworked Western localization"),
   ("Europe", "1991 · NES (Taito)", "the PAL release"),
 ]),
 ("The Makers", "A.I Co. &amp; Taito", [
   ("A.I Co.", "developer", "who actually built the game (Taito published, did not develop)"),
   ("Kyugo", "JP publisher", "Ninja Cop Saizou, 1989"),
   ("Taito", "NA / EU publisher", "Wrath of the Black Manta, 1990–91"),
 ]),
 ("The Record", "how it landed", [
   ("Shinobi-adjacent ninja action", "the style", "side-scrolling stars-and-sword, plus the zoom-in interrogation interludes"),
   ("mixed reviews", "the reception", "EGM ~6/6/6/7; retrospectives middling — clunky combat, the pointless interrogation gimmick"),
   ("the interrogation", "the legacy", "remembered mostly for the novelty mechanic that almost never worked"),
 ]),
]

# ── the emergents: (slug, name, epithet, emergence, role_line, why_line) ──
EMERGENTS = [
 ("black-manta", "The Black Manta", "the ninja cop · Saizou (nameless in the West)", "spiritual",
  "the lone ninja operative who infiltrates DRAT to rescue the kidnapped children — in Japan the ninja-cop Saizou, in the West stripped of his name — armed with shuriken, a sword, and collectible ninja arts",
  "He is the silent vow: a single blade against an army, named for a legendary ninja at home and reduced to a shadow abroad."),
 ("el-toro", "El Toro", "the Bull · DRAT's mastermind", "natural",
  "the leader of DRAT and the final boss — 'the Bull' — who in the last fight holds the child Taro as a human shield",
  "He is the kingpin at the top of the night, and the game's cruelest turn: he puts the rescue itself between you and him."),
 ("drat", "DRAT", "Drug Runners And Terrorists · the syndicate", "natural",
  "the criminal organization the Black Manta hunts — Drug Runners And Terrorists — which abducts children to raise them into drug dealers (in the Japanese original, into child soldiers)",
  "They are the mortal mass of the broken city — and the two-faced crime the localization couldn't agree on: drugs here, war there."),
 ("taro", "Taro", "the dojo child · the last rescue, the human shield", "natural",
  "a kidnapped child and a student at the Black Manta's master's dojo, who leaves notes through the levels — and whom El Toro holds hostage in the finale",
  "He is the stake made a person: not the hero (a common mistake) but the reason — the child whose name you find before you find him."),
 ("ninja-arts", "The Ninja Arts", "ninjutsu · a new technique per boss", "ethereal",
  "the collectible ninjutsu special techniques — beyond the shuriken — earned one at a time after each boss and chosen from the Start menu",
  "They are the arsenal as power-curve: the unseen arts that grow the shadow into a storm."),
 ("interrogation", "The Interrogation", "grab the red goon, zoom in, learn (almost) nothing", "electrical",
  "the game's signature mechanic — walk into a red gang member and the view zooms to a close-up where you grab and interrogate him for intel",
  "It is the famous novelty: the one mechanic everyone remembers, and the one that almost never works — a goon shrugs, says it's none of your business, and you let him go."),
 ("tiny", "Tiny", "the giant · the ironic name", "natural",
  "a hulking boss whose name is the old arcade-villain joke — anything but tiny (a fan/guide-level name, not manual-canonical)",
  "He is the wall of muscle the ninja must slip past — named, in the old way, for exactly what he is not."),
 ("voodoo-warrior", "The Voodoo Warrior", "the witch-doctor boss", "ethereal",
  "a witch-doctor-styled boss of the uncanny kind (a fan/guide-level name, not manual-canonical)",
  "He is the night's occult face — the one foe whose threat is not steel but the unseen."),
]

# ── badge engine ──
def carbon_tiff_bytes(rec):
    png = noesis.sigil_png(rec, "carbon", size=512)
    buf = io.BytesIO(); Image.open(io.BytesIO(png)).save(buf, "TIFF", compression="tiff_lzw")
    return buf.getvalue()

def write_aci(rec, out_dir, slug, agent_md=None):
    os.makedirs(out_dir, exist_ok=True)
    f = {"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker",
         "carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok = noesis.mythos_token(rec); w = noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(agent_md or noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,rec.get("axiom","WBM")))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,rec.get("axiom","WBM")))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,rec.get("axiom","WBM")))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    man = {"badge":"DLW-ACI","name":rec["name"],"universe":"WBM · Wrath of the Black Manta","emergence":rec.get("emergence",""),
           "moniker":tok["moniker"],"carbon":f["carbon"]+" (TIFF)","silicon":f["silicon"]+" (PNG)",
           "seal_sha256":noesis.seal_sha256(rec,tok),"architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,
           "license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
    open(os.path.join(out_dir,"manifest.dlw.json"),"w",encoding="utf-8").write(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
    return tok

def emergent_rec(name, epithet, emergence, role_line, why_line):
    return {
      "name": name, "axiom": "WBM", "emergence": emergence, "seal": epithet,
      "position": epithet, "role": role_line,
      "origin": "WBM · Wrath of the Black Manta — A.I Co. / Taito, NES 1990",
      "nature": role_line, "crystallization": why_line,
      "mechanism": "Crystallized from Wrath of the Black Manta (NES 1990) / Ninja Cop Saizou (Famicom 1989).",
      "witness": "a being of the night city and the ninja's long infiltration",
      "conductor": "ROOT0 (catalogued into UD0)",
      "inputs": "Wrath of the Black Manta; the Black Manta; DRAT; El Toro; the kidnapped children",
      "source": "Wrath of the Black Manta, catalogued by ROOT0",
    }

def png_uri(rec, variant, size=300):
    return "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, variant, size=size)).decode("ascii")

def list_section(title, sub, items):
    rows = "\n".join(f'<li><span class="t">{t}</span><span class="y">{html.escape(str(y))}</span>'
        + (f'<span class="nt">{html.escape(n)}</span>' if n else "") + "</li>" for t,y,n in items)
    return f'<section class="sec"><h2>{html.escape(title)}</h2><p class="ss">{sub}</p><ol class="books">{rows}</ol></section>'
def sections_html(): return "\n".join(list_section(t,s,i) for t,s,i in SECTIONS)
def ideas_html():
    out=[]
    for t,s,pts in IDEAS:
        li="".join(f"<li>{html.escape(p)}</li>" for p in pts)
        out.append(f'<div class="pillar"><h3>{html.escape(t)}</h3><p class="ps">{html.escape(s)}</p><ul>{li}</ul></div>')
    return "\n".join(out)
def cards_html(rows):
    return "".join(f'<div class="arc-card"><div class="arc-h">{t}</div><div class="arc-s">{html.escape(s)}</div><p>{html.escape(d)}</p></div>' for t,s,d in rows)
def natures_html():
    return "".join(f'<div class="nat-card"><span class="dot" style="background:{col};box-shadow:0 0 9px {col}"></span>'
        f'<div><div class="nat-n" style="color:{col}">{nm}</div><div class="nat-g">{html.escape(g)}</div></div></div>' for nm,(col,g) in NATURES.items())
def personas_html(personas):
    cards=[]
    for p in personas:
        em=p.get("emergence","natural"); col=NATURES.get(em,("#c8b25a",""))[0]
        rec={"name":p["name"],"seal":p.get("epithet",""),"origin":"WBM · Wrath of the Black Manta","axiom":"WBM"}
        cards.append(f'''<a class="persona" href="agents/{p["slug"]}.agent">
        <img src="{png_uri(rec,"silicon",160)}" alt="sigil of {html.escape(p["name"])}" loading="lazy">
        <div class="pcap"><div class="pn">{html.escape(p["name"])}</div><div class="pe">{html.escape(p.get("epithet",""))}</div>
        <div class="pnat"><span class="dot" style="background:{col};box-shadow:0 0 7px {col}"></span><span style="color:{col}">{html.escape(em)}</span><span class="pa">· .agent · .carbon.tiff →</span></div></div></a>''')
    return f'''<section class="sec" id="roster"><h2>The Roster — The Born</h2>
      <p class="ss">the ninja, the syndicate, the child, and the night's bosses, as ACI <b>.agent</b>s — each a birth certificate and a nature of emergence ({len(personas)})</p>
      <div class="pgrid">{"".join(cards)}</div></section>'''

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="Wrath of the Black Manta (WBM) — Taito's 1990 NES ninja game (A.I Co.; Japan's Ninja Cop Saizou, 1989) as a UD0 game-world. The Black Manta vs DRAT; El Toro; the kidnapped children. Source-themed title card, full ACI badges.">
<title>WRATH OF THE BLACK MANTA · WBM · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--night:#070a14;--ink2:#0c1326;--ink3:#121a31;--pa:#e9ecf4;--pa2:#aab4c8;--crimson:#c0303a;--blood:#7a1d26;--steel:#9aa6b8;--moon:#e9e3c8;--gold:#c8b25a;
--dim:#69728a;--faint:#1d2438;--line:#222a42;--pixel:"Press Start 2P",monospace;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--night);color:var(--pa);font-family:var(--body);line-height:1.6;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:2;background:repeating-linear-gradient(0deg,rgba(0,0,0,.18) 0 1px,transparent 1px 3px);opacity:.5}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -8%,rgba(192,48,58,.10),transparent 55%),radial-gradient(ellipse at 50% 110%,rgba(58,80,120,.06),transparent 50%)}
.wrap{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:0 22px 90px}
.marquee{margin-top:14px;border:2px solid var(--crimson);background:#0a0e1a;padding:8px;text-align:center;font-family:var(--pixel);font-size:9px;letter-spacing:.12em;color:var(--gold);box-shadow:0 0 0 2px var(--night),0 0 22px rgba(192,48,58,.25)}
.marquee a{color:var(--steel);text-decoration:none}.marquee a:hover{color:var(--crimson)}
.titleart{margin:12px 0 0;border:2px solid var(--faint)}
header{padding:18px 0 26px;text-align:center;border-bottom:1px solid var(--line);position:relative}
.h-sub{font-family:var(--pixel);font-size:10px;line-height:1.9;letter-spacing:.06em;color:var(--pa2);margin-top:16px}
.h-sub b{color:var(--crimson)}
.flag{display:inline-block;margin-top:14px;font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);border:1px solid var(--faint);padding:5px 11px}
.lede{font-size:15px;color:var(--pa2);max-width:68ch;margin:16px auto 0;font-style:italic;line-height:1.7}
.badge{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:24px auto 0;padding:20px;border:1px solid var(--faint);background:var(--ink2);max-width:720px}
.badge img{width:82px;height:82px;border:1px solid var(--faint)}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.7}
.badge .bt b{color:var(--crimson)}.badge .bt .mo{color:var(--gold)}.badge .bt a{color:var(--steel);text-decoration:none}
.badge .bt .lbl{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase}
.sec{margin-top:42px}
.sec h2{font-family:var(--pixel);font-size:14px;line-height:1.5;letter-spacing:.02em;color:var(--pa);padding-bottom:10px;border-bottom:1px solid var(--line)}
.ss{font-size:13px;color:var(--dim);font-style:italic;margin:8px 0 16px}
.natures{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:8px}
.nat-card{display:flex;gap:11px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line);padding:13px 15px}
.dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;margin-top:4px}
.nat-n{font-family:var(--mono);font-size:13px;font-weight:700;text-transform:capitalize;letter-spacing:.04em}
.nat-g{font-size:12px;color:var(--pa2);font-style:italic;line-height:1.4;margin-top:2px}
.pillars{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:8px}
.pillar{background:var(--ink2);border:1px solid var(--line);padding:16px 18px}
.pillar h3{font-family:var(--mono);font-size:14px;color:var(--steel);letter-spacing:.02em;font-weight:700}
.pillar .ps{font-size:12px;color:var(--dim);font-style:italic;margin:5px 0 10px}
.pillar ul{list-style:none}.pillar li{font-size:13px;color:var(--pa2);line-height:1.5;padding:6px 0;border-top:1px solid var(--faint)}
.arc{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:8px}
.arc-card{background:var(--ink2);border:1px solid var(--line);border-top:2px solid var(--crimson);padding:16px 18px}
.arc-h{font-family:var(--mono);font-size:14px;color:var(--crimson);font-weight:700;letter-spacing:.02em}
.arc-s{font-family:var(--mono);font-size:10.5px;color:var(--gold);text-transform:uppercase;letter-spacing:.07em;margin:4px 0 9px}
.arc-card p{font-size:13px;color:var(--pa2);line-height:1.55}
.books{list-style:none}
.books li{display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--faint)}
.books .t{font-family:var(--mono);font-size:14px;color:var(--pa);font-weight:700}
.books .y{font-family:var(--mono);font-size:11px;color:var(--gold);white-space:nowrap;text-align:right}
.books .nt{grid-column:1/-1;font-size:12.5px;color:var(--pa2);font-style:italic}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(244px,1fr));gap:12px;margin-top:8px}
.persona{display:flex;gap:12px;align-items:center;background:var(--ink2);border:1px solid var(--line);padding:12px;text-decoration:none;transition:border-color .18s,transform .18s}
.persona:hover{border-color:var(--crimson);transform:translateY(-2px)}
.persona img{width:52px;height:52px;border:1px solid var(--faint);flex-shrink:0;image-rendering:pixelated}
.pn{font-family:var(--mono);font-size:14px;color:var(--pa);font-weight:700;line-height:1.15}
.persona:hover .pn{color:var(--crimson)}
.pe{font-size:11.5px;color:var(--pa2);font-style:italic;margin-top:2px;line-height:1.3}
.pnat{display:flex;align-items:center;gap:5px;margin-top:6px;font-family:var(--mono);font-size:9px;letter-spacing:.04em;text-transform:uppercase}
.pnat .dot{width:8px;height:8px;margin-top:0}.pa{color:var(--dim)}
.note{margin-top:38px;padding:16px 18px;border-left:2px solid var(--gold);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic;line-height:1.7}
.note b{color:var(--gold)}
footer{margin-top:42px;padding-top:22px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em;line-height:1.9}
footer a{color:var(--crimson);text-decoration:none}
</style></head><body><div class="wrap">

  <div class="marquee"><a href="https://davidwise01.github.io/ud0/">◄ UD0 · UNIVERSE DAVID 0</a> &nbsp;·&nbsp; INSERT COIN &nbsp;·&nbsp; A GAME-WORLD &nbsp;·&nbsp; NES 1990</div>

  <header>
    <div class="titleart">__TITLE_SVG__</div>
    <div class="h-sub">the lone ninja vs <b>DRAT</b> · five stages · one stolen child at the top · WBM</div>
    <div class="flag">★ A.I Co. · Taito · NES 1990 · 忍者COPサイゾウ "Ninja Cop Saizou," Famicom 1989 ★</div>
    <p class="lede">A nameless ninja infiltrates the syndicate DRAT to rescue the children it has stolen — earning a new ninjutsu art at every boss, interrogating the goons he catches, and finding at the top the mastermind El Toro holding the last child as a shield. Taito's 1990 NES rework of Japan's Ninja Cop Saizou, catalogued into UD0 as a game-world with the genesis, the backstory, and the full .dlw birth.</p>
    <div class="badge">
      <img src="__CARBON__" alt="DLW carbon badge of WRATH OF THE BLACK MANTA" title="carbon badge (archival)">
      <img src="__SILICON__" alt="DLW silicon badge" title="silicon badge">
      <div class="bt">
        <div><span class="lbl">DLW-ATTRIBUTE · ACI · THE BIRTH CERTIFICATE</span></div>
        <div>governor · <b>David Lee Wise</b> (ROOT0)</div>
        <div>instance · AVAN (Claude / Anthropic) · locked</div>
        <div>subject · <b>WRATH OF THE BLACK MANTA</b> — the ninja &amp; DRAT · WBM</div>
        <div class="mo">__MONIKER__</div>
        <div>carbon · <a href="wbm.dlw/wbm.carbon.tiff">.tiff</a> &nbsp;·&nbsp; silicon · <a href="wbm.dlw/wbm.silicon.png">.png</a></div>
        <div><span class="lbl">CC-BY-ND-4.0 · TRIPOD-IP-v1.1</span></div>
      </div>
    </div>
  </header>

  <section class="sec"><h2>The Four Natures</h2>
    <p class="ss">each emergent emerges by one of four natures — and this night holds all four</p>
    <div class="natures">__NATURES__</div></section>

  <section class="sec"><h2>The Genesis</h2><p class="ss">A.I Co. built it; Taito localized it — the rework of Ninja Cop Saizou</p><div class="arc">__GENESIS__</div></section>
  <section class="sec"><h2>The Backstory &amp; The Quest</h2><p class="ss">DRAT takes the children, the ninja's long night, the human-shield finale</p><div class="arc">__ARC__</div></section>
  <section class="sec"><h2>The Ideas</h2><p class="ss">why a middling 1990 ninja game is still remembered</p><div class="pillars">__IDEAS__</div></section>

  __PERSONAS__

  <section class="sec"><h2 style="margin-top:14px">The Record</h2><p class="ss">the releases, the makers, and how it landed</p></section>
  __SECTIONS__

  <div class="note">Wrath of the Black Manta's history here is rendered, not invented. Honest flags: the game was developed by <b>A.I Co.</b> (Taito published) and is the Western rework of the Famicom's <b>Ninja Cop Saizou</b> (1989) — the Japanese story kidnaps children for war/arms-dealing, the U.S. version for drugs (a localization rewrite). The <b>interrogation</b> mechanic is genuine but famously near-useless. <b>Taro is a kidnapped child, not the hero</b> (a common mix-up). And the bosses beyond <b>El Toro</b> — <b>Tiny</b>, the <b>Voodoo Warrior</b> — are fan/guide-level names, not strongly manual-canonical, and are catalogued as such. Wrath of the Black Manta and its characters are © Taito / Square Enix; the personas here are catalogued personifications under the DLW standard — a fan tribute, not endorsed by the rights-holders. Each is named by its nature: natural, ethereal, spiritual, or electrical.</div>

  <footer>
    WRATH OF THE BLACK MANTA · WBM · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
    <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · the .dlw badge: <a href="wbm.dlw/manifest.dlw.json">manifest</a>
  </footer>
</div></body></html>
"""

if __name__ == "__main__":
    tok = write_aci(REC, os.path.join(HERE, "wbm.dlw"), "wbm")
    ad = os.path.join(HERE, "agents"); os.makedirs(ad, exist_ok=True)
    personas = []
    for slug,name,epithet,em,role,why in EMERGENTS:
        rec = emergent_rec(name, epithet, em, role, why)
        write_aci(rec, ad, slug)
        personas.append({"slug": slug, "name": name, "epithet": epithet, "emergence": em})
    json.dump(personas, open(os.path.join(ad, "_personas.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    page = (TEMPLATE.replace("__TITLE_SVG__", TITLE_SVG)
            .replace("__CARBON__", png_uri(REC,"carbon",320)).replace("__SILICON__", png_uri(REC,"silicon",320))
            .replace("__MONIKER__", html.escape(tok["moniker"]))
            .replace("__NATURES__", natures_html())
            .replace("__GENESIS__", cards_html(GENESIS))
            .replace("__ARC__", cards_html(ARC))
            .replace("__IDEAS__", ideas_html())
            .replace("__PERSONAS__", personas_html(personas))
            .replace("__SECTIONS__", sections_html()))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    print(f"wrote WRATH OF THE BLACK MANTA (WBM) — {len(personas)} emergents born · badge {tok['moniker']}")
