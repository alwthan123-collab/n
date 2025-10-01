// ========== بيانات العناصر (10 تطبيقات + 10 كتب) ==========
// استبدل FILE_ID_x بروابط التحميل الحقيقية أو استخدم downloads/app1.apk محلياً
const ITEMS = [
  // التطبيقات
  { id:'app1', type:'app', title:'تعلم الإنجليزية', category:'تعليمي', size:'32 MB', version:'1.4.2', date:'2025-08-10', desc:'تطبيق تفاعلي لتعليم الإنجليزية مع ألعاب وتمارين صوتية.', thumb:'images/apps/app1.png', shots:['images/apps/app1.png'], downloads:[{label:'Drive',url:'https://drive.google.com/uc?export=download&id=FILE_ID_1'}] },
  { id:'app2', type:'app', title:'منظف الجهاز', category:'أدوات', size:'18 MB', version:'2.0.1', date:'2025-07-22', desc:'تنظيف الملفات المؤقتة وتسريع الهاتف بضغطة.', thumb:'images/apps/app2.png', shots:['images/apps/app2.png'], downloads:[{label:'Drive',url:'https://drive.google.com/uc?export=download&id=FILE_ID_2'}] },
  { id:'app3', type:'app', title:'قاموس عربي-إنجليزي', category:'تعليمي', size:'25 MB', version:'3.1.0', date:'2025-06-11', desc:'قاموس شامل يعمل بدون إنترنت.', thumb:'images/apps/app3.png', shots:[], downloads:[{label:'Drive',url:'https://drive.google.com/uc?export=download&id=FILE_ID_3'}] },
  { id:'app4', type:'app', title:'مراقب الصحة', category:'إنتاجية', size:'28 MB', version:'1.2.5', date:'2025-05-30', desc:'مراقبة النشاط والتمارين وحساب السعرات.', thumb:'images/apps/app4.png', shots:[], downloads:[{label:'Drive',url:'https://drive.google.com/uc?export=download&id=FILE_ID_4'}] },
  { id:'app5', type:'app', title:'مترجم فوري', category:'أدوات', size:'22 MB', version:'4.0.0', date:'2025-08-05', desc:'ترجمة نصوص ومحادثات فورية بدعم صوتي.', thumb:'images/apps/app5.png', shots:[], downloads:[{label:'Drive',url:'https://drive.google.com/uc?export=download&id=FILE_ID_5'}] },
  { id:'app6', type:'app', title:'لعبة ألغاز ممتعة', category:'ترفيه', size:'45 MB', version:'1.0.7', date:'2025-07-01', desc:'ألغاز ومسابقات ذهنية تناسب كل الأعمار.', thumb:'images/apps/app6.png', shots:[], downloads:[{label:'Drive',url:'https://drive.google.com/uc?export=download&id=FILE_ID_6'}] },
  { id:'app7', type:'app', title:'ملاحظات سريعة', category:'إنتاجية', size:'8 MB', version:'2.3.2', date:'2025-06-25', desc:'تطبيق تدوين ملاحظات سريع وخفيف.', thumb:'images/apps/app7.png', shots:[], downloads:[{label:'Drive',url:'https://drive.google.com/uc?export=download&id=FILE_ID_7'}] },
  { id:'app8', type:'app', title:'عارض صور بروفشنال', category:'أدوات', size:'14 MB', version:'1.8.0', date:'2025-05-20', desc:'تطبيق عرض صور وفلترات سهلة الاستخدام.', thumb:'images/apps/app8.png', shots:[], downloads:[{label:'Drive',url:'https://drive.google.com/uc?export=download&id=FILE_ID_8'}] },
  { id:'app9', type:'app', title:'مشغل موسيقى خفيف', category:'ترفيه', size:'11 MB', version:'5.0.0', date:'2025-04-12', desc:'مشغل صوتيات مع مؤثرات ومعادل صوتي.', thumb:'images/apps/app9.png', shots:[], downloads:[{label:'Drive',url:'https://drive.google.com/uc?export=download&id=FILE_ID_9'}] },
  { id:'app10', type:'app', title:'حماية الخصوصية', category:'أدوات', size:'19 MB', version:'3.4.1', date:'2025-03-05', desc:'قفل التطبيقات وإدارة أذونات الخصوصية.', thumb:'images/apps/app10.png', shots:[], downloads:[{label:'Drive',url:'https://drive.google.com/uc?export=download&id=FILE_ID_10'}] },

  // الكتب
  { id:'book1', type:'book', title:'مدخل إلى بايثون', category:'برمجة', size:'7.2 MB', version:'PDF', date:'2025-06-15', desc:'كتاب مبسط للمبتدئين في بايثون مع أمثلة عملية.', thumb:'images/books/book1.png', shots:[], downloads:[{label:'PDF (Drive)',url:'https://drive.google.com/uc?export=download&id=FILE_ID_11'}] },
  { id:'book2', type:'book', title:'تصميم واجهات المستخدم', category:'تصميم', size:'5.8 MB', version:'PDF', date:'2025-05-10', desc:'مبادئ تصميم واجهات حديثة وتجربة المستخدم.', thumb:'images/books/book2.png', shots:[], downloads:[{label:'PDF',url:'https://drive.google.com/uc?export=download&id=FILE_ID_12'}] },
  { id:'book3', type:'book', title:'أساسيات قواعد البيانات', category:'برمجة', size:'6.9 MB', version:'PDF', date:'2025-04-20', desc:'مدخل لقواعد البيانات SQL وتصميم ERD.', thumb:'images/books/book3.png', shots:[], downloads:[{label:'PDF',url:'https://drive.google.com/uc?export=download&id=FILE_ID_13'}] },
  { id:'book4', type:'book', title:'تعلم JavaScript', category:'برمجة', size:'8.1 MB', version:'PDF', date:'2025-03-12', desc:'دليل عملي لتعلم لغة JavaScript من الصفر.', thumb:'images/books/book4.png', shots:[], downloads:[{label:'PDF',url:'https://drive.google.com/uc?export=download&id=FILE_ID_14'}] },
  { id:'book5', type:'book', title:'فن الإقناع', category:'تنمية بشرية', size:'3.4 MB', version:'PDF', date:'2025-02-01', desc:'نصائح وتطبيقات عملية في فن التواصل والإقناع.', thumb:'images/books/book5.png', shots:[], downloads:[{label:'PDF',url:'https://drive.google.com/uc?export=download&id=FILE_ID_15'}] },
  { id:'book6', type:'book', title:'أساسيات الشبكات', category:'شبكات', size:'9.5 MB', version:'PDF', date:'2024-12-05', desc:'مفاهيم الشبكات، TCP/IP، والنشر العملي.', thumb:'images/books/book6.png', shots:[], downloads:[{label:'PDF',url:'https://drive.google.com/uc?export=download&id=FILE_ID_16'}] },
  { id:'book7', type:'book', title:'الذكاء الاصطناعي مبسط', category:'ذكاء اصطناعي', size:'10.2 MB', version:'PDF', date:'2025-01-22', desc:'مقدمة في الذكاء الاصطناعي وتطبيقاته العملية.', thumb:'images/books/book7.png', shots:[], downloads:[{label:'PDF',url:'https://drive.google.com/uc?export=download&id=FILE_ID_17'}] },
  { id:'book8', type:'book', title:'رواية الأفق المفقود', category:'روايات', size:'4.1 MB', version:'PDF', date:'2024-11-18', desc:'رواية درامية مشوقة بأسلوب شيق وسلس.', thumb:'images/books/book8.png', shots:[], downloads:[{label:'PDF',url:'https://drive.google.com/uc?export=download&id=FILE_ID_18'}] },
  { id:'book9', type:'book', title:'خوارزميات مبسطة', category:'برمجة', size:'6.6 MB', version:'PDF', date:'2024-10-10', desc:'شرح الخوارزميات الأساسية مع أمثلة.', thumb:'images/books/book9.png', shots:[], downloads:[{label:'PDF',url:'https://drive.google.com/uc?export=download&id=FILE_ID_19'}] },
  { id:'book10', type:'book', title:'رحلة نحو الإنتاجية', category:'تنمية بشرية', size:'2.9 MB', version:'PDF', date:'2024-08-25', desc:'خطوات عملية لتحسين الإنتاجية وإدارة الوقت.', thumb:'images/books/book10.png', shots:[], downloads:[{label:'PDF',url:'https://drive.google.com/uc?export=download&id=FILE_ID_20'}] }
];

