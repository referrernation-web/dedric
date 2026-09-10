# -*- coding: utf-8 -*-
"""Dedric Brown — resume site. `python build.py` -> index.html (+ llms.txt, sitemap.xml, robots.txt).
Data source of truth: Downloads\\Dedric Resume 2026 (1).docx (Sept 2026).
Look (Mark, Sept 11): masontywong.com — warm peach room, white pill nav, clay 3D laptop that plays the intro, rounded everything."""
import pathlib, re, json, html as _h
HERE = pathlib.Path(__file__).parent
A = HERE / "assets"
BASE = "https://referrernation-web.github.io/dedric/"


def webp(p, maxw=1280, q=80):
    """assets/<p> -> assets/img/<stem>.webp, returns relative URL ('' if missing)."""
    from PIL import Image, ImageOps
    f = A / p
    if not f.exists():
        return ""
    out = A / "img"; out.mkdir(exist_ok=True)
    o = out / (f.stem + ".webp")
    if not o.exists() or o.stat().st_mtime < f.stat().st_mtime:
        im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
        if im.width > maxw:
            im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
        im.save(o, "WEBP", quality=q, method=6)
    return "assets/img/" + o.name


HEADSHOT = webp("headshot.jpg", 900, 82)
DREAMFORCE = webp("dreamforce.jpg", 1100, 78)
RENDER1 = webp("render1.jpg", 900, 78)
RENDER2 = webp("render2.jpg", 900, 78)
FRAME = webp("dedric-frame.jpg", 720, 80)          # clean still from the approved render (blazer + purple shirt)
INTRO = "video/intro.mp4" if (HERE / "video" / "intro.mp4").exists() else ""   # the application intro, once rendered and approved

# ---------------------------------------------------------------- data (docx)
NAME = "Dedric Brown"
EMAIL = "dedric.brown55@gmail.com"
PHONE = "470-262-7774"
LINKEDIN = "https://www.linkedin.com/in/dbrowntech"
TRAILBLAZER = "https://www.salesforce.com/trailblazer/dbrown6422"
CALENDLY = "https://calendly.com/dbrowntech15/30min"
PDF = "assets/Dedric-Brown-Resume-2026.pdf"

SUMMARY = ("Senior product and platform leader with 8+ years owning product vision, strategy, roadmaps and end-to-end delivery for enterprise "
           "Salesforce CRM, go-to-market systems, revenue operations, identity, healthcare and AI automation. I partner with executives across "
           "Sales, Marketing, Customer Success, Finance, Engineering, IT, Clinical Operations and Compliance to turn fragmented, manual processes "
           "into governed, automated platforms with measurable revenue impact.")

STATS = {
    "sales": [("150", "$", "M+", "annual pipeline on the Sales Cloud roadmap I owned at Cloudflare"),
              ("40", "", "%", "faster time-to-insight for Finance and Sales Ops, dashboards adopted by 12+ teams"),
              ("35", "", "%", "Salesforce adoption lift across the GTM user base"),
              ("15", "$", "M+", "enterprise contract value retained at Salesforce")],
    "health": [("27.6", "", "M", "members served by the managed-care org whose Health Cloud roadmap I own"),
               ("2", "", "", "AI workflows stopped before production for unresolved source-data issues"),
               ("1", "", "", "provider identity, NPI-keyed, reconciling three prescriber systems"),
               ("10", "", "-yr", "old call-logging environment being modernized into an operational CRM")],
}

EXPERTISE = [
    ("01", "Product Strategy &amp; Roadmap Ownership", "Vision, portfolio intake, business cases, prioritization, acceptance criteria, release plans and post-launch measurement across enterprise Salesforce ecosystems."),
    ("02", "CRM &amp; ERP Systems Integration", "Salesforce to NetSuite across opportunity-to-order, order-to-cash, billing, invoicing and revenue recognition. External IDs, master data, deduplication, one system of record."),
    ("03", "GTM &amp; Revenue Operations", "Lead-to-opportunity, pipeline management, forecasting, marketing automation, renewals and retention, KPI definition and dashboards Finance actually adopts."),
    ("04", "Agentforce &amp; AI Automation", "Agentforce and Einstein use cases with process mapping, data-readiness gates, human-in-the-loop controls and AI governance in HIPAA-regulated workflows."),
]

CAREER = [
    ("Jan 2026 – Present", "Centene Corporation", "Senior Salesforce Product Manager", "Atlanta, GA",
     "Fortune 500 managed care organization serving 27.6M members. Owns the Salesforce Health Cloud roadmap for specialty pharmacy and managed care with IT, Clinical Operations and Compliance.",
     ["Lead discovery and future-state process design to modernize a 10-year-old call-logging environment into an operational Salesforce CRM: lead-to-opportunity workflows, stage-exit criteria, requirements, forecasting dashboards for member and referral volume.",
      "Own the AI product roadmap for prior authorization, benefits investigation and referral-to-therapy; apply process mapping, data-readiness, governance and human-in-the-loop criteria to Agentforce and Einstein use cases, preventing two workflows with unresolved source-data issues from entering production.",
      "Built the governance backbone the roadmap depends on: standardized provider and member data models plus NPI-keyed external IDs reconciling ScriptMed (Inovalon), Centene prescriber and Symphony Health into one provider identity.",
      "Lead portfolio intake, stakeholder alignment and roadmap prioritization; translate business and regulatory needs into requirements, acceptance criteria, release plans and audit-ready controls for HIPAA workflows."],
     ["Health Cloud", "Agentforce", "Einstein", "HIPAA", "Data governance"]),
    ("Apr 2023 – Jan 2026", "Cloudflare", "Product Manager, GTM Business Systems", "Atlanta, GA",
     "$2.17B FY2025 revenue, roughly 332K paying customers. Owned the Sales Cloud roadmap supporting $150M+ in annual pipeline and directed a developer team on a SAFe Program Increment cadence.",
     ["Reduced reporting time-to-insight 40% for Finance and Sales Operations by replacing manual data pulls with KPI dashboards and forecast reporting adopted by 12+ teams.",
      "Led end-to-end delivery of the Salesforce-to-NetSuite ERP integration across opportunity-to-order, order-to-cash, billing, invoicing and revenue recognition, creating a reconciled system of record and reducing manual handoffs at month-end close.",
      "Increased Salesforce platform adoption 35% across the GTM user base by prioritizing automation on product analytics and business value during PI planning, paired with change management and role-based enablement.",
      "Reduced post-launch defects 20% and accelerated feature delivery 15% by strengthening discovery, backlog refinement, sprint planning, acceptance criteria, UAT and release readiness."],
     ["Sales Cloud", "NetSuite ERP", "SAFe", "Forecasting", "RevOps"]),
    ("Jun 2021 – Apr 2023", "Salesforce", "Product Manager, Customer Platforms", "Atlanta, GA",
     "Vlocity / OmniStudio and Marketing Cloud roadmap for health insurance and commercial partner accounts holding $15M+ in contract value and a $10M+ upsell and renewal book.",
     ["Retained $15M+ in enterprise contract value by resequencing the roadmap around what health insurance and commercial partners were escalating, then holding internal stakeholders to that order through delivery.",
      "Grew lead generation 35% and customer retention 20% by running Marketing Cloud go-to-market campaigns re-cut against performance data rather than the launch calendar.",
      "Scaled Vlocity / OmniStudio enablement across the partner base, lifting adoption inside the $10M+ renewal book.",
      "Prioritized enhancements from customer feedback and user research against defined success metrics, moving adoption 15% and user satisfaction to 95%."],
     ["OmniStudio", "Marketing Cloud", "Enablement", "Renewals"]),
    ("Jan 2020 – Jun 2021", "Salesforce", "Product Manager, Identity &amp; Security", "Atlanta, GA",
     "Enterprise identity and access management program: SSO and MFA across 8,000+ users supporting $25M+ in regulated enterprise contracts.",
     ["Cut access-related incidents 40% by standing up enterprise IAM frameworks and business rules and taking SSO/MFA adoption to the full 8,000-user base.",
      "Closed 10+ critical security findings by integrating IAM with existing security infrastructure, and standardized access processes across regulated environments so compliance and audit had one story to review."],
     ["IAM", "SSO / MFA", "Compliance", "Audit"]),
    ("Jan 2018 – Jan 2020", "NCR Corporation", "Product Manager, CRM Platforms", "Atlanta, GA",
     "Sales Cloud modernization for an enterprise sales org carrying $20M+ in contracts and 2M+ legacy CRM records.",
     ["Delivered $1.8M+ in operating cost savings by automating onboarding and internal Salesforce workflows; migrated 2M+ legacy CRM records with zero downtime and improved data accuracy 35%.",
      "Redesigned Sales Cloud lead and opportunity workflows, reducing sales-cycle time 15%, increasing lead conversion 10% and lowering Salesforce support tickets 30%."],
     ["Sales Cloud", "Migration", "Automation"]),
]

