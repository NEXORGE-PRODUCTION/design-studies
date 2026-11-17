const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const reveal=new IntersectionObserver(entries=>entries.forEach(({isIntersecting,target})=>{
 if(isIntersecting){if(!reduced)target.animate([{opacity:.35,transform:'translateY(18px)'},{opacity:1,transform:'none'}],{duration:540,easing:'ease-out'});reveal.unobserve(target)}
}));
document.querySelectorAll('.chapter').forEach(el=>reveal.observe(el));
const stage=document.querySelector('[data-model]');
if(stage)new IntersectionObserver((entries,observer)=>{if(entries.some(e=>e.isIntersecting)){observer.disconnect();import('./viewer.js').then(m=>m.mount(stage)).catch(()=>{stage.querySelector('.model-note').textContent='The interactive view requires WebGL. The editorial photograph is available here.'})}}, {rootMargin:'260px'}).observe(stage);
const form=document.querySelector('.workbook');
if(form)form.addEventListener('submit',e=>{
 e.preventDefault();const data=new FormData(form);
 const text=[form.dataset.title,String(data.get('focus')),String(data.get('notes'))].filter(Boolean).join('\n\n');
 const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download=form.dataset.slug+'-notes.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
for(const choice of document.querySelectorAll('[data-choice]')){
 choice.onclick=()=>{
  document.querySelectorAll('[data-choice]').forEach(b=>b.setAttribute('aria-pressed',String(b===choice)));
  document.querySelectorAll('[data-answer]').forEach(panel=>panel.hidden=panel.dataset.answer!==choice.dataset.choice);
 };
}
