# -*- coding: utf-8 -*-
"""Turn Mark's world engine (copied index.html) into Dedric's World. Idempotent: run on the fresh copy.
Every replacement asserts exactly one hit so a drift in the source is loud, not silent."""
import re, pathlib, json

P = pathlib.Path(__file__).parent / "index.html"
s = P.read_text(encoding="utf-8")
BASE = "https://referrernation-web.github.io/dedric/"
EMAIL, PHONE = "dedric.brown55@gmail.com", "470-262-7774"
LI, TB, CAL = "https://www.linkedin.com/in/dbrowntech", "https://www.salesforce.com/trailblazer/dbrown6422", "https://calendly.com/dbrowntech15/30min"
PDF = "../assets/Dedric-Brown-Resume-2026.pdf"


def one(old, new, flags=0, regex=False):
    global s
    if regex:
        m = re.findall(old, s, flags)
        assert len(m) == 1, (old[:60], len(m))
        s = re.sub(old, lambda _: new, s, count=1, flags=flags)
    else:
        assert s.count(old) == 1, (old[:60], s.count(old))
        s = s.replace(old, new)


# ---------------------------------------------------------------- head
JSONLD = json.dumps({"@context": "https://schema.org", "@graph": [
    {"@type": "Person", "@id": BASE + "#person", "name": "Dedric Brown", "jobTitle": "Senior Salesforce Product Manager",
     "email": "mailto:" + EMAIL, "telephone": "+1-" + PHONE, "address": {"@type": "PostalAddress", "addressLocality": "Atlanta", "addressRegion": "GA", "addressCountry": "US"},
     "url": BASE, "sameAs": [LI, TB, "https://thededricbrown.com/", "https://blazer2role.com/"], "worksFor": {"@type": "Organization", "name": "Centene Corporation"}},
    {"@type": "WebPage", "@id": BASE + "world/", "url": BASE + "world/", "name": "Dedric's World, 3D resume", "about": {"@id": BASE + "#person"}, "isPartOf": {"@id": BASE}}]}, ensure_ascii=False)
one(r"<title>.*?</script>", f"""<title>Dedric's World — ride the 3D resume of Dedric Brown</title>
<meta name="description" content="Interactive 3D resume of Dedric Brown, Senior Salesforce Product Manager: ride across Atlanta, San Francisco, Austin, St. Louis and Dreamforce to explore the roadmap work, the numbers and the credentials.">
<link rel="canonical" href="{BASE}world/">
<meta property="og:type" content="website"><meta property="og:title" content="Dedric's World — the 3D resume of Dedric Brown"><meta property="og:description" content="Ride with Rev across Atlanta, San Francisco, Austin, St. Louis and Dreamforce. Every landmark is one part of Dedric's resume: Salesforce CRM, GTM systems, Agentforce, with the numbers."><meta property="og:image" content="{BASE}world/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:url" content="{BASE}world/">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Dedric's World — 3D resume"><meta name="twitter:image" content="{BASE}world/og.jpg">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='30' fill='%236C2BD9'/%3E%3Ctext x='32' y='42' font-family='Arial,sans-serif' font-size='24' font-weight='900' fill='%23BFFF00' text-anchor='middle'%3EDB%3C/text%3E%3C/svg%3E">
<script type="application/ld+json">{JSONLD}</script>""", re.S, True)

# ---------------------------------------------------------------- seo text, hud, load card
one(r'<section class="seo".*?</section>', f"""<section class="seo" aria-label="Resume text version">
<h1>Dedric Brown — Senior Salesforce Product Manager, GTM Systems and Agentforce (Atlanta, GA)</h1>
<p>Interactive 3D resume. Each landmark is one section. <a href="../">Classic resume</a> · <a href="{PDF}">Resume PDF</a> · <a href="{LI}">LinkedIn</a> · <a href="{TB}">Trailblazer</a>.</p>
<h2>Atlanta — About</h2><p>Senior product and platform leader with 8+ years owning product vision, strategy, roadmaps and end-to-end delivery for enterprise Salesforce CRM, go-to-market systems, revenue operations, identity, healthcare and AI automation.</p>
<h2>Peachtree Road — Journey</h2><ul><li>2018–2020 Product Manager, CRM Platforms, NCR Corporation: $1.8M+ cost savings, 2M+ records migrated with zero downtime</li><li>2020–2021 Product Manager, Identity and Security, Salesforce: SSO/MFA across 8,000+ users, access incidents down 40%</li><li>2021–2023 Product Manager, Customer Platforms, Salesforce: $15M+ retained, $10M+ renewal book</li><li>2023–2026 Product Manager, GTM Business Systems, Cloudflare: $150M+ pipeline roadmap, NetSuite ERP integration, time-to-insight down 40%</li><li>2026– Senior Salesforce Product Manager, Centene: Health Cloud, Agentforce governance, NPI-keyed provider identity</li></ul>
<h2>San Francisco — Expertise</h2><ul><li>Product strategy and roadmap ownership</li><li>CRM and ERP systems integration (Salesforce to NetSuite)</li><li>GTM and revenue operations</li><li>Agentforce and AI automation with governance</li></ul>
<h2>Austin — Stack</h2><p>Sales Cloud, Service Cloud, Health Cloud, Marketing Cloud, OmniStudio / Vlocity, Agentforce, Einstein, Flow Builder, NetSuite ERP, APIs, IAM, SSO, MFA, HIPAA, SAFe, Scrum.</p>
<h2>Blazer2Role Boardwalk — Videos</h2><p>Approved talks: Called When It Breaks, Why Tech parts 1–5, Entry-Level Now Means You. blazer2role.com.</p>
<h2>Dreamforce — Certifications (14)</h2><p>Agentforce Specialist, AI Associate, Agentforce Sales Consultant, Platform Strategy Designer, Business Analyst, Platform Administrator II, Platform Foundations, Agentforce Service Consultant, Platform Administrator, SAFe 6 POPM, Certified ScrumMaster, Google AI Essentials, CompTIA Security+, Trailhead Security Specialist Superbadge.</p>
<h2>St. Louis — Contact</h2><p>Open to senior product roles, Atlanta or remote across the US. <a href="mailto:{EMAIL}">{EMAIL}</a> · {PHONE} · <a href="{CAL}">Book a call</a>.</p>
</section>""", re.S, True)
one('<div id="hud"><b>Mark <span>Edcel</span></b><small>Full-Stack Dev · SEO · AEO<br>Makati → US · CA · AU</small></div>',
    '<div id="hud"><b>Dedric <span>Brown</span></b><small>Senior Salesforce PM · Agentforce<br>Atlanta → remote US</small></div>')
