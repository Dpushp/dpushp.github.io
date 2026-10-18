#!/usr/bin/env python3
"""Build the academic site using Python 3's standard library. Run: python3 build.py"""
from pathlib import Path
from html import escape
import json,re
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parent
def load(name):return json.loads((ROOT/'data'/f'{name}.json').read_text())
profile=load('profile');projects=load('projects');pubs=load('publications');news=load('news')
P={p['id']:p for p in projects};B={p['id']:p for p in pubs}
lab=profile.get('mode')=='lab'
if lab and not profile.get('lab_name'):raise ValueError('Set lab_name in data/profile.json before enabling lab mode.')
name=profile['lab_name'] if lab else profile['name']
def e(s):return escape(str(s),quote=True)
def link(url,label,cls=''):
 if not url:return ''
 if not (url.startswith(('https://','mailto:')) or not urlparse(url).scheme):raise ValueError('Unsupported link scheme')
 return f'<a class="{e(cls)}" href="{e(url)}">{e(label)}</a>'
def nav(active):
 pages=[('index','Home'),('research','Research'),('publications','Publications')]
 if lab:pages.append(('people','People'))
 pages += [('teaching','Teaching'),('cv','About / PI' if lab else 'CV'),('news','News'),('contact','Contact')]
 return ''.join(f'<a href="{i}.html"'+(' aria-current="page"' if i==active else '')+f'>{t}</a>' for i,t in pages)
def page(title,body,active,description='',filename=None):
 filename=filename or active+'.html'
 url=profile['site_url'].rstrip('/')+'/'+('' if filename=='index.html' else filename)
 doc=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | {e(name)}</title><meta name="description" content="{e(description or profile['intro'])}">
