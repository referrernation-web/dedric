# -*- coding: utf-8 -*-
"""Turn a fresh copy of mark-portfolio/build.py into Dedric's build.py: same format, Dedric's data, blazer2role.com colours.
Run:  cp ../mark-portfolio/build.py build.py && python adapt.py && python build.py"""
import re, pathlib, json
HERE = pathlib.Path(__file__).parent
P = HERE / "build.py"
s = P.read_text(encoding="utf-8")
assert "Mark Edcel" in s, "build.py is not the fresh copy of Mark's"

EMAIL, PHONE = "dedric.brown55@gmail.com", "470-262-7774"
LI, TB, CAL = "https://www.linkedin.com/in/dbrowntech", "https://www.salesforce.com/trailblazer/dbrown6422", "https://calendly.com/dbrowntech15/30min"
BASE = "https://referrernation-web.github.io/dedric/"
PDF = "assets/Dedric-Brown-Resume-2026.pdf"


def one(old, new, regex=False, flags=re.S):
    global s
    if regex:
        n = len(re.findall(old, s, flags)); assert n == 1, (old[:70], n)
        s = re.sub(old, lambda _: new, s, count=1, flags=flags)
    else:
        n = s.count(old); assert n == 1, (old[:70], n)
        s = s.replace(old, new)


# ---------------------------------------------------------------- thumbnails for the case-study cards (branded, no fake screenshots)
def thumbs():
    from PIL import Image, ImageDraw, ImageFont
    A = HERE / "assets"
    cards = {"cloudflare": ("Salesforce → NetSuite", "One system of record, quote to cash", "CLOUDFLARE · 2023–2026"),
             "centene-ai": ("Agentforce, governed", "Two workflows held until the data was ready", "CENTENE · 2026"),
             "centene-id": ("One provider identity", "NPI-keyed across three prescriber systems", "CENTENE · 2026"),
             "salesforce-iam": ("SSO + MFA, 8,000 users", "Access incidents down 40%", "SALESFORCE · 2020–2021")}
    try:
        F1 = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 74); F2 = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 34); F3 = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 26)
    except Exception:
        F1 = F2 = F3 = ImageFont.load_default()
    for key, (h, sub, tag) in cards.items():
        im = Image.new("RGB", (1280, 800), (5, 5, 7)); d = ImageDraw.Draw(im)
        for y in range(800):   # violet glow from the top-right
            pass
        glow = Image.new("RGB", (1280, 800), (5, 5, 7))
        gd = ImageDraw.Draw(glow)
        for r in range(900, 0, -12):
            k = r / 900; col = (int(5 + (108 - 5) * (1 - k) * .55), int(5 + (43 - 5) * (1 - k) * .55), int(7 + (217 - 7) * (1 - k) * .55))
            gd.ellipse([1100 - r, -200 - r * .6, 1100 + r, -200 + r * .6], fill=col)
        im = Image.blend(im, glow, 1.0); d = ImageDraw.Draw(im)
        for gx in range(0, 1280, 40): d.line([(gx, 0), (gx, 800)], fill=(14, 13, 22))
        for gy in range(0, 800, 40): d.line([(0, gy), (1280, gy)], fill=(14, 13, 22))
        d.text((80, 90), tag, font=F3, fill=(170, 255, 0))
        d.text((80, 300), h, font=F1, fill=(250, 250, 250))
        d.text((80, 410), sub, font=F2, fill=(169, 166, 184))
        d.rounded_rectangle([80, 640, 420, 700], radius=10, fill=(108, 43, 217)); d.text((104, 652), "Open case study  →", font=F2, fill=(255, 255, 255))
        im.save(A / f"thumb-{key}.jpg", quality=86)
    # the side-project card: welcome-video frame
    src = A / "hero-poster.jpg"
    if src.exists():
        Image.open(src).convert("RGB").resize((720, 1280)).crop((0, 200, 720, 650)).resize((1280, 800)).save(A / "thumb-blazer2role.jpg", quality=84)


thumbs()

# ---------------------------------------------------------------- data blocks
one(r'PHOTO = b64\("mark-photo.jpg"\)\nHERO = .*?\nABOUT = .*?\n', 'PHOTO = ""\nHERO = webp("dedric-frame.jpg", 1280, 82)\nABOUT = webp("headshot.jpg", 720, 82)\nINTRO = "video/intro.mp4" if (pathlib.Path(__file__).parent / "video" / "intro.mp4").exists() else ""\n', True)
one(r'THUMBS = \{k: webp\("thumb-" \+ d \+ "\.jpg", 1280, 78\) for k, d in \{.*?\}\.items\(\)\}\n',
    'THUMBS = {k: webp("thumb-" + k + ".jpg", 1280, 78) for k in ["cloudflare", "centene-ai", "centene-id", "salesforce-iam", "blazer2role"]}\n', True)