one('<span id="stLoc">MANILA</span>', '<span id="stLoc">ATLANTA</span>')
one('H center on Kimpoy · B bark', 'H center on Rev · B honk')
one(r'<div id="load"><div class="card">\n<h1>.*?</p>', """<div id="load"><div class="card">
<h1>Dedric's <span>World</span></h1>
<p>Ride Rev, the Blazer2Role mascot, across the cities where Dedric built his career. Every landmark is one part of the resume. Drive in and the sign opens. Knock over the letters, bowl the pins, kick the crates.</p>""", re.S, True)

# ---------------------------------------------------------------- panels
DATA = r"""var DATA={
home:{k:'ATLANTA · HOME',t:'Hi, I’m Dedric Brown',h:'<p>Senior product manager for Salesforce CRM, go-to-market systems and Agentforce. Eight-plus years across NCR, Salesforce, Cloudflare and now Centene, turning fragmented, manual processes into governed, automated platforms with numbers Finance signs off on.</p><div class="stat"><div><b>$150M+</b><small>annual pipeline · Sales Cloud roadmap · Cloudflare</small></div><div><b>$15M+</b><small>enterprise contracts retained · Salesforce</small></div><div><b>40%</b><small>faster time-to-insight · 12+ teams</small></div><div><b>8,000+</b><small>users on SSO / MFA · incidents down 40%</small></div></div><p>Ride to each landmark: <b>Peachtree Road</b> (journey), <b>San Francisco</b> (expertise), <b>Austin</b> (stack), <b>Boardwalk</b> (videos), <b>Dreamforce</b> (credentials), <b>St. Louis</b> (contact).</p><a class="cta" href="#" data-go="contact">Hire me</a><a class="cta alt2" href="PDFPATH" target="_blank" rel="noopener">Resume PDF</a><a class="cta alt2" href="../">Classic resume</a>'},
journey:{k:'PEACHTREE ROAD · JOURNEY',t:'From CRM records to the AI roadmap',h:'<p>“Every role was the same knot in a bigger company: two teams, two systems, no shared truth. Untie it, then automate on top of data that can carry it.”</p><ul class="tl"><li><i>2018–2020</i><b>Product Manager, CRM Platforms · NCR</b>Sales Cloud modernization: $1.8M+ cost savings, 2M+ legacy records migrated with zero downtime, data accuracy up 35%.</li><li><i>2020–2021</i><b>Product Manager, Identity &amp; Security · Salesforce</b>SSO and MFA across 8,000+ users on $25M+ of regulated contracts. Access incidents down 40%, 10+ critical findings closed.</li><li><i>2021–2023</i><b>Product Manager, Customer Platforms · Salesforce</b>Vlocity / OmniStudio and Marketing Cloud roadmap. $15M+ retained, $10M+ renewal book, lead gen up 35%.</li><li><i>2023–2026</i><b>Product Manager, GTM Business Systems · Cloudflare</b>Sales Cloud roadmap behind $150M+ pipeline. NetSuite ERP integration, time-to-insight down 40%, adoption up 35%.</li><li><i>2026–</i><b>Senior Salesforce Product Manager · Centene</b>Health Cloud roadmap for specialty pharmacy. Agentforce governance, NPI-keyed provider identity, HIPAA-ready controls.</li></ul><p>BA, Business Administration, Morris Brown College, Atlanta.</p>'},
expertise:{k:'SAN FRANCISCO · EXPERTISE',t:'Four things I do, one tower',h:'<h4>01 Product Strategy &amp; Roadmap Ownership</h4><p>Vision, portfolio intake, business cases, prioritization, acceptance criteria, release plans and post-launch measurement.</p><h4>02 CRM &amp; ERP Systems Integration</h4><p>Salesforce to NetSuite across opportunity-to-order, order-to-cash, billing, invoicing and revenue recognition. One system of record.</p><h4>03 GTM &amp; Revenue Operations</h4><p>Lead-to-opportunity, pipeline, forecasting, marketing automation, renewals, KPI definition and the dashboards Finance adopts.</p><h4>04 Agentforce &amp; AI Automation</h4><p>Agentforce and Einstein use cases gated by process mapping, data readiness, human-in-the-loop controls and AI governance.</p>'},
skills:{k:'AUSTIN · THE STACK',t:'What runs the roadmap',h:'<h4>Salesforce &amp; platforms</h4><div class="tags"><span>Sales Cloud</span><span>Service Cloud</span><span>Health Cloud</span><span>Marketing Cloud</span><span>OmniStudio / Vlocity</span><span>Agentforce</span><span>Einstein</span><span>Flow Builder</span><span>NetSuite ERP</span></div><h4>Agentic AI</h4><div class="tags"><span>Agentforce design</span><span>Predictive models</span><span>LLMs &amp; prompts</span><span>Claude API</span><span>AI readiness</span><span>Human-in-the-loop</span></div><h4>Product &amp; RevOps</h4><div class="tags"><span>Roadmaps</span><span>Discovery</span><span>User research</span><span>Sprint planning</span><span>UAT &amp; release</span><span>Forecasting</span><span>Order-to-cash</span><span>KPI dashboards</span></div><h4>Security &amp; compliance</h4><div class="tags"><span>IAM</span><span>SSO / MFA</span><span>HIPAA</span><span>Audit readiness</span><span>Managed care</span></div>'},
projects:{k:'BLAZER2ROLE BOARDWALK · VIDEOS',t:'The talks Dedric approved',h:''},
certs:{k:'DREAMFORCE · CREDENTIALS',t:'14 credentials, 9 from Salesforce',h:'<p>Official names as of the July 2026 rename; prior names noted. Verify on the <a href="TBURL" target="_blank" rel="noopener">Trailblazer profile</a>.</p><h4>Salesforce</h4><p>Agentforce Specialist (formerly AI Specialist) · AI Associate · Agentforce Sales Consultant (formerly Sales Cloud Consultant) · Platform Strategy Designer (formerly Strategy Designer) · Business Analyst · Platform Administrator II (formerly Advanced Administrator) · Platform Foundations (formerly Salesforce Associate) · Agentforce Service Consultant (formerly Service Cloud Consultant) · Platform Administrator (formerly Administrator)</p><h4>Agile &amp; delivery</h4><p>SAFe 6 Product Owner / Product Manager · Certified ScrumMaster</p><h4>AI &amp; security</h4><p>Google AI Essentials · CompTIA Security+ · Trailhead Security Specialist Superbadge</p><p>Click a banner on the stage to open the profile.</p>'},
contact:{k:'ST. LOUIS · CONTACT',t:'Let’s talk about your roadmap',h:'<p><b>Status:</b> open to senior product roles.<br><b>Region:</b> Atlanta, GA · remote across the US.</p><p><b>EMAILADDR</b><br>PHONENUM</p><form class="form" action="https://formsubmit.co/EMAILADDR" method="POST" target="_blank"><input type="hidden" name="_subject" value="Dedric&#39;s World contact"><label>NAME</label><input name="name" required placeholder="Your name"><label>EMAIL</label><input name="email" type="email" required placeholder="you@company.com"><label>MESSAGE</label><textarea name="message" required placeholder="The role, the platform, the problem."></textarea><button class="cta" type="submit">Send message</button></form><a class="cta alt2" href="CALURL" target="_blank" rel="noopener">Book a 30-minute call</a><a class="cta alt2" href="PDFPATH" target="_blank" rel="noopener">Download resume (PDF)</a><a class="cta alt2" href="mailto:EMAILADDR">Email</a><a class="cta alt2" href="LIURL" target="_blank" rel="noopener">LinkedIn</a><a class="cta alt2" href="TBURL" target="_blank" rel="noopener">Trailblazer</a>'}
};
""".replace("PDFPATH", PDF).replace("EMAILADDR", EMAIL).replace("PHONENUM", PHONE).replace("CALURL", CAL).replace("LIURL", LI).replace("TBURL", TB)
one(r"var DATA=\{\n.*?\n\};\n", DATA, re.S, True)