CASES = [
    ("ERP INTEGRATION", "One system of record from quote to cash", "Cloudflare",
     "Opportunity, order, billing and revenue recognition lived in two systems that never agreed. Month-end close ran on manual handoffs.",
     "Owned the Salesforce-to-NetSuite integration end to end: opportunity-to-order, order-to-cash, billing, invoicing, revenue recognition. Defined the external IDs and reconciliation rules first, then the roadmap.",
     "A reconciled system of record, fewer manual handoffs at close, and KPI dashboards Finance adopted across 12+ teams (time-to-insight down 40%).",
     ["Sales Cloud", "NetSuite", "External IDs", "Rev rec"]),
    ("AI GOVERNANCE", "Agentforce that clears a HIPAA gate", "Centene",
     "Prior authorization, benefits investigation and referral-to-therapy were the obvious AI targets, but the source data behind two of them could not be trusted yet.",
     "Built the readiness path before the use case: process mapping, data-readiness scoring, human-in-the-loop controls and audit-ready governance criteria that every Agentforce or Einstein workflow has to pass.",
     "Two workflows held back from production until the data was fixed; the ones that shipped carry controls Compliance can review.",
     ["Agentforce", "Einstein", "Health Cloud", "HIPAA"]),
    ("PROVIDER IDENTITY", "Three prescriber systems, one provider", "Centene",
     "ScriptMed (Inovalon), the Centene prescriber file and Symphony Health each described the same provider differently. Every downstream dashboard inherited the disagreement.",
     "Standardized the provider and member data models and keyed external IDs on the National Provider Identifier so the three sources reconcile into one identity.",
     "One provider identity the roadmap can build on, and the governance backbone for the CRM modernization.",
     ["Master data", "NPI", "Deduplication", "Governance"]),
    ("IDENTITY &amp; ACCESS", "SSO and MFA for 8,000 users", "Salesforce",
     "Access-related incidents kept landing on regulated contracts worth $25M+, and every audit told a different story about who could reach what.",
     "Stood up enterprise IAM frameworks and business rules, integrated IAM with the existing security stack and drove SSO/MFA adoption across the full user base.",
     "Access-related incidents down 40%, 10+ critical findings closed, and one access story for compliance and audit.",
     ["IAM", "SSO", "MFA", "Zero trust"]),
]

# Approved talks (Dedric signed off): kept small, framed as speaking / side project, not as his job
REELS = [
    ("whytech1", "Why Tech, Part 1", "video/whytech1.mp4", webp("thumb-whytech1.jpg", 540, 72)),
    ("whytech2", "Why Tech, Part 2", "video/whytech2.mp4", webp("thumb-whytech2.jpg", 540, 72)),
    ("whytech3", "Why Tech, Part 3", "video/whytech3.mp4", webp("thumb-whytech3.jpg", 540, 72)),
    ("whytech4", "Why Tech, Part 4", "video/whytech4.mp4", webp("thumb-whytech4.jpg", 540, 72)),
    ("whytech5", "Why Tech, Part 5", "video/whytech5.mp4", webp("thumb-whytech5.jpg", 540, 72)),
    ("topic01", "Entry-Level Now Means You", "video/topic01.mp4", webp("thumb-topic01.jpg", 540, 72)),
]

CERTS = [
    ("SALESFORCE", "Agentforce Specialist", "formerly AI Specialist · Oct 2024"),
    ("SALESFORCE", "AI Associate", "Oct 2024"),
    ("SALESFORCE", "Agentforce Sales Consultant", "formerly Sales Cloud Consultant · Apr 2023"),
    ("SALESFORCE", "Platform Strategy Designer", "formerly Strategy Designer · Apr 2023"),
    ("SALESFORCE", "Business Analyst", "Jan 2023"),
    ("SALESFORCE", "Platform Administrator II", "formerly Advanced Administrator · Sep 2022"),
    ("SALESFORCE", "Platform Foundations", "formerly Salesforce Associate · Sep 2022"),
    ("SALESFORCE", "Agentforce Service Consultant", "formerly Service Cloud Consultant · Dec 2021"),
    ("SALESFORCE", "Platform Administrator", "formerly Administrator · Oct 2020"),
    ("SCALED AGILE", "SAFe 6 Product Owner / Product Manager", "Jun 2024"),
    ("SCRUM ALLIANCE", "Certified ScrumMaster (CSM)", "Jan 2023"),
    ("GOOGLE", "Google AI Essentials", "Coursera · Jun 2026"),
    ("COMPTIA", "Security+", "CompTIA"),
    ("TRAILHEAD", "Security Specialist Superbadge", "Salesforce Trailhead"),
]