// ======= DOM UTIL =======
const $ = (s, el=document) => el.querySelector(s);
const $$ = (s, el=document) => Array.from((el||document).querySelectorAll(s));
const fmtDate = d => new Date(d).toLocaleDateString('ar-EG', {year:'numeric', month:'short', day:'numeric'});

// set years
['year1','year2','year3','year4'].forEach(id => { const e=document.getElementById(id); if(e) e.textContent=new Date().getFullYear();});

// local storage counters & favorites
const DL_KEY='dl_v3', FAV_KEY='fav_v3';
const dlCounts = JSON.parse(localStorage.getItem(DL_KEY) || '{}');
const favs = new Set(JSON.parse(localStorage.getItem(FAV_KEY) || '[]'));
function saveDL(){ localStorage.setItem(DL_KEY, JSON.stringify(dlCounts)); }
function saveFavs(){ localStorage.setItem(FAV_KEY, JSON.stringify([...favs])); }
function incDownload(id){ dlCounts[id]=(dlCounts[id]||0)+1; saveDL(); renderAll(); }
function toggleFav(id){ if(favs.has(id)) favs.delete(id); else favs.add(id); saveFavs(); renderAll(); }

// state for filters/search
let state = { q:'', cat:'all', sort:'new' };

// global search
const globalSearch = document.getElementById('globalSearch');
if(globalSearch) globalSearch.addEventListener('input', e=>{ state.q = e.target.value.trim(); renderHome(state.q); });