PROJECTS = r"""var PROJECTS=[
['Called When It Breaks','hero','The welcome video. You are the one they call when it breaks; that is not a job title, that is a career.','../video/hero.mp4',['31s','approved welcome video','Dedric, Sept 2026']],
['Why Tech, Part 1','whytech1','Thinking about a career in tech but not sure it is for you?','../video/whytech1.mp4',['1 / 5','Why Tech series','published Sept 1, 2026']],
['Why Tech, Part 2','whytech2','Feeling stuck in a job that pays the bills but not much else?','../video/whytech2.mp4',['2 / 5','Why Tech series','published Sept 1, 2026']],
['Why Tech, Part 3','whytech3','No degree? No experience? Here is what tech actually asks for.','../video/whytech3.mp4',['3 / 5','Why Tech series','published Sept 2, 2026']],
['Why Tech, Part 4','whytech4','The tech industry does not care where you started.','../video/whytech4.mp4',['4 / 5','Why Tech series','published Sept 2, 2026']],
['Why Tech, Part 5','whytech5','Ready to make the jump? Start with the free resume scorer.','../video/whytech5.mp4',['5 / 5','Why Tech series','published Sept 3, 2026']],
['Entry-Level Now Means You','topic01','PwC counted: AI-exposed entry-level roles are seven times more likely to ask for senior judgment.','../video/topic01.mp4',['7x','more likely to ask for senior skills','PwC AI Jobs Barometer 2026']]];
"""
one(r"var PROJECTS=\[\n.*?\]\]\];\n", PROJECTS, re.S, True)
one(r"DATA\.projects\.h=.*?\n",
    "DATA.projects.h=PROJECTS.map(function(p){return '<div class=\"pj\"><img src=\"../assets/img/thumb-'+p[1]+'.webp\" alt=\"\"><div><b>'+p[0]+'</b><small>'+p[2]+'</small><a href=\"'+p[3]+'\" target=\"_blank\" rel=\"noopener\">Play ↗</a></div></div>'}).join('')+'<p>All seven were approved by Dedric before they went out. More at <a href=\"https://blazer2role.com\" target=\"_blank\" rel=\"noopener\">blazer2role.com</a>.</p><a class=\"cta alt2\" href=\"https://blazer2role.com/#resume-scorer\" target=\"_blank\" rel=\"noopener\">Free resume scorer ↗</a>';\n",
    re.S, True)
# thumbnails: hero poster is named hero-poster
s = s.replace("'../assets/img/thumb-'+p[1]+'.webp'", "'../assets/img/'+(p[1]==='hero'?'hero-poster':'thumb-'+p[1])+'.webp'")

# ---------------------------------------------------------------- stations
one(r"var ST=\[\n.*?\}\];\n", """var ST=[
{id:'home',n:'Atlanta',x:0,z:0,r:16},
{id:'journey',n:'Peachtree Road',x:-78,z:-30,r:20},
{id:'expertise',n:'San Francisco',x:80,z:-40,r:22},
{id:'skills',n:'Austin',x:20,z:-95,r:16},
{id:'projects',n:'Boardwalk',x:-10,z:88,r:26},
{id:'certs',n:'Dreamforce',x:-80,z:50,r:18},
{id:'contact',n:'St. Louis',x:85,z:60,r:18}];
""", re.S, True)