SKILLS = [
    ("Salesforce &amp; Enterprise Platforms", ["Sales Cloud", "Service Cloud", "Health Cloud", "Marketing Cloud", "OmniStudio / Vlocity", "Agentforce", "Einstein", "Flow Builder", "NetSuite ERP", "APIs &amp; integration"]),
    ("Agentic AI &amp; Automation", ["Agentforce solution design", "Einstein predictive models", "LLMs &amp; prompt design", "Anthropic Claude API", "AI readiness assessment", "Human-in-the-loop", "Responsible AI"]),
    ("Product Leadership", ["Vision &amp; strategy", "Roadmap ownership", "Business cases", "Discovery", "User research", "Backlog prioritization", "Sprint planning", "UAT &amp; release", "Change management"]),
    ("GTM, RevOps &amp; Analytics", ["Lead-to-opportunity", "Order-to-cash", "Forecasting", "Marketing automation", "Renewals &amp; retention", "KPI definition", "Dashboards", "Revenue recognition"]),
    ("Security, Healthcare &amp; Compliance", ["IAM · SSO · MFA", "HIPAA", "Audit readiness", "Managed care", "Specialty pharmacy", "Prior authorization", "Provider &amp; member data"]),
]


# ---------------------------------------------------------------- html pieces
def esc(s): return _h.escape(s, quote=True)


def stats_html(key):
    return "".join(
        f'<div class="stat"><b data-count="{n}" data-prefix="{pre}" data-suffix="{suf}">{pre}{n}{suf}</b><span>{d}</span></div>'
        for n, pre, suf, d in STATS[key])


expertise_html = "".join(f'<article class="pillar rv"><span class="xnum">{n}</span><h3>{t}</h3><p>{d}</p></article>' for n, t, d in EXPERTISE)

career_html = ""
for i, (when, co, role, loc, ctx, bullets, chips) in enumerate(CAREER):
    career_html += (f'<article class="node rv" id="role{i}"><div class="port in"></div><div class="port out"></div>'
                    f'<header><span class="mono">{when}</span><h3>{role}</h3><div class="co">{co} <span>· {loc}</span></div></header>'
                    f'<p class="ctx">{ctx}</p><ul>' + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"
                    f'<div class="chips">' + "".join(f"<span>{c}</span>" for c in chips) + "</div></article>")

cases_html = "".join(
    f'<article class="case rv"><span class="mono acc">{cat}</span><h3>{t}</h3><small>{co}</small>'
    f'<dl><dt>Problem</dt><dd>{p}</dd><dt>What I did</dt><dd>{d}</dd><dt>Result</dt><dd>{r}</dd></dl>'
    f'<div class="chips">' + "".join(f"<span>{c}</span>" for c in chips) + "</div></article>"
    for cat, t, co, p, d, r, chips in CASES)

reels_html = "".join(
    f'<button class="reel rv" data-src="{src}" data-title="{esc(t)}" type="button"><img src="{poster}" alt="{esc(t)}" loading="lazy" decoding="async" width="540" height="960"><span class="play">&#9654;</span><b>{t}</b></button>'
    for k, t, src, poster in REELS)

certs_html = "".join(
    f'<div class="flip rv"><div class="finner"><div class="fface ffront"><span class="chip">{chip}</span><h4>{t}</h4><small>{d}</small></div>'
    f'<div class="fface fback"><small class="mono">VERIFY</small><h4>{t}</h4><a href="{TRAILBLAZER if chip in ("SALESFORCE", "TRAILHEAD") else LINKEDIN}" target="_blank" rel="noopener">{"Trailblazer profile" if chip in ("SALESFORCE", "TRAILHEAD") else "LinkedIn"} &#8599;</a></div></div></div>'
    for chip, t, d in CERTS)

skills_html = "".join(f'<div class="sgroup rv"><h3>{g}</h3><div class="chips">' + "".join(f"<span>{s}</span>" for s in items) + "</div></div>" for g, items in SKILLS)

JSONLD = json.dumps({
    "@context": "https://schema.org", "@type": "Person", "@id": BASE + "#person",
    "name": "Dedric Brown", "jobTitle": "Senior Salesforce Product Manager", "url": BASE,
    "email": "mailto:" + EMAIL, "telephone": "+1-" + PHONE,
    "address": {"@type": "PostalAddress", "addressLocality": "Atlanta", "addressRegion": "GA", "addressCountry": "US"},
    "sameAs": [LINKEDIN, TRAILBLAZER, "https://thededricbrown.com/"],
    "worksFor": {"@type": "Organization", "name": "Centene Corporation"},
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "Morris Brown College"},
    "knowsAbout": ["Salesforce", "Sales Cloud", "Health Cloud", "Agentforce", "Revenue Operations", "Product Management", "NetSuite", "IAM"],
    "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": c[1], "credentialCategory": "certification"} for c in CERTS],
}, ensure_ascii=False)

# laptop screen: the intro video when it exists, otherwise the approved still
SCREEN = (f'<video id="reel" src="{INTRO}" poster="{FRAME}" muted autoplay loop playsinline preload="metadata"></video>' if INTRO
          else f'<img id="reel" src="{FRAME}" alt="Dedric Brown" width="720" height="720"><span class="soon">INTRO VIDEO &middot; IN PRODUCTION</span>')