// page-specific listeners
const searchApps = document.getElementById('searchApps');
if(searchApps) searchApps.addEventListener('input', e=>{ state.q = e.target.value.trim(); renderApps(); });
const filterCat = document.getElementById('filterCat');
if(filterCat) filterCat.addEventListener('change', e=>{ state.cat = e.target.value; renderApps(); });
const sortApps = document.getElementById('sortApps');
if(sortApps) sortApps.addEventListener('change', e=>{ state.sort = e.target.value; renderApps(); });

const searchBooks = document.getElementById('searchBooks');
if(searchBooks) searchBooks.addEventListener('input', e=>{ state.q = e.target.value.trim(); renderBooks(); });

// helpers
function filterItems(kind){
  let list = ITEMS.filter(i => i.type === kind);
  if(state.cat && state.cat !== 'all') list = list.filter(i => i.category === state.cat);
  if(state.q) list = list.filter(i => (i.title + ' ' + i.desc + ' ' + i.category).toLowerCase().includes(state.q.toLowerCase()));
  if(state.sort === 'new') list.sort((a,b)=> new Date(b.date) - new Date(a.date));
  if(state.sort === 'popular') list.sort((a,b)=> (dlCounts[b.id]||0) - (dlCounts[a.id]||0));
  if(state.sort === 'az') list.sort((a,b)=> a.title.localeCompare(b.title,'ar'));
  return list;
}

// card builder
function makeCard(item){
  const dls = dlCounts[item.id] || 0;
  const favClass = favs.has(item.id) ? 'fav active' : 'fav';
  return `
    <div class="card" data-id="${item.id}">
      <div class="${favClass}" onclick="toggleFav('${item.id}')">❤</div>
      <div class="thumb"><img src="${item.thumb}" alt="${item.title}"></div>
      <div class="titleRow"><h3>${item.title}</h3><span class="badge">${item.category}</span></div>
      <div class="desc">${item.desc}</div>
      <div class="metaRow"><div class="pill">${item.version}</div><div class="pill">${item.size}</div><div class="pill">${fmtDate(item.date)}</div></div>
      <div class="actionsRow">
        <a class="btn primary" href="${item.downloads[0]?.url||'#'}" target="_blank" onclick="incDownload('${item.id}')">${item.type==='app'?'تحميل APK':'تحميل PDF'}</a>
        <a class="btn ghost" href="${item.type==='app'?'app-detail.html?id='+item.id:'book-detail.html?id='+item.id}">التفاصيل</a>
      </div>
      <div class="dlcount">التحميلات: ${dls}</div>
    </div>
  `;
}

