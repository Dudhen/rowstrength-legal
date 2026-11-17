(function(){'use strict';
const dict=window.RS_STRINGS||{};const supported=['ru','en','de','fr','es'];
let code=new URLSearchParams(location.search).get('lang');
if(!supported.includes(code)){try{code=localStorage.getItem('rs.lang')}catch(_){}}
if(!supported.includes(code)){code=(navigator.language||'en').slice(0,2).toLowerCase()}
if(!supported.includes(code))code='en';
const selectors=document.querySelectorAll('#site-language');
function apply(lang){if(!supported.includes(lang))return;code=lang;document.documentElement.lang=lang;
try{localStorage.setItem('rs.lang',lang)}catch(_){}
const t=dict[lang]||dict.en||{};
document.querySelectorAll('[data-i18n]').forEach(e=>{const key=e.getAttribute('data-i18n');const v=t[key]||dict.en?.[key];if(v!==undefined)e.textContent=v});
document.querySelectorAll('a[data-local-nav]').forEach(a=>{const href=a.getAttribute('href');if(!href||href.startsWith('#'))return;try{const u=new URL(href,location.href);u.searchParams.set('lang',lang);a.href=u.pathname+u.search+u.hash}catch(_){}});
selectors.forEach(s=>s.value=lang);
if(typeof window.renderLegalSummary==='function')window.renderLegalSummary(lang);
if(typeof window.applyDeleteTranslations==='function')window.applyDeleteTranslations(lang);
}
selectors.forEach(s=>s.addEventListener('change',()=>apply(s.value)));
window.rsTranslate=apply;
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>apply(code));else apply(code);
})();