# ---------------------------------------------------------------- css (masontywong.com treatment: peach room, clay, pills)
CSS = r"""
:root{--bg:#f1dcc7;--bg2:#e6c8ad;--wall:#f6e4d3;--card:#fff8f1;--ink:#4f453f;--ink2:#62564f;--mut:#8f8078;--line:rgba(79,69,63,.12);--clay:#e9a878;--clay2:#f3c39b;--dark:#4f453f;--holo:linear-gradient(120deg,#ffb27a,#ffd08a 30%,#c9a2ff 60%,#8fd3ff)}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font:400 16px/1.65 'Plus Jakarta Sans',ui-sans-serif,system-ui,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.55;background:repeating-linear-gradient(90deg,var(--wall) 0 84px,var(--bg) 84px 96px)}
body::after{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;background:radial-gradient(1200px 500px at 50% 110%,rgba(79,69,63,.18),transparent 60%)}
a{color:inherit;text-decoration:none}
img{max-width:100%;display:block}
.wrap{position:relative;z-index:1;max-width:1180px;margin:0 auto;padding:0 28px}
.mono{font:700 11px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--mut)}
.acc{background:var(--holo);-webkit-background-clip:text;background-clip:text;color:transparent}
h1,h2,h3{font-family:'Bricolage Grotesque','Plus Jakarta Sans',sans-serif;letter-spacing:-.02em;line-height:1.05;text-wrap:balance;color:var(--ink)}
h2{font-size:clamp(32px,4.4vw,52px);font-weight:800;margin:10px 0 14px}
section{position:relative;padding:96px 0}
.shead{max-width:720px;margin-bottom:44px}.shead p{color:var(--ink2);font-size:17px}
.shead.center{margin:0 auto 44px;text-align:center}
.btn{display:inline-flex;align-items:center;gap:10px;padding:14px 22px;border-radius:99px;font-weight:700;font-size:15px;border:1px solid rgba(255,255,255,.7);background:#fff;color:var(--ink);cursor:pointer;box-shadow:0 10px 24px rgba(79,69,63,.14),inset 0 -3px 0 rgba(79,69,63,.06);transition:transform .2s,box-shadow .2s}
.btn:hover{transform:translateY(-2px);box-shadow:0 16px 30px rgba(79,69,63,.18)}
.btn.dark{background:var(--dark);color:#fff;border-color:var(--dark)}
.btn.holo{position:relative;background:#fff;isolation:isolate}.btn.holo::before{content:"";position:absolute;inset:-2px;border-radius:inherit;background:var(--holo);z-index:-1;opacity:.9}
.btn:focus-visible,button:focus-visible,a:focus-visible{outline:3px solid #8fd3ff;outline-offset:2px}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chips span{font:600 12px/1 'Plus Jakarta Sans',sans-serif;padding:8px 11px;border-radius:99px;background:#fff;color:var(--ink2);box-shadow:0 3px 8px rgba(79,69,63,.08)}
/* clay cards */
.clay{background:var(--card);border-radius:28px;box-shadow:0 18px 40px rgba(79,69,63,.14),inset 0 -8px 16px rgba(79,69,63,.06),inset 0 3px 6px #fff;border:1px solid rgba(255,255,255,.8)}
/* floating pill nav (Mason Wong) */
nav.top{position:fixed;top:18px;left:18px;z-index:50;display:flex;align-items:center;gap:6px;padding:6px;border-radius:99px;background:#fff;box-shadow:0 14px 34px rgba(79,69,63,.18)}
nav.top .logo{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:22px;letter-spacing:-.04em;padding:0 12px 0 14px}
nav.top a.pl{padding:10px 16px;border-radius:99px;font-weight:600;font-size:15px;color:var(--ink);transition:background .2s}
nav.top a.pl:hover,nav.top a.pl.on{background:#f0ebe6}
nav.top a.w{background:var(--dark);color:#fff}
.dock{position:fixed;top:18px;right:18px;z-index:50;display:flex;gap:6px;padding:6px;border-radius:99px;background:#fff;box-shadow:0 14px 34px rgba(79,69,63,.18)}
.dock a{padding:10px 14px;border-radius:99px;font-weight:700;font-size:13px;color:var(--ink)}.dock a:hover{background:#f0ebe6}.dock a.l{background:var(--dark);color:#fff}
@media(max-width:900px){nav.top a.pl{display:none}.dock{top:auto;bottom:16px;right:50%;transform:translateX(50%)}}
/* hero: the room */
.hero{min-height:100svh;display:grid;grid-template-columns:1fr 1.05fr;gap:40px;align-items:center;padding:120px 0 60px}
.hero .kicker{display:inline-flex;align-items:center;gap:10px;font:700 12px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--ink2);margin-bottom:22px;padding:8px 14px;border-radius:99px;background:#fff;box-shadow:0 6px 16px rgba(79,69,63,.1)}
.hero .kicker i{width:8px;height:8px;border-radius:50%;background:#3fb96a}
.hero h1{font-size:clamp(40px,5.2vw,72px);font-weight:800}
.hero h1 em{font-style:normal;background:var(--holo);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero .sub{color:var(--ink2);font-size:18px;max-width:56ch;margin:22px 0 28px}
.hero .cta{display:flex;flex-wrap:wrap;gap:12px}
/* the clay laptop that plays the intro */
.scene{position:relative;perspective:1400px;justify-self:center;width:min(560px,100%);aspect-ratio:1.1}
.desk{position:absolute;left:-6%;right:-6%;bottom:2%;height:34%;border-radius:50%;background:radial-gradient(ellipse at 50% 40%,#f6e6d8,#e7cbb3 70%,transparent 72%);filter:blur(.5px)}
.laptop{position:absolute;left:8%;right:8%;bottom:14%;transform:rotateX(58deg) rotateZ(-14deg);transform-style:preserve-3d;transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.scene:hover .laptop{transform:rotateX(54deg) rotateZ(-10deg)}
.base{height:150px;border-radius:22px;background:linear-gradient(180deg,#f3c29a,#e9a878);box-shadow:0 30px 50px rgba(79,69,63,.35),inset 0 -10px 18px rgba(0,0,0,.08),inset 0 4px 8px rgba(255,255,255,.5);position:relative}
.base .pad{position:absolute;left:50%;top:18%;width:32%;height:44%;transform:translateX(-50%);border-radius:14px;background:linear-gradient(180deg,#e39e6c,#d99461);box-shadow:inset 0 3px 8px rgba(0,0,0,.14)}
.base .keys{position:absolute;left:10%;right:10%;top:68%;height:16%;border-radius:10px;background:repeating-linear-gradient(90deg,#e39e6c 0 6%,transparent 6% 8%);opacity:.5}
.lid{position:absolute;left:0;right:0;bottom:100%;height:340px;transform-origin:50% 100%;transform:rotateX(-96deg);border-radius:22px 22px 8px 8px;background:linear-gradient(180deg,#f3c29a,#e9a878);padding:14px 14px 22px;box-shadow:0 12px 30px rgba(79,69,63,.25),inset 0 4px 8px rgba(255,255,255,.5)}
.screen{position:relative;width:100%;height:100%;border-radius:12px;overflow:hidden;background:#221a16}
.screen video,.screen img{width:100%;height:100%;object-fit:cover;object-position:50% 20%}
.screen .soon{position:absolute;left:12px;bottom:12px;padding:7px 10px;border-radius:99px;background:rgba(255,255,255,.9);color:var(--ink);font:800 10px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.14em}
.unmute{position:absolute;left:50%;bottom:0;transform:translateX(-50%);padding:11px 16px;border-radius:99px;border:0;background:var(--dark);color:#fff;font:800 12px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.1em;cursor:pointer;box-shadow:0 10px 24px rgba(79,69,63,.25)}
.mug{position:absolute;right:2%;bottom:16%;width:70px;height:60px;border-radius:12px 12px 20px 20px;background:linear-gradient(180deg,#fff,#efe3d8);box-shadow:0 14px 24px rgba(79,69,63,.25)}
.mug::after{content:"";position:absolute;right:-18px;top:14px;width:22px;height:26px;border:8px solid #f4ebe3;border-left:0;border-radius:0 14px 14px 0}
.steam{position:absolute;right:5%;bottom:30%;width:30px;height:34px;color:#fff;font-size:28px;line-height:1;opacity:.8;animation:steam 3s ease-in-out infinite}
@keyframes steam{50%{transform:translateY(-6px);opacity:.4}}
/* the switch */
.switch{display:inline-flex;align-items:center;gap:12px;margin:34px 0 14px;font:700 12px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.switch button{position:relative;width:58px;height:30px;border-radius:99px;border:0;background:#fff;box-shadow:inset 0 2px 6px rgba(79,69,63,.15);cursor:pointer}
.switch button i{position:absolute;top:3px;left:3px;width:24px;height:24px;border-radius:50%;background:var(--holo);transition:left .25s cubic-bezier(.2,.8,.2,1)}
.switch.on button i{left:31px}
.switch.on .b,.switch:not(.on) .a{color:var(--ink)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.stat{padding:16px 16px 14px;border-radius:22px;min-height:112px;display:flex;flex-direction:column;justify-content:space-between}
.stat b{font-family:'Bricolage Grotesque',sans-serif;font-size:30px;font-weight:800;letter-spacing:-.03em;color:var(--ink);font-variant-numeric:tabular-nums}
.stat span{font-size:12px;color:var(--mut);line-height:1.35}
#stats{transition:opacity .25s}#stats.fade{opacity:0}
@media(max-width:980px){.hero{grid-template-columns:1fr;gap:34px;padding-top:110px}.scene{width:min(440px,100%)}.stats{grid-template-columns:repeat(2,1fr)}.lid{height:260px}.base{height:110px}}
/* proof band */
.proofband{position:relative;z-index:1;background:var(--dark);color:#fff;overflow:hidden;padding:14px 0}
.mq{display:flex;gap:44px;width:max-content;animation:sc 48s linear infinite}.proofband:hover .mq{animation-play-state:paused}
.pf{display:inline-flex;align-items:baseline;gap:10px;font:600 12px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.04em;white-space:nowrap;color:rgba(255,255,255,.8)}.pf b{font:800 20px/1 'Bricolage Grotesque',sans-serif;letter-spacing:-.02em;color:#fff}
@keyframes sc{to{transform:translateX(-50%)}}
/* about */
.about{display:grid;grid-template-columns:.9fr 1.1fr;gap:54px;align-items:center}
.photo{position:relative;overflow:hidden;border-radius:32px}
.photo img{aspect-ratio:4/5;object-fit:cover;width:100%}
.photo .badge{position:absolute;left:16px;bottom:16px;display:inline-flex;align-items:center;gap:8px;padding:9px 14px;border-radius:99px;background:#fff;font:800 11px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.1em;box-shadow:0 8px 20px rgba(79,69,63,.2)}
.photo .badge i{width:8px;height:8px;border-radius:50%;background:#3fb96a}
.about p{color:var(--ink2);font-size:17px;margin-bottom:16px}
.gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:22px}.gallery img{aspect-ratio:1;object-fit:cover;border-radius:18px;box-shadow:0 8px 18px rgba(79,69,63,.14)}
@media(max-width:900px){.about{grid-template-columns:1fr}}
/* expertise */
.pillars{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.pillar{position:relative;padding:26px 22px 24px;transition:transform .25s}
.pillar:hover{transform:translateY(-4px)}
.pillar .xnum{font:800 12px/1 'Plus Jakarta Sans',sans-serif;color:var(--mut);letter-spacing:.14em}
.pillar h3{font-size:19px;margin:14px 0 10px}.pillar p{color:var(--ink2);font-size:14px}
@media(max-width:980px){.pillars{grid-template-columns:repeat(2,1fr)}}@media(max-width:560px){.pillars{grid-template-columns:1fr}}
/* career canvas */
.canvas{position:relative}
.flow{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
.flow path{fill:none;stroke:var(--clay);stroke-width:3;stroke-dasharray:6 8;opacity:.9;animation:dash 14s linear infinite}
@keyframes dash{to{stroke-dashoffset:-400}}
.nodes{position:relative;display:grid;gap:34px;max-width:860px;margin:0 auto}
.node{position:relative;padding:26px 28px}
.node:nth-child(odd){margin-right:80px}.node:nth-child(even){margin-left:80px}
.node .port{position:absolute;left:50%;width:14px;height:14px;border-radius:50%;background:#fff;border:3px solid var(--clay);transform:translateX(-50%)}
.node .port.in{top:-8px}.node .port.out{bottom:-8px}
.node:first-child .port.in,.node:last-child .port.out{display:none}
.node h3{font-size:22px;margin:8px 0 4px}.node .co{font-weight:700;color:var(--ink)}.node .co span{font-weight:500;color:var(--mut)}
.node .ctx{color:var(--ink2);font-size:15px;margin:12px 0}
.node ul{padding-left:18px;color:var(--ink2);font-size:14.5px;display:grid;gap:8px;margin-bottom:16px}.node li::marker{color:var(--clay)}
@media(max-width:700px){.node:nth-child(odd),.node:nth-child(even){margin:0}}
/* cases */
.cases{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.case{padding:26px}
.case h3{font-size:22px;margin:10px 0 4px}.case small{color:var(--mut)}
.case dl{margin:18px 0 16px;display:grid;gap:10px}.case dt{font:800 11px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.14em;color:var(--mut)}.case dd{color:var(--ink2);font-size:14.5px}
@media(max-width:800px){.cases{grid-template-columns:1fr}}
/* certs */
.cwrap{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding:6px 2px 18px;scrollbar-width:thin}
.flip{flex:0 0 250px;scroll-snap-align:start;perspective:1000px;height:170px}
.finner{position:relative;width:100%;height:100%;transition:transform .6s;transform-style:preserve-3d}
.flip:hover .finner,.flip:focus-within .finner{transform:rotateY(180deg)}
.fface{position:absolute;inset:0;border-radius:24px;padding:18px;background:var(--card);box-shadow:0 12px 26px rgba(79,69,63,.12),inset 0 3px 6px #fff;backface-visibility:hidden;-webkit-backface-visibility:hidden;display:flex;flex-direction:column;gap:8px}
.fback{transform:rotateY(180deg);background:var(--dark);color:#fff}.fback h4{color:#fff}
.fface h4{font-size:16px;line-height:1.25}.fface small{color:var(--mut);font-size:12px;margin-top:auto}
.fface .chip{font:800 10px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.14em;color:var(--clay)}
.fback a{margin-top:auto;font-weight:700;color:#ffd08a}
.arrows{display:flex;gap:8px}.arrows button{width:42px;height:42px;border-radius:50%;border:0;background:#fff;color:var(--ink);font-size:20px;cursor:pointer;box-shadow:0 8px 18px rgba(79,69,63,.14)}
/* skills */
.sgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}.sgroup{padding:22px}.sgroup h3{font-size:15px;margin-bottom:12px}
@media(max-width:760px){.sgrid{grid-template-columns:1fr}}
/* beyond the day job: small, honest */
.beyond{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.reels{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.reel{position:relative;border:0;border-radius:18px;overflow:hidden;background:#221a16;text-align:left;cursor:pointer;padding:0;color:#fff;transition:transform .25s;box-shadow:0 10px 22px rgba(79,69,63,.18)}
.reel:hover{transform:translateY(-4px)}
.reel img{aspect-ratio:9/16;object-fit:cover;width:100%;opacity:.92}
.reel .play{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:44px;height:44px;border-radius:50%;background:#fff;color:var(--ink);display:grid;place-items:center;font-size:14px}
.reel b{position:absolute;left:10px;right:10px;bottom:10px;font-size:12px;text-shadow:0 2px 8px #000}
dialog.vd{border:0;padding:0;background:transparent;max-width:min(420px,92vw);width:100%}dialog.vd::backdrop{background:rgba(79,69,63,.7);backdrop-filter:blur(8px)}
dialog.vd video{width:100%;aspect-ratio:9/16;border-radius:22px;background:#000}
dialog.vd .x{position:absolute;right:-6px;top:-46px;width:40px;height:40px;border-radius:50%;border:0;background:#fff;color:var(--ink);font-size:20px;cursor:pointer}
@media(max-width:860px){.beyond{grid-template-columns:1fr}}
/* contact */
.contact{padding-bottom:60px}
.cgrid{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.form{padding:26px;display:grid;gap:10px}
.form label{font:800 11px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.14em;color:var(--mut);margin-top:6px}
.form input,.form textarea{width:100%;padding:12px 14px;border-radius:14px;border:1px solid var(--line);background:#fff;color:var(--ink);font:400 15px 'Plus Jakarta Sans',sans-serif}
.form textarea{min-height:120px;resize:vertical}
.form button{margin-top:8px}
.cinfo{display:grid;gap:14px;align-content:start}.cinfo div{padding:18px 20px}.cinfo b{display:block;font:800 11px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.14em;color:var(--mut);margin-bottom:8px}
.cinfo a{color:var(--ink);text-decoration:underline;text-decoration-color:rgba(79,69,63,.3)}
@media(max-width:860px){.cgrid{grid-template-columns:1fr}}
.foot{margin-top:60px;padding-top:24px;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;color:var(--mut);font-size:13px}
.bigname{font-family:'Bricolage Grotesque',sans-serif;font-size:clamp(48px,12vw,150px);font-weight:800;letter-spacing:-.05em;line-height:.9;color:rgba(79,69,63,.07);margin-top:40px;pointer-events:none;user-select:none}
.rv{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1)}.rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}.mq,.flow path,.steam{animation:none}.laptop{transition:none}}
.seo{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
"""