<link rel="canonical" href="{e(url)}"><meta name="theme-color" content="#ffffff">
<meta property="og:title" content="{e(title)} | {e(name)}"><meta property="og:description" content="{e(description or profile['intro'])}"><meta property="og:type" content="website"><meta property="og:url" content="{e(url)}"><meta property="og:image" content="{e(profile['site_url'].rstrip('/'))}/assets/images/profile.png">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css?v=20261018">
<script src="videos.js?v=20261018" defer></script><script src="script.js?v=20261018" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="container header-inner"><a class="brand" href="index.html">{e(name)}<span>{e(profile['tagline'] if not lab else profile.get('lab_tagline') or profile['tagline'])}</span></a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav" type="button">Menu</button><nav id="site-nav" aria-label="Main navigation">{nav(active)}</nav></div></header>
<main id="main" class="container">{body}</main><footer class="site-footer container"><span>© 2026 {e(name)}</span><span>{e(profile['institution'])} · Updated {e(profile['updated'])}</span><a href="contact.html">Contact ↗</a></footer></body></html>'''
 (ROOT/filename).write_text(doc)
def heading(t,d=''):return f'<div class="page-heading"><h1>{e(t)}</h1>'+(f'<p class="lead">{e(d)}</p>' if d else '')+'</div>'
def image(p,cls=''):
 if not p.get('image'):return '<div class="research-text-mark"><span>Embodiment</span><strong>What should<br>a robot change?</strong></div>'
 return f'<img class="{e(cls)}" src="assets/images/{e(p["image"])}" alt="{e(p["image_alt"])}" loading="lazy" width="640" height="360">'
def projectcard(p):return f'<article class="project-card"><a class="project-image" href="project-{e(p["id"])}.html">{image(p)}</a><p class="eyebrow">{e(p["theme"])}</p><h3><a href="project-{e(p["id"])}.html">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p><a class="text-link" href="project-{e(p["id"])}.html">Explore project →</a></article>'
def newsrows(items):return ''.join(f'<div class="news-row"><span class="news-date">{e(n["date"])}</span><p>{e(n["text"])}'+(f' <a href="project-{e(n["project"])}.html">Read more →</a>' if n.get('project') else '')+'</p></div>' for n in items)
def authors(s):return e(s).replace('D. Pushp','<strong>D. Pushp</strong>')
def bib(p):
 kind={'Journal':'article','Conference':'inproceedings','Preprint':'misc','Other':'misc'}[p['kind']]
 key='pushp'+str(p['year'])+p['id'];venue='journal' if kind=='article' else 'booktitle' if kind=='inproceedings' else 'howpublished'
 auth=p['authors'].replace(', and ',' and ').replace(', ',' and ')
 result=f'@{kind}{{{key},\n  title = {{{p["title"]}}},\n  author = {{{auth}}},\n  {venue} = {{{p["venue"]}}},\n  year = {{{p["year"]}}}'
 if p.get('paper'):result+=f',\n  url = {{{p["paper"]}}}'
 return result+'\n}'
def pubentry(p):
 pr=P.get(p.get('project'));im=f'<a class="paper-image" href="project-{e(pr["id"])}.html">{image(pr)}</a>' if pr else '<div class="paper-label">'+e(p['kind'])+'<span>'+str(p['year'])+'</span></div>'
 title=link(p.get('paper',''),p['title']) or e(p['title'])
 resources=link(p.get('paper',''),'Paper ↗')
 if pr:resources+=link(f'project-{pr["id"]}.html','Project →')
 video=f'<a data-video-link="{e(pr["video_key"])}" hidden>Video ↗</a>' if pr else ''
 award=f'<p class="award">{e(p["award"])}</p>' if p.get('award') else ''
 return f'<article class="paper" data-kind="{e(p["kind"])}">{im}<div><h3>{title}</h3><p class="authors">{authors(p["authors"])}</p><p class="venue"><em>{e(p["venue"])}</em>, {p["year"]}.</p>{award}<div class="resource-links">{resources}{video}<details class="bibtex"><summary>BibTeX</summary><pre>{e(bib(p))}</pre></details></div></div></article>'
social=''.join(link(profile.get(k,''),v) for k,v in [('github','GitHub ↗'),('scholar','Google Scholar ↗'),('linkedin','LinkedIn ↗'),('orcid','ORCID ↗')])
if not lab:
 home=f'''<section class="profile"><figure class="portrait"><img src="assets/images/profile.png" alt="Durgakant Pushp working with mobile robots in the laboratory." width="1136" height="854"><figcaption>In the robotics lab</figcaption></figure><div><h1>{e(profile['name'])}</h1><p class="affiliation">{e(profile['role'])}<br>{e(profile['department'])}<br>{e(profile['institution'])}</p><p>{e(profile['intro'])}</p><p>{e(profile['bio'])}</p><div class="resource-links">{link('assets/Durgakant_Pushp_CV.pdf','CV (PDF) ↗')}{link('mailto:'+profile['email'],'Email ↗')}{social}</div></div></section>'''
else:
 home=heading(profile['lab_name'],profile.get('lab_mission') or profile['vision'])
 if profile.get('lab_photo'):home+=f'<img class="lab-banner" src="{e(profile["lab_photo"])}" alt="Research in the laboratory">'
 home+='<div class="resource-links"><a href="research.html">Our research →</a><a href="people.html">Meet the team →</a></div>'
home+=f'<section class="section"><div class="section-title"><h2>News</h2><a href="news.html">All news →</a></div>{newsrows(news[:4])}</section><section class="section"><div class="section-title"><h2>Selected research</h2><a href="research.html">All research →</a></div><div class="project-grid">'+''.join(projectcard(P[k]) for k in ['povnav','miniugv2','context-policy'])+'</div></section><section class="section"><div class="section-title"><h2>Selected publications</h2><a href="publications.html">All publications →</a></div>'+''.join(pubentry(B[k]) for k in ['j1','c4','c8'])+'</section>'
page('Home',home,'index')
themes=[('Embodiment','What a robot can physically do','Complementary platforms, sensing, actuation, and tools can expand the missions a robot can undertake.'),('Representation','How a robot makes its world useful for action','Compact representations can connect visual information to navigation and reduce the burden on mapping and computation.'),('Policy','How a robot chooses its actions','Informed default policies and bounded adaptation support decisions under limited information and computation.')]
research=heading('Research',profile['vision'])+'<section class="theme-grid">'+''.join(f'<div><p class="eyebrow">{e(t)}</p><h2>{e(h)}</h2><p>{e(d)}</p></div>' for t,h,d in themes)+'</section><section class="section"><h2>Projects & directions</h2><div class="filters" data-filter-group="projects" hidden>'+''.join(f'<button type="button" data-filter="{e(t)}" aria-pressed="{str(t=="All").lower()}">{e(t)}</button>' for t in ['All','Embodiment','Representation','Policy','Systems'])+'</div><div id="projects">'
for p in projects:research+=f'<article class="research-row" data-theme="{e(p["theme"])}"><a class="research-image" href="project-{e(p["id"])}.html">{image(p)}</a><div><p class="eyebrow">{e(p["theme"])} · {e(p["status"])}</p><h2><a href="project-{e(p["id"])}.html">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p><a class="text-link" href="project-{e(p["id"])}.html">View project →</a></div></article>'
research+='</div><p class="filter-empty" data-empty="projects" hidden>No projects match this filter.</p></section>'
page('Research',research,'research')
for p in projects:
 body=f'<a class="back-link" href="research.html">← All research</a><div class="project-heading"><p class="eyebrow">{e(p["theme"])} · {e(p["status"])}</p><h1>{e(p["title"])}</h1><p class="lead">{e(p["subtitle"])}</p><div class="resource-links">{link(p["paper"],"Paper ↗")}{link(p["code"],"Code ↗")}<a data-video-link="{e(p["video_key"])}" hidden>Watch video ↗</a></div></div>'
 if p['image']:body+=f'<figure class="project-figure">{image(p)}<figcaption>{e(p["caption"])}</figcaption></figure>'
 body+=f'<div class="project-overview"><section><h2>Overview</h2><p>{e(p["overview"])}</p></section><section><h2>{"Research questions" if p["id"]=="embodiment-search" else "Highlights"}</h2><ul>'+''.join(f'<li>{e(c)}</li>' for c in p['contributions'])+'</ul></section></div>'
 body+=f'<section class="section video-section" data-video-section="{e(p["video_key"])}" hidden><h2>Research demonstration</h2><div class="video-container" data-video-player="{e(p["video_key"])}"></div><p class="small"><a data-video-link="{e(p["video_key"])}" hidden>Watch on YouTube ↗</a></p><noscript>Open the associated paper for its supplementary video.</noscript></section>'
 if p['related']:body+='<section class="section"><h2>Related publications</h2>'+''.join(pubentry(B[k]) for k in p['related'])+'</section>'
 page(p['title'],body,'research',p['summary'],f'project-{p["id"]}.html')
body=heading('Publications','Journal articles, conference publications, and preprints. My name is highlighted in the author lists.')+'<div class="filters" data-filter-group="publications" hidden>'+''.join(f'<button type="button" data-filter="{t}" aria-pressed="{str(t=="All").lower()}">{t}</button>' for t in ['All','Journal','Conference','Preprint','Other'])+'</div><div id="publications">'
for year in sorted({p['year'] for p in pubs},reverse=True):body+=f'<section class="publication-year"><h2>{year}</h2>'+''.join(pubentry(p) for p in pubs if p['year']==year)+'</section>'
body+='</div><p class="filter-empty" data-empty="publications" hidden>No publications match this filter.</p>'
page('Publications',body,'publications')
body=heading('Teaching & mentoring',profile['teaching_statement'])+'<section class="section"><h2>Teaching experience</h2>'
for date,title,role,desc in [('August 2024','Autonomous Robots','Guest Lecturer · Indiana University Bloomington','Delivered a lecture for approximately 20 undergraduate and graduate students on autonomous racing, GNSS localization, PID and Pure Pursuit control, and an introduction to MPPI.'),('January–May 2024','Introduction to Cyber-Physical Systems','Teaching Assistant · Indiana University Bloomington','Supported approximately 30 undergraduate students through ROS and autonomy-stack projects, office hours, and assessment.'),('September 2017','Aeromodelling workshop','Organizer & Instructor · Jadavpur University','Designed and delivered a two-day workshop for approximately 250 undergraduate participants, covering aerodynamics, flight mechanics, aircraft construction, and flight.')]:
 body+=f'<article class="teaching-row"><p class="small">{e(date)}</p><div><h3>{e(title)}</h3><p class="small">{e(role)}</p><p>{e(desc)}</p></div></article>'
body+='</section><section class="section"><h2>Research mentoring</h2><p>'+e(profile['mentoring_statement'])+'</p><div class="mentoring-list">'
for title,desc in [('LiDAR localization for high-speed racing','Mentor a Ph.D. student on research direction and technical development of the localization module at Purdue.'),('Seeing Where to Deploy (IROS 2026)','Directed the research from project inception through manuscript completion; guided the first and second authors and contributed to writing.'),('AFRDA (RA-L 2025)','Held weekly research meetings, helped shape the study through submission, and contributed to manuscript writing.'),('From Zero to High-Speed Racing (ISER 2025)','Led the underlying racing-system development and guided the work through most of the project. The first author led final completion for submission.')]:body+=f'<article><h3>{e(title)}</h3><p>{e(desc)}</p></article>'
body+='</div></section>'
page('Teaching & mentoring',body,'teaching')
body=heading('Curriculum vitae','An overview of my academic background, research experience, and professional service.')+link('assets/Durgakant_Pushp_CV.pdf','Download full CV (PDF) ↓','download-link')
def cvsection(title,entries):return '<section class="section"><h2>'+e(title)+'</h2>'+''.join(f'<div class="cv-row"><p class="small">{e(date)}</p><div><h3>{e(t)}</h3><p>{e(org)}</p>'+('' if not desc else f'<p class="small">{e(desc)}</p>')+'</div></div>' for date,t,org,desc in entries)+'</section>'
body+=cvsection('Appointments & research experience',[
 ('2026–Present','Postdoctoral Research Fellow','Purdue University · School of Mechanical Engineering','Purdue AI Racing: localization research, mentoring, and autonomy-stack development.'),('2023–2026','Team Lead, IU–Luddy Autonomous Racing Team','Indiana University Bloomington','Technical development, research planning, mentoring, integration, and on-track testing.'),('2023–2025','Research Assistant; Project Technical Leadership','Indiana University Bloomington','ERDC-supported robotic inspection of flood-control systems.'),('2021–2023','Research Assistant; Project Technical Leadership','Indiana University Bloomington','ARL-supported Off-Road Autonomy / SARA program.'),('2021–2022','Team Lead, AISUM Autonomous Systems Challenge','Indiana University Bloomington','GPS-denied exploration; national Top-8 finish.'),('2017–2020','Research Engineer; Field Experiment Lead','TCS Research & Indian Institute of Science, Bangalore','Perception, navigation, aerial manipulation, and multi-robot systems.')])
body+=cvsection('Education',[('2021–2026','Ph.D., Intelligent Systems Engineering','Indiana University Bloomington','Advisor: Prof. Lantao Liu. Dissertation on bounded rational robots, embodiment, representation, and intelligent behavior.'),('2013–2017','B.Tech., Computer Science and Engineering','West Bengal University of Technology','')])
body+=cvsection('Selected honors & team results',[('2025','IJRR Paper of the Season, Q2 2025: Honorable Mention','Navigating the Wild',''),('2026','PAIR: first place, time trial; second place, multi-car race','Indy Autonomous Challenge · Laguna Seca','Team result; see CV for research contributions.'),('2025','IU–Luddy: second place, LVMS time trial; fourth place, Laguna Seca','Indy Autonomous Challenge',''),('2024','Second Place, Cheng Wu Innovation Challenge','Single-member team',''),('2023','Audience Choice Award, MassRobotics Form & Function Challenge','Single-member team',''),('2021–2022','Top-8 National Finalist, AISUM Challenge','Single-member team',''),('2020','Best Innovation Award','Mohamed Bin Zayed International Robotics Challenge','Team award.')])
body+=cvsection('Patents',[('2024','Robot-Mountable Adaptive Gripper Assembly for Intercepting Aerial Targets','Indian Patent No. IN 202321018297','R. Lima, D. Pushp, et al.'),('Provisional','UAV Tethered to UGV System','U.S. provisional patent application No. 63/914,830','D. Pushp, S. Kalhapure, and L. Liu.')])
body+='<section class="section"><h2>Professional service</h2><p>Peer reviewer for ICRA, IROS, IEEE Robotics and Automation Letters, and ISER. Research and robotics mentoring across graduate, undergraduate, and high-school projects.</p></section><section class="section"><h2>Technical expertise</h2><p>Localization, visual navigation, terrain perception, planning and control, multi-robot coordination, field testing, and systems integration.</p><p>C++, Python, ROS 1/2, Gazebo, AirSim, MuJoCo, PyTorch, TensorFlow, and OpenCV.</p></section>'
page('Curriculum vitae',body,'cv')
page('News',heading('News','Research updates, publications, and milestones.')+'<section class="news-archive">'+newsrows(news)+'</section>','news')
contact=heading('Contact','For research inquiries and collaborations, please get in touch by email.')+f'<div class="contact-grid"><section><h2>{e(profile["name"])}</h2><p>{e(profile["role"])}<br>{e(profile["department"])}<br>{e(profile["institution"])}<br>{e(profile["location"])}</p><p>{link("mailto:"+profile["email"],profile["email"])}</p><div class="resource-links">{social}{link("assets/Durgakant_Pushp_CV.pdf","CV (PDF) ↗")}</div></section><figure class="contact-photo"><img src="assets/images/profile.png" alt="Durgakant Pushp with mobile robot platforms in the lab." width="1136" height="854"></figure></div>'
page('Contact',contact,'contact')
if lab:
 people=heading('People','Researchers working on adaptive robotic intelligence.')+'<h2>Principal investigator</h2><div class="research-row"><figure class="portrait"><img src="assets/images/profile.png" alt="Durgakant Pushp in the lab."></figure><div><h3>'+e(profile['name'])+'</h3><p>'+e(profile['bio'])+'</p><a href="cv.html">Biography & CV →</a></div></div>'
 for group in sorted({p['group'] for p in profile['people']}):
  people+='<section class="section"><h2>'+e(group)+'</h2><div class="project-grid">'
  for member in profile['people']:
   if member['group']!=group:continue
   people+='<article><h3>'+e(member['name'])+'</h3><p>'+e(member['role'])+'</p><p>'+e(member.get('interests',''))+'</p></article>'
  people+='</div></section>'
 page('People',people,'people')
else:(ROOT/'people.html').unlink(missing_ok=True)
page('Page not found',heading('Page not found','The page may have moved. Please use the navigation or return to the homepage.')+'<a href="index.html">Return home →</a>','index',filename='404.html')
urls=['index.html','research.html','publications.html','teaching.html','cv.html','news.html','contact.html']+[f'project-{p["id"]}.html' for p in projects]
if lab:urls.append('people.html')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+e(profile['site_url'].rstrip('/')+'/'+('' if u=='index.html' else u))+'</loc></url>' for u in urls)+'</urlset>\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+profile['site_url'].rstrip('/')+'/sitemap.xml\n')
(ROOT/'assets/publications.bib').write_text('\n\n'.join(bib(p) for p in pubs)+'\n')
print(f'Built {len(urls)} pages + 404; {len(pubs)} publications; mode={profile["mode"]}.')