# ---------------------------------------------------------------- landmarks (primitives only; kit.glb dressing stays)
BUILD = r"""function buildWorld(){
 var EIF=null;window.EIF=EIF;
 // ---------- ATLANTA: Peachtree skyline (Bank of America Plaza spire, Westin cylinder), Centene + NCR towers, MARTA car, peach tree ----------
 var h0=ground(0,0);mbStart();
 [[-14,-16,3,9,0xdedbd3],[-8,-19,3.4,13,0xcfd6dd],[3,-20,3,11,0xe6e2da],[12,-16,2.8,8,0xd8d2c8],[-19,-8,2.6,7,0xe0dcd4],[19,-22,3.2,15,0xc9d2da]].forEach(function(t){tower(t[0],t[1],t[2],t[3],t[4])});
 mp(BX(3.6,18,3.6),0xc9b58a,-2,h0+9,-28);mp(CN(1.6,9,4),0xe8c35a,-2,h0+22.5,-28);COL.push({x:-2,z:-28,r:2.6});SHB.push([-2,-28,2.6,18]);      // Bank of America Plaza: gold lattice spire
 mp(CY(2.2,2.2,16,18),0x9fb3c8,24,h0+8,-30);mp(CY(2.6,2.6,.6,18),0x4a5560,24,h0+16.3,-30);COL.push({x:24,z:-30,r:2.4});SHB.push([24,-30,2.4,16]);  // Westin Peachtree Plaza cylinder
 vehicle(-6,6,.4,0xe8c35a,4.6);   // MARTA-style car
 mp(BX(3.2,2.2,2.6),0xf4e2c0,-16,h0+1.1,4);mp(BX(3.6,.2,1.2),0x6C2BD9,-16,h0+2.3,5.6);mp(BX(3.6,.2,1.2),0xffffff,-16,h0+2.32,5.0);mp(BX(2.6,.9,.3),0x8a6a3a,-16,h0+.9,5.35);COL.push({x:-16,z:4,r:2});SHB.push([-16,4,2,2.4]);   // coffee stand
 mbEnd();mbStart();
 mp(CY(.35,.5,3,7),0x7a4b2a,-13,h0+1.5,-5);mp(SP(2.4),0x5aa63c,-13,h0+4.6,-5);for(var pc=0;pc<7;pc++){var pa=pc*.9;mp(SP(.28),0xf29b5b,-13+Math.cos(pa)*2.1,h0+4.4+Math.sin(pa*2)*.9,-5+Math.sin(pa)*2.1)}COL.push({x:-13,z:-5,r:1.2});SHB.push([-13,-5,2.4,5]);   // the peach tree
 mbEnd();
 label('ATLANTA',0,h0+20,-8,'HOME · start here',1.4);
 sign(4,4,['← Peachtree Rd W','San Francisco E →','Austin N ↑','Boardwalk S ↓']);
 lampsAround(0,0,10,6);
 // ---------- PEACHTREE ROAD: five milestones on a hill road, one office per role ----------
 var s=ST[1],y=ground(s.x,s.z);mbStart();
 for(var i=0;i<5;i++){var r=14.5-i*2.1;mp(CY(r-.4,r,1.1,26),i%2?0x3d3a52:0x4a4664,s.x,y+.55+i*1.1,s.z,0,i*.4);mp(CY(r-.2,r-.2,.22,26),0x2a2838,s.x,y+i*1.1,s.z,0,i*.4)}   // terraced hill
 var ROLES=[['NCR','2018',0x6a7d9a],['SALESFORCE','2020',0x2f8fd6],['SALESFORCE','2021',0x2f8fd6],['CLOUDFLARE','2023',0xf38020],['CENTENE','2026',0x8a55f0]];
 ROLES.forEach(function(rl,i){var a=-1.2+i*.62,rx=s.x+Math.cos(a)*11,rz=s.z+Math.sin(a)*11,ry=ground(rx,rz);mp(BX(2.6,2.2+i*.9,2.6),rl[2],rx,ry+1.1+i*.45,rz,0,-a);mp(BX(2.9,.25,2.9),0xffffff,rx,ry+2.35+i*.9,rz,0,-a);COL.push({x:rx,z:rz,r:1.8});SHB.push([rx,rz,1.9,3+i]);label(rl[0],rx,ry+4.6+i*.9,rz,rl[1],.75)});
 mp(CY(2.2,2.6,1.2,10),0x6C2BD9,s.x,y+6.1,s.z);mp(CN(1.4,2.6,6),0xBFFF00,s.x,y+8,s.z);   // summit marker
 mbEnd();
 SHB.push([s.x,s.z,15.5,7]);COL.push({x:s.x,z:s.z,r:3});label('PEACHTREE ROAD',s.x,y+13,s.z,'JOURNEY · five roles',1.3);
 for(var a=0;a<10;a++){var ang=a*.63;tree(s.x+Math.cos(ang)*(19+a%3*2),s.z+Math.sin(ang)*(19+a%3*2),.8)}
 // ---------- SAN FRANCISCO: Salesforce Tower (tapered, crown), Golden Gate span, Transamerica, cable car ----------
 s=ST[2];y=ground(s.x,s.z);mbStart();
 for(var f=0;f<9;f++){var fr=4.2-f*.3;mp(CY(fr-.3,fr,3.2,22),f%2?0xb9c6d6:0xc9d4e2,s.x,y+1.6+f*3.2,s.z)}mp(CY(1.4,1.9,2.4,22),0xdfe7f0,s.x,y+30.2,s.z);   // Salesforce Tower
 for(var q=0;q<12;q++){var qa=q/12*Math.PI*2;mp(BX(.18,1.6,.18),0xBFFF00,s.x+Math.cos(qa)*1.55,y+30.4,s.z+Math.sin(qa)*1.55)}LAMPS.push([s.x,y+31,s.z,.75,1,0]);
 SHB.push([s.x,s.z,4.4,31]);COL.push({x:s.x,z:s.z,r:4.3});
 mp(CN(2.2,14,4),0xd9d2c4,s.x+12,y+7,s.z-9);COL.push({x:s.x+12,z:s.z-9,r:2});SHB.push([s.x+12,s.z-9,2.2,14]);   // Transamerica pyramid
 var gx=s.x-4,gz=s.z+16;[[gx-9,gz],[gx+9,gz]].forEach(function(tp){mp(BX(1.2,12,1.2),0xc0392b,tp[0],ground(tp[0],tp[1])+6,tp[1]);mp(BX(2.4,.5,1.4),0xc0392b,tp[0],ground(tp[0],tp[1])+8,tp[1]);mp(BX(2.4,.5,1.4),0xc0392b,tp[0],ground(tp[0],tp[1])+11.6,tp[1]);COL.push({x:tp[0],z:tp[1],r:1})});
 mp(BX(24,.4,3),0xc0392b,gx,ground(gx,gz)+4.2,gz);for(var c=0;c<13;c++){var cx0=gx-9+c*1.5,sag=4.2+Math.abs(c-6)*.9;mp(BX(.1,sag-4.2+.2,.1),0xc0392b,cx0,ground(cx0,gz)+4.2+(sag-4.2)/2,gz)}   // Golden Gate deck + cables
 var cc=s.x-12,cz=s.z-4;mp(BX(3.6,1.4,1.8),0x8a1f1f,cc,ground(cc,cz)+1.3,cz,0,.3);mp(BX(3.8,.3,2),0xf0e2b8,cc,ground(cc,cz)+2.1,cz,0,.3);COL.push({x:cc,z:cz,r:2});   // cable car
 mbEnd();
 label('SAN FRANCISCO',s.x,y+36,s.z,'EXPERTISE · Salesforce years',1.3);for(var a=0;a<6;a++)tree(s.x-16+a*6,s.z+24,.7);lampsAround(s.x,s.z,9,4);
 // ---------- AUSTIN: Cloudflare data hall (rack rows with lime LEDs), Capitol dome, food truck ----------
 s=ST[3];y=ground(s.x,s.z);mbStart();
 mp(BX(22,.3,16),0x2a2838,s.x,y+.15,s.z);
 for(var rw=0;rw<3;rw++)for(var rk=0;rk<6;rk++){var rx2=s.x-10+rk*4,rz2=s.z-5+rw*5;mp(BX(2.2,4.2,1.1),0x1c1b26,rx2,y+2.4,rz2);mp(BX(2.3,.08,1.15),0x3a3850,rx2,y+4.5,rz2);for(var led=0;led<5;led++)mp(BX(.14,.14,.05),(led+rk)%3?0xBFFF00:0x6C2BD9,rx2-.8+led*.4,y+1.2+led*.6,rz2+.58);if(rk===0&&rw===1)LAMPS.push([rx2,y+2.4,rz2+1,.75,1,0]);COL.push({x:rx2,z:rz2,r:1.2});SHB.push([rx2,rz2,1.3,4.4])}
 var kx=s.x+16,kz=s.z-10,ky=ground(kx,kz);mp(BX(8,5,6),0xf1e4d0,kx,ky+2.5,kz);mp(CY(2.6,2.6,3,18),0xf1e4d0,kx,ky+6.5,kz);mp(SP(2.7),0xe8dcc2,kx,ky+8.5,kz);mp(CN(.5,2,6),0xd9c9a8,kx,ky+12.2,kz);COL.push({x:kx,z:kz,r:4.4});SHB.push([kx,kz,4.4,13]);   // Texas Capitol dome
 vehicle(s.x-14,s.z+10,1.1,0xf38020,4.4);
 mbEnd();
 label('AUSTIN',s.x,y+14,s.z,'THE STACK · GTM systems',1.3);lampsAround(s.x,s.z,12,4);
 // ---------- BOARDWALK: the approved videos on boards, receipts, umbrellas, lifeguard tower ----------
 s=ST[4];var bx=s.x-24;for(var i=0;i<PROJECTS.length;i++){board(bx+i*8,s.z-6,0,PROJECTS[i][0],PROJECTS[i][1]);receipt(bx+i*8,s.z-12,PROJECTS[i][4])}
 for(var a=0;a<9;a++)palm(s.x-28+a*7,s.z+8);
 mbStart();
 for(var k=0;k<4;k++){var ux=s.x+4+k*5,uz=s.z+6,uy=ground(ux,uz);mp(CY(.05,.05,2.6,5),0x777777,ux,uy+1.3,uz);mp(CN(1.5,.6,8),k%2?0x6C2BD9:0xBFFF00,ux,uy+2.8,uz);mp(BX(1.4,.25,.6),0xfbf7f1,ux+.6,uy+.2,uz+.8)}
 var lx=s.x+22,lz=s.z-2,ly=ground(lx,lz);[[-.9,-.9],[.9,-.9],[-.9,.9],[.9,.9]].forEach(function(p){mp(CY(.1,.12,3.2,5),0xe8dcc2,lx+p[0],ly+1.6,lz+p[1])});mp(BX(2.6,.2,2.6),0xe8dcc2,lx,ly+3.3,lz);mp(BX(2.2,1.4,2),0xffffff,lx,ly+4.1,lz);mp(CN(2,1,4),0x6C2BD9,lx,ly+5.3,lz,0,Math.PI/4);COL.push({x:lx,z:lz,r:1.8});SHB.push([lx,lz,1.8,5]);
 mbEnd();
 label('BLAZER2ROLE BOARDWALK',s.x,ground(s.x,s.z)+12,s.z,'VIDEOS · 7 boards',1.3);
 // ---------- DREAMFORCE: keynote stage, ring of banner masts (certs), screens, campfire ----------
 s=ST[5];y=ground(s.x,s.z);mbStart();
 mp(CY(14,14.5,.5,32),0x2a2838,s.x,y+.25,s.z);
 mp(BX(12,1.2,7),0x1c1b26,s.x,y+1.1,s.z-3);mp(BX(12.4,.2,7.4),0x6C2BD9,s.x,y+1.8,s.z-3);mp(BX(11,6,.6),0x14131d,s.x,y+4.8,s.z-6.5);mp(BX(10.2,4.6,.1),0x8a55f0,s.x,y+4.9,s.z-6.1);mp(BX(4.6,2.2,.06),0xBFFF00,s.x,y+5.6,s.z-6.0);COL.push({x:s.x,z:s.z-3,r:6.5});SHB.push([s.x,s.z-3,6.5,8]);   // stage + LED wall
 for(var a=0;a<28;a++){var ang=a/28*Math.PI*2;mp(CY(.12,.14,8,6),0xd9d2c4,s.x+Math.cos(ang)*14.4,y+4,s.z+Math.sin(ang)*14.4);COL.push({x:s.x+Math.cos(ang)*14.4,z:s.z+Math.sin(ang)*14.4,r:.5})}   // banner masts
 for(var rw2=0;rw2<4;rw2++)for(var st=0;st<8;st++){mp(BX(.9,.5,.9),rw2%2?0x3d3a52:0x4a4664,s.x-5+st*1.4,y+.75+rw2*.35,s.z+3+rw2*1.4)}   // seating
 var cfx=s.x+11,cfz=s.z+10;mp(CY(1.2,1.4,.3,10),0x555555,cfx,ground(cfx,cfz)+.15,cfz);mp(CN(.5,1.1,6),0xf29b5b,cfx,ground(cfx,cfz)+.8,cfz);LAMPS.push([cfx,ground(cfx,cfz)+1,cfz,1,.6,.2]);   // campfire
 mbEnd();
 SHB.push([s.x,s.z,12.6,7]);label('DREAMFORCE',s.x,y+16,s.z,'CREDENTIALS · 14',1.3);
 // ---------- ST. LOUIS: Gateway Arch, Centene tower, riverboat, mailbox ----------
 s=ST[6];y=ground(s.x,s.z);mbStart();
 for(var seg=0;seg<28;seg++){var t0=seg/28,t1=(seg+1)/28,ax0=s.x+(t0-.5)*26,ax1=s.x+(t1-.5)*26,ah0=Math.sin(t0*Math.PI)*22,ah1=Math.sin(t1*Math.PI)*22;var mx2=(ax0+ax1)/2,my2=(ah0+ah1)/2,dl=Math.hypot(ax1-ax0,ah1-ah0),rz=Math.atan2(ah1-ah0,ax1-ax0);mp(BX(dl+.3,1.3-Math.sin(t0*Math.PI)*.6,1.3-Math.sin(t0*Math.PI)*.6),0xcfd6dd,mx2,y+my2,s.z-2,0,0,rz)}   // Gateway Arch (catenary of boxes)
 COL.push({x:s.x-12.5,z:s.z-2,r:1.2});COL.push({x:s.x+12.5,z:s.z-2,r:1.2});SHB.push([s.x,s.z-2,13,22]);
 for(var a=0;a<7;a++){var cx2=s.x-14+a*4.5,cz2=s.z-16-(a%2)*3,th2=6+((a*7)%10),cy2=ground(cx2,cz2);mp(BX(3,th2,3),a%3?0x8d99a6:0x7c8896,cx2,cy2+th2/2,cz2);mp(BX(2.2,th2*.35,2.2),0x9aa6b3,cx2,cy2+th2+th2*.17,cz2);for(var f2=1;f2<th2/1.3;f2++){mp(BX(3.06,.3,1.2),0x2c3e50,cx2,cy2+f2*1.3,cz2+.9)}SHB.push([cx2,cz2,2.3,th2]);COL.push({x:cx2,z:cz2,r:2.1})}
 mp(BX(3.4,20,3.4),0x8a55f0,s.x+16,ground(s.x+16,s.z-14)+10,s.z-14);mp(BX(3.8,.6,3.8),0xBFFF00,s.x+16,ground(s.x+16,s.z-14)+20.3,s.z-14);COL.push({x:s.x+16,z:s.z-14,r:2.5});SHB.push([s.x+16,s.z-14,2.6,20]);label('CENTENE',s.x+16,ground(s.x+16,s.z-14)+23,s.z-14,'2026 · Health Cloud',.8);
 mp(BX(1,1.4,.7),0x2f8fd6,s.x-3,y+1.3,s.z+13);mp(CY(.08,.08,1,6),0x555555,s.x-3,y+.5,s.z+13);   // mailbox
 vehicle(s.x-8,s.z+6,1.2,0xf4c430,4);
 mbEnd();
 label('ST. LOUIS',s.x,y+26,s.z,'CONTACT · hire me',1.3);lampsAround(s.x,s.z,12,5);
 // ---------- scenery: trees, rocks ----------
 for(var i=0;i<170;i++){var x=(Math.random()-.5)*230,z=(Math.random()-.5)*230;if(Math.hypot(x,z)<18)continue;var near=ST.some(function(s){return Math.hypot(x-s.x,z-s.z)<s.r+2});if(near)continue;if(hgt(x,z)<1.3)continue;if(x>60&&z<-10)rock(x,z,1+Math.random()*1.5);else tree(x,z,.7+Math.random()*.8)}
 dress([['bench',6,10,1.6],['bench',-7,12,.4],['planter',9,7,0,0,1.1],['planter',-9,7,0,0,1.1],['bollard',11,3,0],['bollard',11,6,0],
  ['busstop',-12,14,1.2,0xfbf7f1,1,1.6],['stall',22,2,-.5,0,1,1.2],['shop_a',-20,-3,1.57,0xe6e2da,1,2.2],['shop_b',-20,3,1.57,0xd8d2c8,1,1.9],
  ['mid_a',27,-6,0,0xcfd6dd,1,2.4],['mid_a',-17,-13,.6,0xdedbd3,1,2.4],['car2',8,-14,1.1,0x6C2BD9],['tree2',5,16,0],['tree2',-5,17,0],
  ['bench',ST[6].x-4,ST[6].z+6,0],['bench',ST[6].x+4,ST[6].z+6,3.14],['planter',ST[6].x-8,ST[6].z+5,0,0,1.2],['planter',ST[6].x+8,ST[6].z+5,0,0,1.2],
  ['busstop',ST[6].x-13,ST[6].z+4,1.57,0xfbf7f1,1,1.6],['bollard',ST[6].x-2,ST[6].z+9,0],['bollard',ST[6].x+2,ST[6].z+9,0],
  ['mid_a',ST[6].x-19,ST[6].z-4,0,0x8d99a6,1,2.4],['mid_a',ST[6].x+14,ST[6].z-2,.4,0x9aa6b3,1,2.4],['car2',ST[6].x+7,ST[6].z+12,2.2,0x6C2BD9]]);
}
"""
one(r"function buildWorld\(\)\{\n.*?\n\}\nfunction dress\(", BUILD + "function dress(", re.S, True)
one("var EIF,", "var _EIFunused,") if "var EIF," in s else None
one("if(EIF&&!EIF.on&&Math.hypot(P.x-EIF.x,P.z-EIF.z)<110){EIF.on=true;placeModel('eiffel.glb',EIF.x,EIF.z,36,'h',0)}", "")
# SP() helper must exist (used above) — Mark's file defines SP alongside BX/CY/CN
assert "function SP(" in s or "SP=function" in s or re.search(r"function SP\(", s), "SP helper missing"