# ---------------------------------------------------------------- html
HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dedric Brown &mdash; Senior Salesforce Product Manager | GTM Systems &amp; Agentforce</title>
<meta name="description" content="Senior product manager who owns Salesforce CRM and GTM systems roadmaps: $150M+ pipeline at Cloudflare, Health Cloud and Agentforce governance at Centene, IAM at Salesforce. Atlanta, open to remote.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='18' fill='%234f453f'/%3E%3Ctext x='32' y='43' font-family='Arial,sans-serif' font-size='28' font-weight='900' fill='%23ffd08a' text-anchor='middle'%3EDB%3C/text%3E%3C/svg%3E">
<meta name="theme-color" content="#f1dcc7">
<meta property="og:type" content="profile"><meta property="og:title" content="Dedric Brown &mdash; Senior Salesforce Product Manager"><meta property="og:description" content="Salesforce CRM, GTM systems and Agentforce product leadership. $150M+ pipeline roadmap, $15M+ retained, 8,000-user SSO/MFA. Atlanta, open to remote."><meta property="og:url" content="{BASE}"><meta property="og:image" content="{BASE}assets/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{BASE}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&display=swap" rel="stylesheet">
<script type="application/ld+json">{JSONLD}</script>
<style>{CSS}</style></head><body>

<nav class="top" aria-label="Sections"><a class="logo" href="#top">DB</a><a class="pl on" href="#about">About</a><a class="pl" href="#career">Career</a><a class="pl" href="#cases">Case studies</a><a class="pl" href="#certs">Credentials</a><a class="pl w" href="world/" title="Ride the 3D resume">3D World</a></nav>
<nav class="dock" aria-label="Quick links"><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a><a href="{CALENDLY}" target="_blank" rel="noopener">Book a call</a><a class="l" href="{PDF}" target="_blank" rel="noopener">Resume</a></nav>

