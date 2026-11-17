import * as T from './three.module.min.js';
export function mount(stage){
 const kind=stage.dataset.model, host=stage.querySelector('.viewport');
 const renderer=new T.WebGLRenderer({antialias:true,alpha:true}); renderer.setPixelRatio(Math.min(devicePixelRatio,1.6));
 host.replaceChildren(renderer.domElement); const scene=new T.Scene(), g=new T.Group();scene.add(g);
 const camera=new T.PerspectiveCamera(32,1,.1,100);camera.position.set(3,2.2,5.5);camera.lookAt(0,0,0);
 scene.add(new T.HemisphereLight(0xffffff,0x707b89,2.2));
 const light=new T.DirectionalLight(0xffffff,3);light.position.set(4,6,3);scene.add(light);
 const a=getComputedStyle(stage).getPropertyValue('--accent').trim(), metal='#aaaeb0', sand='#e4ceab';
 function mesh(geo,col,x=0,y=0,z=0){const m=new T.Mesh(geo,new T.MeshStandardMaterial({color:col,roughness:.37,metalness:.18}));m.position.set(x,y,z);g.add(m);return m}
 const box=(w,h,d,c,x=0,y=0,z=0)=>mesh(new T.BoxGeometry(w,h,d),c,x,y,z);
 const cyl=(top,base,h,c,x=0,y=0,z=0,n=64)=>mesh(new T.CylinderGeometry(top,base,h,n),c,x,y,z);
 const ring=(r,t,c)=>mesh(new T.TorusGeometry(r,t,16,64),c);
 const ball=(r,c,x=0,y=0,z=0)=>mesh(new T.SphereGeometry(r,32,24),c,x,y,z);
 switch(kind){
 case 'wheel':ring(.9,.22,'#202328');ring(.78,.06,metal);for(let i=0;i<10;i++)box(.08,1.55,.12,metal).rotation.z=i*Math.PI/10;ball(.18,metal);break;
 case 'lamp':cyl(.48,.58,.12,a,0,-.85);cyl(.045,.045,1.3,metal,0,-.15);cyl(.28,.76,.6,sand,0,.62);break;
 case 'vase':mesh(new T.LatheGeometry([[.02,-.9],[.45,-.9],[.68,-.55],[.66,0],[.32,.5],[.3,.87],[.25,.87],[.25,.76]].map(([x,y])=>new T.Vector2(x,y)),80),sand);break;
 case 'cross':box(.5,1.7,.42,a);box(1.7,.5,.42,a);break;
 case 'ridge':for(let i=0;i<4;i++)cyl(0,.7+i*.05,1+i*.24,i%2?a:sand,(i-1.5)*.49,-.1,(i%2)*.4,5);break;
 case 'bag':box(1.55,1.12,.56,a,0,-.25);ring(.48,.07,sand).position.y=.43;break;
 case 'dish':cyl(.99,.69,.18,sand);cyl(.65,.4,.29,a,0,.16);break;
 case 'prism':mesh(new T.OctahedronGeometry(1.1),'#bc75e4');break;
 case 'blocks':for(let i=0;i<4;i++)box(.72,.72,.72,i%2?a:sand,(i%2)*.75-.38,Math.floor(i/2)*.73-.37,i===3?.4:0);break;
 case 'bottle':box(.9,1.22,.54,'#d3a074',0,-.14);cyl(.23,.23,.4,a,0,.66);box(.57,.4,.02,sand,0,-.15,.28);break;
 case 'plane':{const body=ball(.45,metal);body.scale.set(.58,.62,3);box(2.55,.065,.47,a);box(.99,.08,.27,metal,0,.1,-.98);box(.07,.39,.3,a,0,.2,-1);break}
 case 'golf':cyl(.17,.05,.68,sand,0,-.48);ball(.52,'#f9f7ea',0,.32);break;
 case 'track':for(let i=0;i<5;i++){const r=ring(.6+i*.09,.035,i%2?a:sand);r.scale.x=1.45;r.rotation.x=Math.PI/2}break;
 case 'scales':cyl(.4,.48,.1,metal,0,-.8);cyl(.045,.045,1.4,sand,0,-.05);box(1.55,.07,.07,sand,0,.6);for(const x of [-.7,.7]){cyl(.015,.015,.7,sand,x,.25);cyl(.36,.14,.15,metal,x,-.14)}break;
 case 'cards':case 'folio':for(let i=0;i<4;i++){const m=box(1.48,.95,.07,i%2?a:sand,i*.09-.12,i*.11-.15,i*.1);m.rotation.z=(i-1.5)*.12}break;
 case 'orbit':ball(.44,a);for(let i=0;i<3;i++){const r=ring(.94,.028,i%2?metal:a);r.rotation.set(.7*i,.9*i,.5)}break;
 case 'grid':for(let i=0;i<9;i++)box(.49,.16+(i%3)*.18,.49,i%2?a:sand,(i%3-1)*.57,0,(Math.floor(i/3)-1)*.57);break;
 }
 const draw=()=>renderer.render(scene,camera);
 new ResizeObserver(()=>{const w=host.clientWidth,h=host.clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();draw()}).observe(host);
 let prev;
 host.onpointerdown=e=>{prev=[e.clientX,e.clientY];host.setPointerCapture(e.pointerId)};
 host.onpointermove=e=>{if(prev){g.rotation.y+=(e.clientX-prev[0])*.012;g.rotation.x=Math.max(-1,Math.min(1,g.rotation.x+(e.clientY-prev[1])*.009));prev=[e.clientX,e.clientY];draw()}};
 host.onpointerup=host.onpointercancel=()=>{prev=null};
 stage.querySelectorAll('[data-turn]').forEach(b=>{b.disabled=false;b.onclick=()=>{g.rotation.y+=Number(b.dataset.turn);draw()}});
}