# ---------------------------------------------------------------- certs banners, voice lines, pads, letters
one(r"var CERTS=\[\[.*?\]\];\n", "var CERTS=" + json.dumps([
    ["SALESFORCE", "Agentforce Specialist", "formerly AI Specialist · Oct 2024", TB], ["SALESFORCE", "AI Associate", "Oct 2024", TB],
    ["SALESFORCE", "Agentforce Sales Consultant", "formerly Sales Cloud Consultant · Apr 2023", TB], ["SALESFORCE", "Platform Strategy Designer", "formerly Strategy Designer · Apr 2023", TB],
    ["SALESFORCE", "Business Analyst", "Jan 2023", TB], ["SALESFORCE", "Platform Administrator II", "formerly Advanced Administrator · Sep 2022", TB],
    ["SALESFORCE", "Platform Foundations", "formerly Salesforce Associate · Sep 2022", TB], ["SALESFORCE", "Agentforce Service Consultant", "formerly Service Cloud Consultant · Dec 2021", TB],
    ["SALESFORCE", "Platform Administrator", "formerly Administrator · Oct 2020", TB], ["SCALED AGILE", "SAFe 6 Product Owner / Product Manager", "Jun 2024", LI],
    ["SCRUM ALLIANCE", "Certified ScrumMaster (CSM)", "Jan 2023", LI], ["GOOGLE", "Google AI Essentials", "Coursera · Jun 2026", LI],
    ["COMPTIA", "Security+", "CompTIA", LI], ["TRAILHEAD", "Security Specialist Superbadge", "Salesforce Trailhead", TB]], ensure_ascii=False) + ";\n", re.S, True)