one(r'EXPERTISE = \[\n.*?\n\]\n', '''EXPERTISE = [
    ("01", "Product Strategy &amp; Roadmap Ownership",
     "Vision, portfolio intake, business cases, prioritization, acceptance criteria, release plans and post-launch measurement across enterprise Salesforce ecosystems."),
    ("02", "CRM &amp; ERP Systems Integration",
     "Salesforce to NetSuite across opportunity-to-order, order-to-cash, billing, invoicing and revenue recognition. External IDs, master data, deduplication, one system of record."),
    ("03", "GTM &amp; Revenue Operations",
     "Lead-to-opportunity, pipeline management, forecasting, marketing automation, renewals and retention, KPI definition and the dashboards Finance actually adopts."),
    ("04", "Agentforce &amp; AI Automation",
     "Agentforce and Einstein use cases with process mapping, data-readiness gates, human-in-the-loop controls and AI governance in HIPAA-regulated workflows."),
]
''', True)
one(r'SKILL_GROUPS = \[\n.*?\n\]\n', '''SKILL_GROUPS = [
    ("Salesforce Platform", [
        ("salesforce", "Sales Cloud"), ("salesforce", "Service Cloud"), ("salesforce", "Health Cloud"),
        ("salesforce", "Marketing Cloud"), ("salesforce", "OmniStudio"), ("salesforce", "Agentforce")]),
    ("Systems &amp; Integration", [
        ("oracle", "NetSuite ERP"), ("mulesoft", "MuleSoft"), ("postman", "APIs"),
        ("snowflake", "Data models"), ("tableau", "Tableau"), ("okta", "IAM · SSO · MFA")]),
    ("AI &amp; Automation", [
        ("salesforce", "Einstein"), ("anthropic", "Claude API"), ("openai", "LLMs"),
        ("zapier", "Workflow automation"), ("googlesheets", "Data readiness"), ("json", "Governance")]),
    ("Product &amp; Delivery", [
        ("jira", "Jira"), ("confluence", "Confluence"), ("miro", "Miro"),
        ("figma", "Figma"), ("scrumalliance", "Scrum · SAFe"), ("slack", "Slack")]),
]
''', True)
one(r'FEATURED = \[\n.*?\n\]\n', '''FEATURED = [
    ("ERP INTEGRATION • CLOUDFLARE", "One system of record from quote to cash",
     "Opportunity, order, billing and revenue recognition lived in two systems that never agreed. I owned the Salesforce-to-NetSuite integration end to end: external IDs and reconciliation rules first, then the roadmap.",
     "Time-to-insight down 40% &mdash; KPI dashboards adopted by 12+ teams; fewer manual handoffs at month-end close",
     ["Sales Cloud", "NetSuite", "External IDs", "Rev rec"], "cloudflare", "#career"),
    ("AI GOVERNANCE • CENTENE", "Agentforce that clears a HIPAA gate",
     "Prior authorization, benefits investigation and referral-to-therapy were the obvious AI targets, but the source data behind two of them could not be trusted yet. I built the readiness path before the use case.",
     "Two workflows held back from production until the data was fixed &mdash; the ones that shipped carry controls Compliance can review",
     ["Agentforce", "Einstein", "Health Cloud", "HIPAA"], "centene-ai", "#career"),
    ("PROVIDER IDENTITY • CENTENE", "Three prescriber systems, one provider",
     "ScriptMed (Inovalon), the Centene prescriber file and Symphony Health each described the same provider differently. I standardized the data models and keyed external IDs on the NPI.",
     "One provider identity the roadmap can build on &mdash; the governance backbone for the CRM modernization",
     ["Master data", "NPI", "Deduplication", "Governance"], "centene-id", "#career"),
    ("IDENTITY &amp; ACCESS • SALESFORCE", "SSO and MFA for 8,000 users",
     "Access-related incidents kept landing on $25M+ of regulated contracts. I stood up enterprise IAM frameworks, integrated IAM with the security stack and drove SSO/MFA to the full user base.",
     "Access incidents down 40% &mdash; 10+ critical findings closed, one access story for compliance and audit",
     ["IAM", "SSO", "MFA", "Zero trust"], "salesforce-iam", "#career"),
    ("SIDE PROJECT • SPEAKING", "Blazer2Role",
     "A side project for people making a mid-career move into tech: short talks and a free resume scorer. It is where the Why Tech series lives. The day job is the roadmap above.",
     "Seven approved talks published &mdash; Sept 2026",
     ["Speaking", "Community", "Side project"], "blazer2role", "https://blazer2role.com"),
]
''', True)
one(r'SYSLOG = \[\n.*?\n\]\n', '''SYSLOG = [
    ("Centene &middot; Health Cloud roadmap", "Specialty pharmacy and managed care &middot; 27.6M members &middot; since Jan 2026", "Current", "#career"),
    ("Cloudflare &middot; $150M+ pipeline", "Sales Cloud roadmap owner &middot; SAFe PI cadence &middot; adoption up 35%", "GTM", "#career"),
    ("Salesforce &middot; Customer Platforms", "$15M+ retained &middot; $10M+ renewal book &middot; lead gen up 35%", "Retention", "#career"),
    ("NCR &middot; CRM modernization", "2M+ records migrated with zero downtime &middot; $1.8M+ cost savings", "Migration", "#career"),
    ("Dreamforce", "Regular attendee and speaker-track alumni &middot; San Francisco", "Community", "https://www.salesforce.com/dreamforce/"),
    ("Why Tech series", "Five approved talks for mid-career changers &middot; Blazer2Role", "Speaking", "https://blazer2role.com"),
]
''', True)
CERTS = [("SALESFORCE", "Agentforce Specialist", "formerly AI Specialist · Oct 2024", TB), ("SALESFORCE", "AI Associate", "Oct 2024", TB),
         ("SALESFORCE", "Agentforce Sales Consultant", "formerly Sales Cloud Consultant · Apr 2023", TB), ("SALESFORCE", "Platform Strategy Designer", "formerly Strategy Designer · Apr 2023", TB),
         ("SALESFORCE", "Business Analyst", "Jan 2023", TB), ("SALESFORCE", "Platform Administrator II", "formerly Advanced Administrator · Sep 2022", TB),
         ("SALESFORCE", "Platform Foundations", "formerly Salesforce Associate · Sep 2022", TB), ("SALESFORCE", "Agentforce Service Consultant", "formerly Service Cloud Consultant · Dec 2021", TB),
         ("SALESFORCE", "Platform Administrator", "formerly Administrator · Oct 2020", TB), ("SCALED AGILE", "SAFe 6 Product Owner / Product Manager", "Jun 2024", LI),
         ("SCRUM ALLIANCE", "Certified ScrumMaster (CSM)", "Jan 2023", LI), ("GOOGLE", "Google AI Essentials", "Coursera · Jun 2026", LI),
         ("COMPTIA", "Security+", "CompTIA", LI), ("TRAILHEAD", "Security Specialist Superbadge", "Salesforce Trailhead", TB)]