<header class="wrap hero" id="top">
  <div>
    <span class="kicker"><i></i>Hello! I&rsquo;m Dedric &middot; Senior Salesforce PM &middot; Atlanta &middot; remote US</span>
    <h1>I make Salesforce <em>pay for itself.</em></h1>
    <p class="sub">Senior product manager for Salesforce CRM, go-to-market systems and Agentforce, 8+ years across NCR, Salesforce, Cloudflare and Centene. I turn fragmented, manual processes into governed, automated platforms, then prove it with the numbers Finance signs off on.</p>
    <div class="cta"><a class="btn dark" href="{CALENDLY}" target="_blank" rel="noopener">Book a 30-minute call</a><a class="btn" href="{PDF}" target="_blank" rel="noopener">Resume PDF</a><a class="btn holo" href="#cases">Case studies</a></div>
    <div class="switch" id="sw"><b class="a">Sales Cloud years</b><button type="button" aria-label="Switch between Sales Cloud and Health Cloud numbers"><i></i></button><b class="b">Health Cloud now</b></div>
    <div class="stats" id="stats">{stats_html("sales")}</div>
  </div>
  <div class="scene rv" aria-label="Intro video on a laptop">
    <div class="desk"></div>
    <div class="laptop"><div class="lid"><div class="screen">{SCREEN}</div></div><div class="base"><span class="pad"></span><span class="keys"></span></div></div>
    <div class="mug"></div><div class="steam">&#8767;</div>
    {'<button class="unmute" id="unmute" type="button">&#128266; PLAY WITH SOUND</button>' if INTRO else ''}
  </div>
</header>

<div class="proofband" aria-label="Highlights"><div class="mq">
  <span class="pf"><b>$150M+</b>annual pipeline &middot; Sales Cloud roadmap &middot; Cloudflare</span><span class="pf"><b>40%</b>faster time-to-insight &middot; 12+ teams</span><span class="pf"><b>35%</b>Salesforce adoption lift &middot; GTM users</span><span class="pf"><b>$15M+</b>enterprise contracts retained &middot; Salesforce</span><span class="pf"><b>8,000+</b>users on SSO / MFA &middot; incidents down 40%</span><span class="pf"><b>2M+</b>CRM records migrated &middot; zero downtime &middot; NCR</span><span class="pf"><b>9</b>Salesforce credentials &middot; Agentforce Specialist</span>
  <span class="pf"><b>$150M+</b>annual pipeline &middot; Sales Cloud roadmap &middot; Cloudflare</span><span class="pf"><b>40%</b>faster time-to-insight &middot; 12+ teams</span><span class="pf"><b>35%</b>Salesforce adoption lift &middot; GTM users</span><span class="pf"><b>$15M+</b>enterprise contracts retained &middot; Salesforce</span><span class="pf"><b>8,000+</b>users on SSO / MFA &middot; incidents down 40%</span><span class="pf"><b>2M+</b>CRM records migrated &middot; zero downtime &middot; NCR</span><span class="pf"><b>9</b>Salesforce credentials &middot; Agentforce Specialist</span>