one(r"var VOT=\{.*?\};\n", """var VOT={home:"Welcome to Atlanta. I'm Dedric Brown, senior Salesforce product manager. Ride Rev to any landmark and I'll show you the roadmap work behind the numbers.",journey:"Peachtree Road. Five roles, one habit: find the knot between two teams and two systems, then build the system of record they both trust. NCR, Salesforce twice, Cloudflare, and now Centene.",expertise:"San Francisco. Four things I do: product strategy and roadmap ownership, CRM and ERP integration, GTM and revenue operations, and Agentforce with governance that survives an audit.",skills:"Austin. This is the stack behind the roadmap: Sales Cloud, Health Cloud, OmniStudio, Agentforce, NetSuite, and the identity and compliance layer underneath.",projects:"The boardwalk. Seven talks Dedric approved: the welcome video, the five-part Why Tech series, and Entry-Level Now Means You. Press Enter on any board to play it.",certs:"Dreamforce. Fourteen credentials on the banners, nine of them from Salesforce, including Agentforce Specialist. Click a banner to open the Trailblazer profile.",contact:"St. Louis. If you need a product manager who makes Salesforce pay for itself, this is the stop. Book a call, or press Enter on a pad."};
""", re.S, True)
one("""[['EMAIL','mailto:markedcel06@gmail.com'],['LINKEDIN','https://www.linkedin.com/in/mark-edcel-lopez-513509216/'],['ONLINEJOBS.PH','https://www.onlinejobs.ph/jobseekers/info/4576592'],['GITHUB','https://github.com/referrernation-web']]""",
    f"""[['EMAIL','mailto:{EMAIL}'],['LINKEDIN','{LI}'],['TRAILBLAZER','{TB}'],['BOOK A CALL','{CAL}']]""")