one(r'CERTS = \[\n.*?\n\]\n', "CERTS = [\n" + "".join(f'    ({json.dumps(c)}, "{i+1:02d}", {json.dumps(t)}, {json.dumps(d)}, {json.dumps(u)}),\n' for i, (c, t, d, u) in enumerate(CERTS)) + "]\n", True)
one(r'LQ = \{k: .*?\n', 'LQ = {k: __import__("patch8_lqip").lqip(A / ("thumb-" + k + ".jpg")) for k in ["cloudflare", "centene-ai", "centene-id", "salesforce-iam", "blazer2role"]}\n', True)
one('<span class="visit">Open case study &rarr;</span>', '<span class="visit">Open case study &rarr;</span>')   # unchanged, sanity

# ---------------------------------------------------------------- head
one(r'<title>.*?</title>', '<title>Dedric Brown &mdash; Senior Salesforce Product Manager | GTM Systems &amp; Agentforce</title>', True)
one(r'<meta name="description" content=".*?">', '<meta name="description" content="Senior product manager who owns Salesforce CRM and GTM systems roadmaps: $150M+ pipeline at Cloudflare, Health Cloud and Agentforce governance at Centene, IAM at Salesforce. Atlanta, open to remote.">', True)
one(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="Dedric Brown &mdash; Senior Salesforce Product Manager">', True)
one(r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="Salesforce CRM, GTM systems and Agentforce product leadership. $150M+ pipeline roadmap, $15M+ retained, 8,000-user SSO/MFA. Atlanta, open to remote.">', True)
s = s.replace("https://referrernation-web.github.io/portfolio/", BASE)
s = s.replace('<link rel="preload" as="image" href="assets/spr/d-run.webp" media="(min-width:981px)"><link rel="preload" as="image" href="assets/spr/p-run.webp" media="(min-width:981px)">', "")
one("font-size='32' font-weight='800' fill='%23fff' text-anchor='middle'%3EM%3C/text%3E%3Ccircle cx='48' cy='44' r='6' fill='%23ff2a2a'/%3E", "font-size='26' font-weight='800' fill='%23AAFF00' text-anchor='middle'%3EDB%3C/text%3E")
one('<meta name="theme-color" content="#000000">', '<meta name="theme-color" content="#050507">')
one('family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Caveat:wght@600', 'family=Space+Grotesk:wght@400;500;600;700&family=DM+Serif+Display:ital@0;1&family=JetBrains+Mono:wght@400;500;600;700&family=Caveat:wght@600')

# ---------------------------------------------------------------- nav + hero
one('<span class="logo">Mark Edcel<i> .</i></span>', '<span class="logo">Dedric Brown<i> .</i></span>')
one('<a class="hire" href="#contact">Hire Me</a>', f'<a class="hire" href="{CAL}" target="_blank" rel="noopener">Book a call</a>')
one('<video id="reel" data-depth="-6" src="video/heroreel.mp4" poster=\\"""" + HERO + """" muted autoplay loop playsinline preload="metadata"></video>',
    '<video id="reel" data-depth="-6"\\"""" + (" src=\\"" + INTRO + "\\"" if INTRO else "") + """ poster=\\"""" + HERO + """" muted autoplay loop playsinline preload="metadata"></video>')
one('<h1><span class="kt" id="kt">Hi, I&rsquo;m a</span><br><span class="rot" id="rot" aria-live="polite">Full-Stack Developer</span><span class="uline"></span></h1>',
    '<h1><span class="kt" id="kt">Hi, I&rsquo;m Dedric, a</span><br><span class="rot" id="rot" aria-live="polite">Senior Product Manager</span><span class="uline"></span></h1>')
one('<p class="sub">I build fast, scalable websites and web apps in WordPress, Node.js and React, then own the technical SEO and AI-search visibility that makes them rank.</p>',
    '<p class="sub">I own Salesforce CRM and go-to-market systems roadmaps, from NetSuite integrations to Agentforce governance, and turn fragmented, manual processes into platforms Finance signs off on.</p>')
one('<a class="btn light" href="#projects">View My Work</a><a class="btn ghosty" href="#contact">Contact Me</a><a class="btn ghosty" href="world/" title="3D resume: ride Kimpoy with Dianna across the wonders of the world">&#127758; Ride the 3D World</a>',
    f'<a class="btn light" href="#projects">View Case Studies</a><a class="btn ghosty" href="world/" title="3D resume: ride Rev across the cities where the career happened">&#127758; Ride the 3D World</a><a class="btn ghosty" href="{PDF}" target="_blank" rel="noopener">Resume PDF</a>')
one('<span class="flabel tr">// Full-Stack &middot; SEO &middot; AEO<br>Available now</span>', '<span class="flabel tr">// Salesforce &middot; GTM Systems &middot; Agentforce<br>Centene, since Jan 2026</span>')
one('<span class="flabel bl">// Makati &rarr; US &middot; CA &middot; AU<br>ET / PT overlap</span>', '<span class="flabel bl">// Atlanta &middot; remote US<br>$150M+ pipeline roadmap</span>')
one('<span class="ainote">AI-GENERATED REEL &middot; REAL RESULTS BELOW</span>', '<span class="ainote">""" + ("APPLICATION INTRO &middot; REAL RESULTS BELOW" if INTRO else "INTRO VIDEO IN PRODUCTION &middot; REAL RESULTS BELOW") + """</span>')
one('<button class="unmute" id="unmute">&#128266; UNMUTE REEL</button>', '""" + (\'<button class="unmute" id="unmute">&#128266; UNMUTE INTRO</button>\' if INTRO else "") + """')
one("var R=['Full-Stack Developer','WordPress Developer','SEO Specialist','AEO Specialist']", "var R=['Senior Product Manager','Salesforce PM','GTM Systems Owner','Agentforce Lead']")

# ---------------------------------------------------------------- proof band
one(r'<div class="proofband" aria-label="Evidence highlights"><div class="mq-track">.*?</div></div>',
    '<div class="proofband" aria-label="Evidence highlights"><div class="mq-track">' + 2 * ('<span class="pf"><b>$150M+</b>annual pipeline · Sales Cloud roadmap · Cloudflare</span><span class="pf"><b>40%</b>faster time-to-insight · 12+ teams</span><span class="pf"><b>35%</b>Salesforce adoption lift · GTM users</span><span class="pf"><b>$15M+</b>enterprise contracts retained · Salesforce</span><span class="pf"><b>8,000+</b>users on SSO / MFA · incidents down 40%</span><span class="pf"><b>2M+</b>CRM records migrated · zero downtime · NCR</span><span class="pf"><b>9</b>Salesforce credentials · Agentforce Specialist</span><span class="pf"><b>Atlanta</b>open to remote across the US</span>') + '</div></div>', True)

# ---------------------------------------------------------------- about
one('alt="Mark Edcel Lopez" loading="lazy" decoding="async" width="720" height="720">', 'alt="Dedric Brown" loading="lazy" decoding="async" width="720" height="720">')
one('<div class="badge"><span class="dot"></span>OPEN TO OPPORTUNITIES</div>', '<div class="badge"><span class="dot"></span>OPEN TO SENIOR PM ROLES</div>')
one('<h2>I&rsquo;m Mark Edcel Lopez</h2>', '<h2>I&rsquo;m Dedric Brown</h2>')
one(r'<p>A full-stack developer based in Makati.*?</p>', '<p>A senior product and platform leader in Atlanta with 8+ years owning product vision, strategy, roadmaps and end-to-end delivery for enterprise Salesforce CRM, go-to-market systems, revenue operations, identity, healthcare and AI automation. I partner with executives across Sales, Marketing, Finance, Engineering, IT, Clinical Operations and Compliance to turn fragmented, manual processes into governed, automated platforms with measurable revenue impact.</p>', True)
one(r'<div class="stats">\n.*?\n    </div>', '''<div class="stats">
      <div class="stat glow hv" data-rv="drop"><b data-count="150" data-prefix="$" data-suffix="M+">$150M+</b><span>annual pipeline, Sales Cloud roadmap (Cloudflare)</span></div>
      <div class="stat glow hv" data-rv="drop"><b data-count="15" data-prefix="$" data-suffix="M+">$15M+</b><span>enterprise contracts retained (Salesforce)</span></div>
      <div class="stat glow hv" data-rv="drop"><b data-count="40" data-suffix="%">40%</b><span>faster time-to-insight, 12+ teams</span></div>
      <div class="stat glow"><b>8,000+</b><span>users on SSO / MFA</span></div>
    </div>''', True)

# ---------------------------------------------------------------- journey
one('<div class="shead center"><span class="mono">HUMBLE BEGINNINGS</span><h2>From Service Crew to Search Engineer</h2>\n  <p>Every success story has humble beginnings. Mine started behind a pizza counter.</p></div>',
    '<div class="shead center"><span class="mono">CAREER JOURNEY</span><h2>From CRM Records to the AI Roadmap</h2>\n  <p>Five roles, three Fortune 500 logos and one hypergrowth company. The same knot every time, untied at a bigger scale.</p></div>')
one(r'<blockquote class="jquote glass" data-rv="zoom"><p>.*?</p><footer>.*?</footer></blockquote>',
    '<blockquote class="jquote glass" data-rv="zoom"><p>&ldquo;Every role was the same knot in a bigger company: two teams, two systems, no shared truth. Untie it, then put the automation on data that can carry it.&rdquo;</p><footer>&mdash; the line I open with in every roadmap review</footer></blockquote>', True)
JT = [("2014&ndash;2017", "BA, Business Administration, Morris Brown College", "Atlanta. The business side first; the platform came after."),
      ("2018&ndash;2020", "Product Manager, CRM Platforms, NCR Corporation", "Sales Cloud modernization: $1.8M+ cost savings, 2M+ legacy records migrated with zero downtime, data accuracy up 35%."),
      ("2020&ndash;2021", "Product Manager, Identity &amp; Security, Salesforce", "SSO and MFA across 8,000+ users on $25M+ of regulated contracts. Access incidents down 40%, 10+ critical findings closed."),
      ("2021&ndash;2023", "Product Manager, Customer Platforms, Salesforce", "Vlocity / OmniStudio and Marketing Cloud roadmap. $15M+ retained, $10M+ renewal book, lead generation up 35%."),
      ("2023&ndash;2026", "Product Manager, GTM Business Systems, Cloudflare", "Sales Cloud roadmap behind $150M+ in pipeline. NetSuite ERP integration, time-to-insight down 40%, adoption up 35%."),
      ("2026", "Senior Salesforce Product Manager, Centene", "Health Cloud roadmap for specialty pharmacy. Agentforce governance, NPI-keyed provider identity, HIPAA-ready controls.")]
jt_html = "".join(f'<li class="jt" data-rv="{"left" if i % 2 == 0 else "right"}"><span class="jdot"></span><div class="jcard hv"><span class="jyear">{y}</span><h3>{t}</h3><p>{d}</p></div></li>' for i, (y, t, d) in enumerate(JT))
one(r'<ol class="jline">.*?</ol>', '<ol class="jline">' + jt_html + '</ol>', True)
one('<div class="note">The journey continues.</div>', '<div class="note">Next: your roadmap.</div>')

# ---------------------------------------------------------------- expertise / skills / projects / certs / intro
one('<h2>Building Sites That Rank in Google &amp; AI</h2>\n    <p>Combining WordPress engineering, technical SEO and Answer Engine Optimization to create sites that get found, cited and hired.</p>\n    <div class="note">Turning rankings into revenue!</div>\n    <button class="mg-play" id="mgplay" type="button">&#9654; WATCH DIANNA PLAY</button>',
    '<h2>Making Salesforce Pay for Itself</h2>\n    <p>One PM who owns the roadmap, the integration, the operating rhythm and the AI governance. Not four separate people.</p>\n    <div class="note">Governance first, then automation.</div>')
one('<h2>Technologies I Work With</h2>\n  <p>Full-stack WordPress, search and AI-visibility tooling I use daily.</p>', '<h2>The Stack Behind the Roadmap</h2>\n  <p>Salesforce clouds, the systems they connect to, and the delivery tooling I run every sprint.</p>')
one('<h2>Projects That Define My Journey</h2>\n  <p>Production client sites and AEO programs. Every number names its evidence.</p>', '<h2>Case Studies That Define the Work</h2>\n  <p>Problem, what I did, result. Every number comes from the resume, not from a template.</p>')
one('<h3>System Logs &amp; Other Engagements</h3>', '<h3>Roles &amp; Other Engagements</h3>')
one('<div class="logline">Reviewing client engagements continuous<span class="cursor"></span></div>', '<div class="logline">Reviewing roadmap items continuous<span class="cursor"></span></div>')
one('<h2>Professional Credentials</h2>', '<h2>Professional Credentials</h2>')
one('Total of """ + str(len(CERTS)) + """ certificates running.', 'Total of """ + str(len(CERTS)) + """ credentials, 9 from Salesforce. Official names as of July 2026.')
one('<a class="btn light" id="csdUrl" target="_blank" rel="noopener">Visit live site &rarr;</a>', '<a class="btn light" id="csdUrl" rel="noopener">See the role &rarr;</a>')
one(r'<section id="intro" class="lz"><div class="wrap">.*?</div></section>',
    '<section id="intro" class="lz"><div class="wrap">\n  <div class="shead center"><span class="mono">INTRO TRANSMISSION</span><h2>Meet Me in Forty Seconds</h2></div>\n  <div class="introwrap glow" id="loomwrap">""" + (\'<video src="\' + INTRO + \'" poster="\' + HERO + \'" controls playsinline preload="metadata" style="width:100%;height:100%;object-fit:cover;background:#000"></video>\' if INTRO else \'<button class="loomfacade" id="loomplay" aria-label="Intro video in production" type="button" disabled><span class="playbtn">&#9654;</span><span>Application intro: in production</span></button>\') + """</div>\n  <p class="intronote">""" + ("Who I am, what I own, three numbers, and what to do next." if INTRO else "Recording this week. The receipts above do not wait.") + """</p>\n</div></section>', True)

# ---------------------------------------------------------------- contact + footer
one('action="https://formsubmit.co/markedcel06@gmail.com"', f'action="https://formsubmit.co/{EMAIL}"')
one('<input type="hidden" name="_subject" value="Portfolio inquiry &mdash; referrernation-web.github.io">', '<input type="hidden" name="_subject" value="Inquiry &mdash; referrernation-web.github.io/dedric">')
one('placeholder="Tell me about your site and what it should rank for."', 'placeholder="The role, the platform, the problem."')
one(r'<div class="cinfo">\n.*?\n    </div>', f'''<div class="cinfo">
      <div><b>// Senior Product Manager</b>Salesforce CRM &amp; GTM systems<br>Agentforce &amp; AI governance</div>
      <div><b>// Status</b><span class="st">Open to senior PM roles</span><br>Atlanta &middot; remote across the US</div>
      <div><b>// Book a call</b><a href="{CAL}" target="_blank" rel="noopener">calendly.com/dbrowntech15/30min</a></div>
      <div><b>// Verify</b><a href="{TB}" target="_blank" rel="noopener">Trailblazer profile</a> &middot; <a href="{LI}" target="_blank" rel="noopener">LinkedIn</a></div>
    </div>''', True)
one('<div class="bigname">MARK EDCEL</div>', '<div class="bigname">DEDRIC BROWN</div>')
one(r'<div class="foot">\n.*?\n  </div>', f'''<div class="foot">
    <div>Contact Transmission<br>{EMAIL} &middot; {PHONE}</div>
    <div><a href="{LI}">LinkedIn</a> &middot; <a href="{TB}">Trailblazer</a> &middot; <a href="{PDF}">Resume PDF</a> &middot; <a href="world/">3D World</a></div>
    <div>&copy; 2026 Dedric Brown &middot; v1 &middot; September 2026</div>
  </div>''', True)

# ---------------------------------------------------------------- scripts: drop the mascot game and the Loom embed
one(r"\(function\(\)\{var DBG=/mgdebug/.*?\n(?=\(function\(\)\{var imgs=document\.querySelectorAll\('img\.lq)", "", True)
one(r"\(function\(\)\{var b=document\.getElementById\('loomplay'\);.*?\n", "", True)
s = s.replace(".mg-play", ".mg-play-off")

# ---------------------------------------------------------------- palette: blazer2role.com (dark, violet, lime)
PAL = [("#8a1c2b", "#6C2BD9"), ("#a02538", "#7c3ae6"), ("#7a1424", "#5a22b8"), ("#9d2436", "#7c3ae6"), ("#d8293f", "#8a55f0"), ("#b23445", "#7c3ae6"), ("#5e0e1b", "#3d1a80"),
       ("#c2606c", "#a07ff0"), ("#d08a95", "#c4a8ff"), ("#b8404f", "#8a55f0"), ("#e6b3bb", "#c4a8ff"), ("#f4d5da", "#e3d6ff"), ("#f0c2c9", "#d9c7ff"), ("#f8e9ec", "#1b1a26"),
       ("138,28,43", "108,43,217"), ("90,20,30", "40,10,90"), ("160,90,100", "150,110,220"), ("#ff2a2a", "#AAFF00"), ("#d40f1f", "#6C2BD9"), ("#e5322d", "#6C2BD9"),
       ("background:rgba(255,255,255,.55);-webkit-backdrop-filter:blur(16px) saturate(160%);backdrop-filter:blur(16px) saturate(160%);border-bottom:1px solid rgba(255,255,255,.7);box-shadow:0 4px 24px rgba(0,0,0,.05);color:#111}", "background:rgba(5,5,7,.6);-webkit-backdrop-filter:blur(16px) saturate(160%);backdrop-filter:blur(16px) saturate(160%);border-bottom:1px solid rgba(255,255,255,.08);box-shadow:0 4px 24px rgba(0,0,0,.3);color:#FAFAFA}"),
       ("nav{background:rgba(247,246,244,.8);border-color:var(--line)}", "nav{background:rgba(5,5,7,.8);border-color:var(--line)}"),
       ("nav.scrolled{background:rgba(255,255,255,.82);box-shadow:0 6px 30px rgba(0,0,0,.08);border-bottom-color:rgba(0,0,0,.06)}", "nav.scrolled{background:rgba(5,5,7,.88);box-shadow:0 6px 30px rgba(0,0,0,.4);border-bottom-color:rgba(255,255,255,.08)}"),
       # light shell -> dark shell
       ("--bg:#fff;--surf:#fff;--line:#e6e6ea;--txt:#111;--mut:#666", "--bg:#050507;--surf:#14131d;--line:rgba(255,255,255,.1);--txt:#FAFAFA;--mut:#a9a6b8"),
       ("body{background:#fff;color:#111;", "body{background:#050507;color:#FAFAFA;"),
       ("font:400 16px/1.6 Inter,ui-sans-serif,system-ui,sans-serif", "font:400 16px/1.6 'Space Grotesk',ui-sans-serif,system-ui,sans-serif"),
       ("--clay-bg:linear-gradient(145deg,#ffffff 0%,#f3f3f7 100%)", "--clay-bg:linear-gradient(145deg,#1c1b27 0%,#12111a 100%)"),
       ("--clay-sh:0 18px 34px rgba(17,17,17,.10),0 4px 10px rgba(17,17,17,.06),inset 0 -6px 12px rgba(0,0,0,.06),inset 0 3px 6px rgba(255,255,255,.95)", "--clay-sh:0 18px 34px rgba(0,0,0,.45),0 4px 10px rgba(0,0,0,.3),inset 0 -6px 12px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.08)"),
       ("inset 0 3px 6px #fff}", "inset 0 1px 0 rgba(255,255,255,.08)}"),
       (".stat,.icon,.proj,.jcard,.fface,.pin,.pcard,.csdIn,.lrow{background:var(--clay-bg);border:1px solid rgba(255,255,255,.9);", ".stat,.icon,.proj,.jcard,.fface,.pin,.pcard,.csdIn,.lrow{background:var(--clay-bg);border:1px solid rgba(255,255,255,.1);"),
       (".btn:not(.light){background:linear-gradient(180deg,#fff,#ececf1);color:#111}", ".btn:not(.light){background:linear-gradient(180deg,#1f1e2b,#14131d);color:#FAFAFA;border:1px solid rgba(255,255,255,.12)}"),
       (".btn.light,.hire{background:linear-gradient(180deg,#a02538,#7a1424)}", ".btn.light,.hire{background:linear-gradient(180deg,#b8ff2a,#8fd400);color:#0a1400}"),
       (".pill{background:linear-gradient(180deg,#fff,#f0f0f4);border-color:#fff;box-shadow:0 3px 6px rgba(0,0,0,.08),inset 0 -2px 3px rgba(0,0,0,.06),inset 0 1px 2px #fff;color:#444}", ".pill{background:linear-gradient(180deg,#1f1e2b,#14131d);border-color:rgba(255,255,255,.12);box-shadow:none;color:#d9d6e6}"),
       (".xnum,.cat{text-shadow:0 1px 0 #fff}", ".xnum,.cat{text-shadow:none}"),
       (".dock{position:fixed;top:auto;right:auto;left:50%;bottom:18px;transform:translateX(-50%);border-bottom:0;z-index:60;display:flex;gap:2px;padding:6px;border-radius:99px;background:rgba(255,255,255,.62)", ".dock{position:fixed;top:auto;right:auto;left:50%;bottom:18px;transform:translateX(-50%);border-bottom:0;z-index:60;display:flex;gap:2px;padding:6px;border-radius:99px;background:rgba(20,19,29,.86)"),
       (".dock a{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;gap:1px;width:64px;padding:7px 0 6px;border-radius:99px;color:#444;", ".dock a{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;gap:1px;width:64px;padding:7px 0 6px;border-radius:99px;color:#d9d6e6;"),
       (".dock a:hover{transform:translateY(-4px) scale(1.06);color:#111}", ".dock a:hover{transform:translateY(-4px) scale(1.06);color:#fff}"),
       (".glass{background:rgba(255,255,255,.55);", ".glass{background:rgba(20,19,29,.7);"),
       ("@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.glass{background:rgba(255,255,255,.94)}", "@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.glass{background:rgba(20,19,29,.96)}"),
       ]
for a, b in PAL:
    s = s.replace(a, b)
# serif display for headings like blazer2role.com; the rest stays Space Grotesk
s = s.replace("h1,h2{", "h1,h2{font-family:'DM Serif Display',Georgia,serif;font-weight:400;", 1) if "h1,h2{" in s else s + "\n"
if "font-family:'DM Serif Display'" not in s:
    s = s.replace("<style>\"\"\" + CSS + \"\"\"", "<style>\"\"\" + CSS + \"\"\"\nh1,h2{font-family:'DM Serif Display',Georgia,serif;font-weight:400;letter-spacing:-.01em}", 1)
# remaining white surfaces and near-black text in the CSS block only
css_start, css_end = s.index('CSS = """'), s.index('"""', s.index('CSS = """') + 8)
css = s[css_start:css_end]
css = re.sub(r"(?<![0-9a-fA-F])#111(?![0-9a-fA-F])", "#FAFAFA", css)
css = re.sub(r"(?<![0-9a-fA-F])#fff(?![0-9a-fA-F])", "#14131d", css)
css = re.sub(r"(?<![0-9a-fA-F])#ffffff(?![0-9a-fA-F])", "#14131d", css)
css = css.replace("#f7f6f4", "#0b0a12").replace("#e5e2dc", "rgba(255,255,255,.1)").replace("#6b6b6b", "#a9a6b8").replace("#444", "#d9d6e6").replace("#666", "#a9a6b8").replace("#f3f3f7", "#12111a").replace("#ececf1", "#14131d").replace("#f0f0f4", "#14131d")
OVERRIDES = """
/* ---- readability overrides (blazer2role palette on Mark's layout) ---- */
.btn.light,.hire,.viewc,.playbtn,.skip,.form button,.csd .btn.light{color:#0a1400!important;background:linear-gradient(180deg,#b8ff2a,#8fd400)!important;border:0}
.btn.light:hover,.hire:hover,.viewc:hover{filter:brightness(1.06)}
.pin.solid,.pin.solid h3,.pin.solid .xnum,.pin.solid p{color:#fff!important}
.st,.hello,.mono.red{color:#c4a8ff!important}
#about .stat b{color:#fff!important}
.jyear,.mono,.visit,.chip,.cat,.lrow em,.shield,.logo i,.cnum,.issued small{color:#a07ff0!important}
.jyear{border-color:rgba(160,127,240,.5)!important}
.proj p,.jcard p,.lrow span,.pin p,.fface small,.certnote,.intronote,.sub{color:#c9c6d6!important}
.hero .shade{background:linear-gradient(90deg,rgba(5,5,7,.94) 0%,rgba(5,5,7,.76) 42%,rgba(5,5,7,.18) 100%),linear-gradient(180deg,rgba(5,5,7,.5),transparent 35%,transparent 65%,#050507 100%)!important}
.hero h1,.hero .kt,.hero .rot{color:#FAFAFA!important;text-shadow:0 2px 24px rgba(0,0,0,.6)}
.hero .rot{color:#c4a8ff!important}
.flabel{color:#e6e3f0!important;background:rgba(5,5,7,.55);border:1px solid rgba(255,255,255,.12);border-radius:10px;padding:8px 12px;backdrop-filter:blur(6px)}
.cue{color:#FAFAFA!important}.ainote{color:#c9c6d6!important;background:rgba(5,5,7,.55);padding:6px 10px;border-radius:8px}
.jquote,.jquote.glass{background:linear-gradient(180deg,#fff5b0,#ffe98a)!important;border:0!important}
.jquote p,.jquote footer{color:#3a2a00!important}
.note{color:#3a2a00!important}
.badge{background:#14131d;color:#FAFAFA;border:1px solid rgba(255,255,255,.14)}
.form input,.form textarea{background:#0b0a12!important;color:#FAFAFA!important;border-color:rgba(255,255,255,.14)!important}
.form input::placeholder,.form textarea::placeholder{color:#7d7a8c}
.consent{color:#c9c6d6}
nav .nlinks a{color:#d9d6e6}nav .nlinks a:hover{color:#fff}
.uline{background:#AAFF00!important}
.hero{background:#050507!important}
.pf b{color:#fff!important}.pf{color:rgba(255,255,255,.88)!important}
.fface,.fface h4,.fface .issued{color:#FAFAFA!important}
.fbot b,.fbot small,.vo{color:#a07ff0!important}
.cinfo .st,.cinfo b,.form .mono.red,.hello{color:#fff!important}
.pin.solid .xnum{color:#d9c7ff!important}
#about h2,#about .atext p{color:#fff!important}
.loomfacade{background:#14131d!important;color:#FAFAFA!important}
"""
s = s[:css_start] + css + OVERRIDES + s[css_end:]

left = [m for m in re.findall(r"Mark|Makati|Dianna|Kimpoy|Coggno|Bytown|markedcel", s)]
print("adapted; leftovers:", len(left), sorted(set(left)))
P.write_text(s, encoding="utf-8")
