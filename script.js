'use strict';
document.documentElement.classList.add('js');
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.getElementById('site-nav');
if (menuButton && navigation) {
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
}
// Publication and project filters progressively enhance fully rendered HTML.
document.querySelectorAll('[data-filter-group]').forEach(group => {
  const type = group.dataset.filterGroup;
  const list = document.getElementById(type);
  if (!list) return;
  group.hidden = false;
  const buttons = group.querySelectorAll('button');
  group.addEventListener('click', event => {
    const selected = event.target.closest('button[data-filter]');
    if (!selected || !group.contains(selected)) return;
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b === selected)));
    const filter = selected.dataset.filter;
    list.querySelectorAll(type === 'projects' ? '[data-theme]' : '[data-kind]').forEach(item => {
      const category = type === 'projects' ? item.dataset.theme : item.dataset.kind;
      item.hidden = filter !== 'All' && category !== filter;
    });
    list.querySelectorAll('.publication-year').forEach(year => {
      year.hidden = ![...year.querySelectorAll('.paper')].some(paper => !paper.hidden);
    });
    const empty = document.querySelector(`[data-empty="${type}"]`);
    if (empty) empty.hidden = !!list.querySelector(type === 'projects' ? '[data-theme]:not([hidden])' : '[data-kind]:not([hidden])');
  });
});
function youtubeId(value) {
  if (typeof value !== 'string' || !value.trim()) return '';
  const raw = value.trim();
  if (/^[A-Za-z0-9_-]{11}$/.test(raw)) return raw;
  try {
    const u = new URL(raw);
    if (!['http:', 'https:'].includes(u.protocol)) return '';
    const host = u.hostname.toLowerCase().replace(/^www\./, '');
    let id = '';
    if (host === 'youtu.be') id = u.pathname.split('/')[1];
    if (['youtube.com', 'm.youtube.com', 'youtube-nocookie.com'].includes(host)) {
      id = u.searchParams.get('v') || (/^\/(embed|shorts|live)\//.test(u.pathname) ? u.pathname.split('/')[2] : '');
    }
    return /^[A-Za-z0-9_-]{11}$/.test(id || '') ? id : '';
  } catch (_) { return ''; }
}
const researchVideos = window.RESEARCH_VIDEOS || {};
document.querySelectorAll('[data-video-link]').forEach(anchor => {
  const id = youtubeId(researchVideos[anchor.dataset.videoLink]);
  if (!id) return;
  anchor.href = `https://www.youtube.com/watch?v=${id}`;
  anchor.hidden = false;
});
document.querySelectorAll('[data-video-section]').forEach(section => {
  const key = section.dataset.videoSection;
  const id = youtubeId(researchVideos[key]);
  const holder = section.querySelector('[data-video-player]');
  if (!id || !holder) return;
  section.hidden = false;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'video-load';
  button.setAttribute('aria-label', 'Play research demonstration');
  const existingFigure = document.querySelector('.project-figure img');
  if (existingFigure) {
    const poster = document.createElement('img');
    poster.src = existingFigure.getAttribute('src');
    poster.alt = '';
    button.appendChild(poster);
  }
  const label = document.createElement('span');
  label.textContent = '▶ Play research video';
  button.appendChild(label);
  button.addEventListener('click', () => {
    const frame = document.createElement('iframe');
    frame.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
    frame.title = 'Research demonstration';
    frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    holder.replaceChildren(frame);
  });
  holder.replaceChildren(button);
});