one("window.open('../assets/Mark-Edcel-Lopez-Resume-2026.pdf','_blank','noopener')", f"window.open('{PDF}','_blank','noopener')")
one("['M','A','R','K'].forEach(function(ch,i){addProp('box',-4.5+i*3,4,{ch:ch})});", "['D','E','D','R','I','C'].forEach(function(ch,i){addProp('box',-7.5+i*3,4,{ch:ch})});")
# OPEN pads on the boardwalk play the video instead of opening a site
one("pad(bx+i*8,s.z-1.2,2.4,1.4,'OPEN '+pj[0].toUpperCase(),function(){window.open(pj[3],'_blank','noopener')})",
    "pad(bx+i*8,s.z-1.2,2.4,1.4,'PLAY '+pj[0].toUpperCase(),function(){window.open(pj[3],'_blank','noopener')})")

# ---------------------------------------------------------------- figures: procedural placeholders, no texture files
one("var FURM=new THREE.MeshStandardMaterial({map:TEX('kimpoy-fur.jpg',1.2),roughness:1,metalness:0});",
    "var FURM=new THREE.MeshStandardMaterial({color:0x6C2BD9,roughness:.55,metalness:.05});")
one("var SHELLM=window.SHELLM=new THREE.MeshStandardMaterial({map:TEX('fur-shell.png',2.4),transparent:true,alphaTest:.3,depthWrite:false,roughness:1,side:THREE.DoubleSide,color:0x8a847a});",
    "var SHELLM=window.SHELLM=new THREE.MeshStandardMaterial({transparent:true,opacity:.22,depthWrite:false,roughness:1,side:THREE.DoubleSide,color:0x8a55f0});")
one("var HEADM=new THREE.MeshStandardMaterial({map:TEX('kimpoy-head.jpg',1,false),roughness:1,metalness:0});",
    "var HEADM=new THREE.MeshStandardMaterial({color:0x8a55f0,roughness:.5,metalness:.05});")
# Rev's lime visor + two eyes on the head front (+z), instead of a snout photo
one("var snout=fs(.24,0,1.48,1.42,1,.8,1.1);var nose=new THREE.Mesh(new THREE.SphereGeometry(.1,8,6),mat(0x111111));nose.position.set(0,1.54,1.68);DOG.add(nose);",
    "var snout=fs(.24,0,1.48,1.42,1,.8,1.1);var nose=new THREE.Mesh(new THREE.SphereGeometry(.1,8,6),mat(0x111111));nose.position.set(0,1.54,1.68);DOG.add(nose);"
    "var visor=new THREE.Mesh(new THREE.BoxGeometry(.62,.2,.16),new THREE.MeshStandardMaterial({color:0xBFFF00,emissive:0x8fbf00,emissiveIntensity:.6,roughness:.3}));visor.position.set(0,1.72,1.42);DOG.add(visor);"
    "[[-.16],[.16]].forEach(function(e){var ey=new THREE.Mesh(new THREE.SphereGeometry(.05,8,6),mat(0x0A0A11));ey.position.set(e[0],1.72,1.5);DOG.add(ey)});")