// renderers
function renderHome(q=''){
  const el = document.getElementById('homeGrid'); if(!el) return;
  let list = [...ITEMS].sort((a,b)=> new Date(b.date) - new Date(a.date)).slice(0,8);
  if(q) list = list.filter(i => (i.title + ' ' + i.desc).toLowerCase().includes(q.toLowerCase()));
  el.innerHTML = list.map(makeCard).join('');
}
function renderApps(){
  const el = document.getElementById('appsGrid'); if(!el) return;
  const list = filterItems('app');
  el.innerHTML = list.map(makeCard).join('') || '<div style="color:var(--muted-text);padding:20px">لا توجد تطبيقات مطابقة</div>';
}
function renderBooks(){
  const el = document.getElementById('booksGrid'); if(!el) return;
  const list = filterItems('book');
  el.innerHTML = list.map(makeCard).join('') || '<div style="color:var(--muted-text);padding:20px">لا توجد كتب مطابقة</div>';
}
function renderAll(){ renderHome(); renderApps(); renderBooks(); buildSlider(); }

// slider (home)
function buildSlider(){
  const slider = document.getElementById('mainSlider'); const dots = document.getElementById('sliderDots');
  if(!slider) return;
  const featured = [...ITEMS].sort((a,b)=> new Date(b.date)-new Date(a.date)).slice(0,3);
  slider.innerHTML = featured.map(it => `
    <div class="slideItem">
      <div class="slideText">
        <div class="badge">${it.type==='app'?'تطبيق مميز':'كتاب مميز'}</div>
        <h2>${it.title}</h2><p>${it.desc}</p>
        <div style="margin-top:12px">
          <a class="btn primary" href="${it.downloads[0]?.url||'#'}" target="_blank" onclick="incDownload('${it.id}')">تحميل الآن</a>
          <a class="btn ghost" href="${it.type==='app'?'app-detail.html?id='+it.id:'book-detail.html?id='+it.id}">التفاصيل</a>
        </div>
      </div>
      <div class="slideCover"><img src="${it.thumb}" alt="${it.title}"></div>
    </div>
  `).join('');
  dots.innerHTML = featured.map((_,i)=> `<div class="dot" data-i="${i}"></div>`).join('');
  let idx=0; const items = slider.children;
  function show(i){ for(let k=0;k<items.length;k++) items[k].style.transform = `translateX(${(k - i)*100}%)`; $$('.dot').forEach(d=>d.classList.remove('active')); $(`.dot[data-i="${i}"]`).classList.add('active'); }
  if(items.length){ for(let k=0;k<items.length;k++) items[k].style.transition='transform .6s ease'; show(0); let t=setInterval(()=>{ idx=(idx+1)%items.length; show(idx); },3500); $$('.dot').forEach(d=>d.addEventListener('click',e=>{ clearInterval(t); idx=+d.dataset.i; show(idx); t=setInterval(()=>{ idx=(idx+1)%items.length; show(idx); },3500); })); }
}