</div></div>

<section id="about"><div class="wrap about">
  <div class="photo clay rv"><img src="{HEADSHOT}" alt="Dedric Brown" width="900" height="1125" loading="lazy" decoding="async"><span class="badge"><i></i>SENIOR SALESFORCE PM &middot; CENTENE</span></div>
  <div class="rv">
    <span class="mono">About</span>
    <h2>The story behind the strategy</h2>
    <p>{SUMMARY}</p>
    <p>The pattern is the same every time: find the knot between the teams, untie it with a system of record everyone trusts, then put the automation and the AI on top of data that can carry it.</p>
    <div class="chips"><span>Atlanta, GA</span><span>Open to remote (US)</span><span>SAFe PI cadence</span><span>Fortune 500 &amp; hypergrowth</span><span>BA, Morris Brown College</span></div>
    <div class="gallery"><img src="{DREAMFORCE}" alt="Dedric at Dreamforce" loading="lazy" decoding="async"><img src="{RENDER1}" alt="Dedric speaking at Render" loading="lazy" decoding="async"><img src="{RENDER2}" alt="Dedric at the Render event" loading="lazy" decoding="async"></div>
  </div>
</div></section>

<section id="expertise"><div class="wrap">
  <div class="shead"><span class="mono">Expertise</span><h2>Four things I do at the intersection of product, platform and revenue</h2><p>Not four separate people. One PM who owns the roadmap, the integration, the operating rhythm and the AI governance.</p></div>
  <div class="pillars">{expertise_html.replace('class="pillar rv"', 'class="pillar clay rv"')}</div>
</div></section>

<section id="career"><div class="wrap">
  <div class="shead center"><span class="mono">Career &middot; drawn as a flow</span><h2>Where I've built</h2><p>Each node is a role. The connectors are what carried over: the system-of-record habit, the governance-first roadmap, the numbers Finance signs.</p></div>
  <div class="canvas"><svg class="flow" id="flow" aria-hidden="true"></svg><div class="nodes" id="nodes">{career_html.replace('class="node rv"', 'class="node clay rv"')}</div></div>
</div></section>

<section id="cases"><div class="wrap">
  <div class="shead"><span class="mono">Case studies</span><h2>Problem, what I did, result</h2><p>Four of the knots. Every number comes from the resume, not from a template.</p></div>
  <div class="cases">{cases_html.replace('class="case rv"', 'class="case clay rv"')}</div>
</div></section>

<section id="certs"><div class="wrap">
  <div class="shead" style="display:flex;justify-content:space-between;align-items:end;max-width:none"><div><span class="mono">Credentials</span><h2>{len(CERTS)} credentials, 9 from Salesforce</h2><p>Official names as of the July 2026 rename; prior names noted. Hover to flip and verify on Trailblazer.</p></div><div class="arrows"><button id="cprev" aria-label="Previous">&#8249;</button><button id="cnext" aria-label="Next">&#8250;</button></div></div>
  <div class="cwrap" id="cwrap">{certs_html}</div>
</div></section>

<section id="skills"><div class="wrap">
  <div class="shead"><span class="mono">Skills</span><h2>The stack behind the roadmap</h2></div>
  <div class="sgrid">{skills_html.replace('class="sgroup rv"', 'class="sgroup clay rv"')}</div>
</div></section>

<section id="beyond"><div class="wrap">
  <div class="shead"><span class="mono">Beyond the day job</span><h2>Speaking, and a side project</h2><p>Short talks I recorded for people making a mid-career move into tech, and Blazer2Role, a side project with a free resume scorer. The day job is the roadmap above.</p></div>
  <div class="beyond">
    <div class="reels">{reels_html}</div>
    <div class="clay rv" style="padding:26px"><span class="mono">Side project</span><h3 style="font-size:24px;margin:8px 0 10px">Blazer2Role</h3><p style="color:var(--ink2)">Helps mid-career people translate what they already do into a role in tech. It is where the talks on the left live. <a href="https://blazer2role.com" target="_blank" rel="noopener" style="text-decoration:underline">blazer2role.com</a></p><p style="color:var(--ink2);margin-top:12px">Also: Dreamforce regular, Atlanta, and the person people call when the CRM breaks.</p></div>
  </div>
</div></section>

<section class="contact" id="contact"><div class="wrap">
  <div class="shead"><span class="mono">Contact</span><h2>Let's talk about your roadmap</h2><p>Senior product roles, Salesforce CRM and GTM systems, Agentforce programs. Atlanta or remote across the US.</p></div>
  <div class="cgrid">
    <form class="form clay" action="https://formsubmit.co/{EMAIL}" method="POST">
      <input type="hidden" name="_subject" value="Inquiry from referrernation-web.github.io/dedric"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_next" value="{BASE}#contact">
      <label for="fn">Name</label><input id="fn" name="name" required placeholder="Your name">
      <label for="fe">Email</label><input id="fe" name="email" type="email" required placeholder="you@company.com">
      <label for="fm">Message</label><textarea id="fm" name="message" required placeholder="The role, the platform, the problem."></textarea>
      <button class="btn dark" type="submit">Send</button>
    </form>
    <div class="cinfo">
      <div class="clay"><b>Book directly</b><a href="{CALENDLY}" target="_blank" rel="noopener">calendly.com/dbrowntech15/30min</a></div>
      <div class="clay"><b>Email &amp; phone</b><a href="mailto:{EMAIL}">{EMAIL}</a><br>{PHONE}</div>
      <div class="clay"><b>Profiles</b><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a> &middot; <a href="{TRAILBLAZER}" target="_blank" rel="noopener">Trailblazer</a></div>
      <div class="clay"><b>Resume</b><a href="{PDF}" target="_blank" rel="noopener">Download the PDF</a> &middot; <a href="world/">Ride the 3D version</a></div>
    </div>
  </div>
  <div class="bigname">DEDRIC BROWN</div>
  <div class="foot"><div>&copy; 2026 Dedric Brown &middot; Atlanta, GA</div><div>v1 &middot; September 2026 &middot; <a href="world/">3D world</a></div></div>
</div></section>