one("TONGUE=bx(.22,.08,.3,0xd2546e,0,1.3,1.5);", "TONGUE=bx(.22,.08,.3,0xBFFF00,0,1.3,1.5);")
# the rider becomes Dedric: navy blazer, purple shirt, brown skin, bald head, glasses
one("var JKM=new THREE.MeshStandardMaterial({map:TEX('dianna-jacket.jpg',1,false),roughness:.75,metalness:0});",
    "var JKM=new THREE.MeshStandardMaterial({color:0x1c2a4a,roughness:.8,metalness:0});var SKM=new THREE.MeshStandardMaterial({color:0x6b3f2a,roughness:.7,metalness:0});")
one("JK.position.set(0,.52,0);JK.scale.set(1.3,1.42,1.12);D.add(JK);",
    "JK.position.set(0,.52,0);JK.scale.set(1.3,1.42,1.12);D.add(JK);var SH=new THREE.Mesh(new THREE.BoxGeometry(.26,.5,.12),mat(0x7a2f9e));SH.position.set(0,.66,.5);D.add(SH);")
one("bx(.62,.12,.52,0x1d3aa8,0,.24,0,D);", "bx(.62,.12,.52,0x14131d,0,.24,0,D);")
one("var hd=new THREE.Mesh(new THREE.SphereGeometry(.07,7,6),mat(0xf1c9a5));", "var hd=new THREE.Mesh(new THREE.SphereGeometry(.07,7,6),SKM);")
one("var ft=new THREE.Mesh(new THREE.SphereGeometry(.07,7,6),mat(0xf1c9a5));", "var ft=new THREE.Mesh(new THREE.SphereGeometry(.07,7,6),mat(0x2b2b33));")
one("var DHM=new THREE.MeshStandardMaterial({map:TEX('dianna-head.jpg',1,false),roughness:.8,metalness:0});", "var DHM=SKM;")
one("var HRM=new THREE.MeshStandardMaterial({map:TEX('dianna-hair.jpg',1,false),roughness:.9,metalness:0});", "var HRM=new THREE.MeshStandardMaterial({color:0x2b2b33,roughness:.9,metalness:0});")
one("dHair=new THREE.Mesh(new THREE.SphereGeometry(.345,16,12,Math.PI*.72,Math.PI*1.56),HRM);dHair.position.set(0,.08,0);dHair.scale.set(1.04,1,1.02);HAIR.add(dHair);",
    "dHair=new THREE.Mesh(new THREE.SphereGeometry(.345,16,12,Math.PI*.72,Math.PI*1.56),HRM);dHair.position.set(0,.08,0);dHair.scale.set(.001,.001,.001);HAIR.add(dHair);"
    "var BRD=new THREE.Mesh(new THREE.SphereGeometry(.2,10,8),HRM);BRD.position.set(0,-.1,.2);BRD.scale.set(1,.55,.7);HAIR.add(BRD);"   # beard
    "[[-.11],[.11]].forEach(function(q){var gl=new THREE.Mesh(new THREE.TorusGeometry(.075,.014,6,14),mat(0x9aa6b3));gl.position.set(q[0],.1,.29);HAIR.add(gl)});var gb=new THREE.Mesh(new THREE.BoxGeometry(.06,.014,.014),mat(0x9aa6b3));gb.position.set(0,.1,.3);HAIR.add(gb);")   # glasses
one("var BH=new THREE.Mesh(new THREE.BoxGeometry(.64,.7,.2),HRM);BH.position.set(0,-.2,-.3);HAIR.add(BH);", "")
one("[[-.33,0],[.33,0]].forEach(function(q){var st=new THREE.Mesh(new THREE.BoxGeometry(.14,.6,.2),HRM);st.position.set(q[0],-.12,-.05);HAIR.add(st)});", "")

# voice lines have no mp3 yet: show the subtitle for a few seconds instead of failing silently
one("a.play().catch(function(){subEl.classList.remove('on')})", "a.play().catch(function(){voCur=null;setTimeout(function(){subEl.classList.remove('on')},Math.min(9000,2500+VOT[id].length*45))})")


# rider lines (were Tagalog, Dianna's voice) -> Dedric's own asides
one(r"var DL=\{.*?\};", "var DL={home:'Atlanta first. Home base, and where every one of these roles happened.',journey:'Five roles. Same knot each time: two teams, two systems, one truth to build.',expertise:'Four things I do. The tower is the Salesforce years.',skills:'The stack behind the roadmap. Racks, not slides.',projects:'The talks I recorded. Press Enter on a board to play one.',certs:'Fourteen banners. Nine are Salesforce.',contact:'Book a call, or press Enter on a pad. I read every message.'};", re.S, True)
one("q.fillText('HERO REEL',256,130);", "q.fillText('INTRO REEL',256,130);")
one("v.src='../video/heroreel.mp4';", "v.src='../video/intro.mp4';")
s = s.replace("Manila and come back", "Atlanta and come back").replace("Manila circuit", "Atlanta circuit").replace("Manila playground", "Atlanta playground").replace("Manila plaza", "Atlanta plaza").replace("Manila to every landmark", "Atlanta to every landmark")

# ---------------------------------------------------------------- palette + names
s = s.replace("8a1c2b", "6C2BD9").replace("f0b323", "BFFF00").replace("d8293f", "6C2BD9")
s = s.replace("Mark's", "Dedric's").replace("Mark&#39;s", "Dedric&#39;s").replace("Mark\\'s", "Dedric\\'s").replace("Mark Edcel Lopez", "Dedric Brown")
s = s.replace("markedcel06@gmail.com", EMAIL).replace("https://www.linkedin.com/in/mark-edcel-lopez-513509216/", LI)
s = s.replace("referrernation-web.github.io/portfolio", "referrernation-web.github.io/dedric")
s = s.replace("Kimpoy", "Rev").replace("Dianna", "Dedric").replace("bark", "honk").replace("Bark", "Honk")
s = s.replace("world traveler'", "world traveler'")
s = s.replace("BABA (G)", "GET OFF (G)")
left = re.findall(r"Mark\b", s)
print("patched; leftover 'Mark' mentions:", len(left), "| Manila:", s.count("Manila"), "| size", len(s) // 1024, "KB")
P.write_text(s, encoding="utf-8")
