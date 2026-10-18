'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
function element(dataset = {}) {
  return { dataset, hidden: true, attrs: {}, children: [], listeners: {}, classList: { toggle() {}, add() {} },
    setAttribute(k,v) { this.attrs[k] = v; }, getAttribute(k) { return this.attrs[k]; },
    addEventListener(k,v) { this.listeners[k] = v; }, contains() { return true; },
    appendChild(v) { this.children.push(v); }, replaceChildren(...v) { this.children = v; } };
}
const menu=element();menu.attrs['aria-expanded']='false';
const nav=element();let menuOpen=false;nav.classList.toggle=(name,on)=>{menuOpen=on;};
const links=[element({videoLink:'povnav'}),element({videoLink:'racing'})];
const holder=element();const section=element({videoSection:'povnav'});section.querySelector=()=>holder;
const emptySection=element({videoSection:'racing'});emptySection.querySelector=()=>element();
const groups=['projects','publications'].map(type=>{
 const g=element({filterGroup:type});g.buttons=['All',type==='projects'?'Policy':'Journal'].map(filter=>element({filter}));g.querySelectorAll=()=>g.buttons;return g;
});
const projectItems=[element({theme:'Policy'}),element({theme:'Embodiment'})];projectItems.forEach(i=>i.hidden=false);
const paperItems=[element({kind:'Journal'}),element({kind:'Conference'})];paperItems.forEach(i=>i.hidden=false);
const year=element();year.querySelectorAll=()=>paperItems;const empty=element();
const lists={projects:{querySelectorAll:s=>s==='.publication-year'?[]:projectItems,querySelector:()=>projectItems.find(i=>!i.hidden)},publications:{querySelectorAll:s=>s==='.publication-year'?[year]:paperItems,querySelector:()=>paperItems.find(i=>!i.hidden)}};
const doc={documentElement:{classList:{add(){}}},
 querySelector(s){if(s==='.menu-toggle')return menu;if(s==='.project-figure img')return null;if(s.startsWith('[data-empty='))return empty;return null;},
 getElementById(s){return s==='site-nav'?nav:lists[s];},
 querySelectorAll(s){return {'[data-filter-group]':groups,'[data-video-link]':links,'[data-video-section]':[section,emptySection]}[s]||[];},
 createElement(){return element();}};
const ctx=vm.createContext({document:doc,window:{},URL,console});
vm.runInContext(fs.readFileSync(path.join(root,'videos.js'),'utf8'),ctx);
vm.runInContext(fs.readFileSync(path.join(root,'script.js'),'utf8'),ctx);
for(const [u,id] of [['wVwIQdXpUM8','wVwIQdXpUM8'],['https://youtu.be/wVwIQdXpUM8?t=20','wVwIQdXpUM8'],['https://www.youtube.com/watch?v=wVwIQdXpUM8&list=a','wVwIQdXpUM8'],['https://youtube.com/shorts/wVwIQdXpUM8','wVwIQdXpUM8'],['https://youtube.com/live/wVwIQdXpUM8','wVwIQdXpUM8'],['https://www.youtube-nocookie.com/embed/wVwIQdXpUM8','wVwIQdXpUM8'],['',''],['https://youtube.com.evil.invalid/watch?v=wVwIQdXpUM8',''],['javascript:alert(1)','']])assert.equal(ctx.youtubeId(u),id);
assert.equal(links[0].href,'https://www.youtube.com/watch?v=wVwIQdXpUM8');assert.equal(links[0].hidden,false);assert.equal(links[1].hidden,true);
assert.equal(section.hidden,false);assert.equal(emptySection.hidden,true);
holder.children[0].listeners.click();assert.match(holder.children[0].src,/youtube-nocookie.com\/embed\/wVwIQdXpUM8/);
menu.listeners.click();assert.equal(menuOpen,true);menu.listeners.click();assert.equal(menuOpen,false);
for(const g of groups){const b=g.buttons[1];g.listeners.click({target:{closest:()=>b}});assert.equal(b.attrs['aria-pressed'],'true');}
assert.equal(projectItems[0].hidden,false);assert.equal(projectItems[1].hidden,true);assert.equal(paperItems[0].hidden,false);assert.equal(paperItems[1].hidden,true);
console.log('PASS: video URLs, links, hidden video slots, click-to-load player, mobile menu, and both filter groups.');