// detail builder
function getParam(n){ const url=new URL(location.href); return url.searchParams.get(n); }
function buildDetail(areaId, id){
  const area = document.getElementById(areaId); if(!area) return;
  const item = ITEMS.find(x=> x.id === id); if(!item){ area.innerHTML='<div style="padding:20px;color:var(--muted-text)">العنصر غير موجود</div>'; return; }
  area.innerHTML = `
    <div class="detail-main">
      <div style="display:flex;gap:16px;align-items:flex-start">
        <img src="${item.thumb}" alt="${item.title}" style="width:180px;height:180px;border-radius:12px;object-fit:cover">
        <div>
          <h2>${item.title}</h2>
          <div style="color:var(--muted-text);margin-top:8px">${item.desc}</div>
          <div style="margin-top:12px;display:flex;gap:8px;">
            ${item.downloads.map((d,i)=> `<a class="btn ${i? 'ghost':'primary'}" href="${d.url}" target="_blank" onclick="incDownload('${item.id}')">${d.label}</a>`).join('')}
          </div>
        </div>
      </div>
      <div style="margin-top:18px">
        <h3>معلومات</h3>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">
          <div class="pill">الحجم: ${item.size}</div>
          <div class="pill">الإصدار: ${item.version}</div>
          <div class="pill">التصنيف: ${item.category}</div>
          <div class="pill">تاريخ الإضافة: ${fmtDate(item.date)}</div>
        </div>
      </div>
    </div>
    <aside class="detail-side">
      <h4>لقطات الشاشة</h4>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">${ (item.shots && item.shots.length) ? item.shots.map(s=> `<img src="${s}" style="width:120px;height:120px;border-radius:8px;object-fit:cover">`).join('') : `<div style="color:var(--muted-text)">لا توجد لقطات شاشة</div>` }</div>
      <div style="margin-top:12px"><h4>التحميلات</h4><div style="color:var(--muted-text)">تم تحميل هذا العنصر ${dlCounts[item.id]||0} مرة</div></div>
    </aside>
  `;
}

// theme toggle
const THEME_KEY='theme_v3';
function applyTheme(t){ if(t==='light') document.documentElement.classList.add('light'); else document.documentElement.classList.remove('light'); localStorage.setItem(THEME_KEY,t); }
const modeBtn = document.getElementById('modeBtn');
if(modeBtn){ const saved=localStorage.getItem(THEME_KEY)||'dark'; applyTheme(saved); modeBtn.addEventListener('click', ()=> applyTheme(document.documentElement.classList.contains('light')?'dark':'light')); }

// three.js bg (subtle floating shapes)
function initThreeBg(){
  const canvas = document.getElementById('three-canvas'); if(!canvas) return;
  const renderer = new THREE.WebGLRenderer({canvas, antialias:true, alpha:true});
  renderer.setPixelRatio(window.devicePixelRatio);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 1000);
  camera.position.z = 50;
  const light = new THREE.DirectionalLight(0xffffff, 0.9); light.position.set(5,10,7); scene.add(light);
  const amb = new THREE.AmbientLight(0xffffff, 0.4); scene.add(amb);

  const group = new THREE.Group();
  const baseColor = 0x5BC0BE;
  for(let i=0;i<18;i++){
    const geom = Math.random()>0.5? new THREE.BoxGeometry(6,6,6) : new THREE.SphereGeometry(3.5, 24, 24);
    const mat = new THREE.MeshStandardMaterial({color: baseColor, metalness:0.2, roughness:0.3, transparent:true, opacity:0.12});
    const m = new THREE.Mesh(geom, mat);
    m.position.set((Math.random()-0.5)*100, (Math.random()-0.5)*70, (Math.random()-0.5)*150);
    m.rotation.set(Math.random()*2, Math.random()*2, Math.random()*2);
    group.add(m);
  }
  scene.add(group);

  function resize(){ const w=window.innerWidth, h=window.innerHeight; renderer.setSize(w,h); camera.aspect=w/h; camera.updateProjectionMatrix(); }
  window.addEventListener('resize', resize); resize();
  function animate(){ requestAnimationFrame(animate); group.rotation.y += 0.0025; group.rotation.x += 0.0012; renderer.render(scene, camera); }
  animate();
}

// init
function init(){
  renderAll();
  // details
  const appArea = document.getElementById('appDetailArea'); if(appArea){ const id=getParam('id'); buildDetail('appDetailArea', id); }
  const bookArea = document.getElementById('bookDetailArea'); if(bookArea){ const id=getParam('id'); buildDetail('bookDetailArea', id); }
  if(document.getElementById('appsGrid')) renderApps();
  if(document.getElementById('booksGrid')) renderBooks();
  if(document.getElementById('homeGrid')) renderHome();
  const popularAnchor = document.getElementById('popularAnchor'); if(popularAnchor) popularAnchor.addEventListener('click', e=>{ e.preventDefault(); state.sort='popular'; renderAll(); window.scrollTo({top:700, behavior:'smooth'}); });
  initThreeBg();
}

window.toggleFav = toggleFav;
window.incDownload = incDownload;
document.addEventListener('DOMContentLoaded', init);