<dialog class="vd" id="vd"><button class="x" id="vdx" aria-label="Close">&times;</button><video id="vdv" controls playsinline></video></dialog>

<section class="seo" aria-label="Resume text version"><h2>Dedric Brown resume</h2><p>{SUMMARY}</p><ul>{"".join(f"<li>{when}: {role}, {co}, {loc}. {ctx}</li>" for when, co, role, loc, ctx, b, c in CAREER)}</ul><p>Certifications: {", ".join(c[1] for c in CERTS)}. Education: BA Business Administration, Morris Brown College. Contact: {EMAIL}, {PHONE}, {LINKEDIN}.</p></section>

<script>
(function(){{var v=document.getElementById('reel'),b=document.getElementById('unmute');if(!v||!b||v.tagName!=='VIDEO')return;function tg(){{v.muted=!v.muted;if(!v.muted){{v.currentTime=0;v.play()}}b.innerHTML=v.muted?'&#128266; PLAY WITH SOUND':'&#128263; MUTE'}}b.onclick=tg;}})();
(function(){{var sw=document.getElementById('sw'),st=document.getElementById('stats');if(!sw)return;var S={{sales:{json.dumps(stats_html("sales"))},health:{json.dumps(stats_html("health"))}}};var on=false;sw.querySelector('button').onclick=function(){{on=!on;sw.classList.toggle('on',on);st.classList.add('fade');setTimeout(function(){{st.innerHTML=on?S.health:S.sales;st.classList.remove('fade');count(st)}},250)}};function count(root){{root.querySelectorAll('[data-count]').forEach(function(b){{var to=parseFloat(b.dataset.count),pre=b.dataset.prefix||'',suf=b.dataset.suffix||'',dec=(String(to).split('.')[1]||'').length,t0=null;function f(t){{if(!t0)t0=t;var p=Math.min(1,(t-t0)/900),e=1-Math.pow(1-p,3);b.textContent=pre+(to*e).toFixed(dec)+suf;if(p<1)requestAnimationFrame(f)}}requestAnimationFrame(f)}})}}if(!matchMedia('(prefers-reduced-motion:reduce)').matches)count(st);document.querySelectorAll('#stats .stat').forEach(function(e){{e.classList.add('clay')}});new MutationObserver(function(){{st.querySelectorAll('.stat').forEach(function(e){{e.classList.add('clay')}})}}).observe(st,{{childList:true}});}})();
(function(){{var els=document.querySelectorAll('.rv');if(!('IntersectionObserver' in window)){{els.forEach(function(e){{e.classList.add('in')}});return}}var io=new IntersectionObserver(function(en){{en.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('in');io.unobserve(x.target)}}}})}},{{threshold:.12}});els.forEach(function(e,i){{e.style.transitionDelay=((i%5)*70)+'ms';io.observe(e)}});}})();
(function(){{var svg=document.getElementById('flow'),wrap=document.getElementById('nodes');if(!svg)return;function draw(){{var r=wrap.getBoundingClientRect(),ns=[].slice.call(wrap.querySelectorAll('.node'));svg.setAttribute('viewBox','0 0 '+r.width+' '+r.height);svg.innerHTML='';for(var i=0;i<ns.length-1;i++){{var a=ns[i].getBoundingClientRect(),b=ns[i+1].getBoundingClientRect();var x1=a.left-r.left+a.width/2,y1=a.bottom-r.top,x2=b.left-r.left+b.width/2,y2=b.top-r.top;var p=document.createElementNS('http://www.w3.org/2000/svg','path');p.setAttribute('d','M'+x1+','+y1+' C'+x1+','+(y1+40)+' '+x2+','+(y2-40)+' '+x2+','+y2);svg.appendChild(p)}}}}draw();addEventListener('resize',draw);setTimeout(draw,800);}})();
(function(){{var d=document.getElementById('vd'),v=document.getElementById('vdv');if(!d||!d.showModal)return;document.querySelectorAll('.reel').forEach(function(b){{b.onclick=function(){{v.src=b.dataset.src;d.showModal();v.play()}}}});function close(){{v.pause();v.removeAttribute('src');v.load();d.close()}}document.getElementById('vdx').onclick=close;d.addEventListener('click',function(e){{if(e.target===d)close()}});}})();
(function(){{var g=document.getElementById('cwrap');if(!g)return;var step=264;document.getElementById('cprev').onclick=function(){{g.scrollBy({{left:-step,behavior:'smooth'}})}};document.getElementById('cnext').onclick=function(){{if(g.scrollLeft+g.clientWidth>=g.scrollWidth-4)g.scrollTo({{left:0,behavior:'smooth'}});else g.scrollBy({{left:step,behavior:'smooth'}})}};}})();
(function(){{var links=[].slice.call(document.querySelectorAll('nav.top a.pl')),secs=[].slice.call(document.querySelectorAll('section[id]'));if(!('IntersectionObserver' in window))return;var io=new IntersectionObserver(function(en){{en.forEach(function(x){{if(!x.isIntersecting)return;links.forEach(function(a){{a.classList.toggle('on',a.getAttribute('href')==='#'+x.target.id)}})}})}},{{rootMargin:'-40% 0px -50% 0px'}});secs.forEach(function(s){{io.observe(s)}});}})();
</script>
</body></html>"""

try:
    import htmlmin, rjsmin, rcssmin
    H2 = re.sub(r"<style>(.*?)</style>", lambda m: "<style>" + rcssmin.cssmin(m.group(1)) + "</style>", HTML, flags=re.S)
    H2 = re.sub(r"<script>(.*?)</script>", lambda m: "<script>" + rjsmin.jsmin(m.group(1)) + "</script>", H2, flags=re.S)
    H2 = htmlmin.minify(H2, remove_comments=True, remove_empty_space=True, reduce_boolean_attributes=False)
except Exception as e:
    print("minify skipped:", e); H2 = HTML
(HERE / "index.html").write_text(H2, encoding="utf-8")
(HERE / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + BASE + "sitemap.xml\n", encoding="utf-8")
(HERE / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                  f'<url><loc>{BASE}</loc></url><url><loc>{BASE}world/</loc></url></urlset>', encoding="utf-8")
(HERE / "llms.txt").write_text(f"# Dedric Brown\n\n> Senior Salesforce Product Manager (CRM, GTM systems, Agentforce), Atlanta GA, open to remote US.\n\n- Resume site: {BASE}\n- 3D resume: {BASE}world/\n- Resume PDF: {BASE}{PDF}\n- LinkedIn: {LINKEDIN}\n- Trailblazer: {TRAILBLAZER}\n\n"
                               + "\n".join(f"- {when}: {re.sub('<[^>]+>', '', role)}, {co} ({loc})" for when, co, role, loc, *_ in CAREER) + "\n", encoding="utf-8")
print("written", len(H2) // 1024, "KB; intro video:", INTRO or "not yet (still on the laptop)")
