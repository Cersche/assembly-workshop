const fs=require('fs'),vm=require('vm'),assert=require('assert');
const elements={},listeners={},requests=[];
const colorFrame={width:1,height:1,data:new Uint8ClampedArray([255,0,0,255])};
const ctx={createImageData(w,h){return {data:new Uint8ClampedArray(w*h*4)}},putImageData(){},setTransform(){},fillRect(){},fillText(){},setLineDash(){},drawImage(){},getImageData(){return colorFrame},beginPath(){},moveTo(){},lineTo(){},stroke(){}};
function element(){return {dataset:{},checked:true,value:1,clientWidth:200,getContext:()=>ctx,setPointerCapture(){}};}
for(const id of ['assemblyCanvas','assemblyStatus','assemblyZoom','assemblyReset','assemblyTop','assemblyJoint','show-tray','show-faceplate','show-hardware','hardwareStatus','piStatus','show-pi_reference'])elements[id]=element();
elements['show-pi_reference'].checked=false;
let loadModel;const modelPending=new Promise(r=>loadModel=r);
const box={document:{getElementById:id=>elements[id],createElement:element},window:{devicePixelRatio:1,assemblyAppearance:null,addEventListener:(name,fn)=>listeners[name]=fn},fetch:async url=>({ok:true,json:async()=>url==='/api/assembly'?modelPending:url==='/api/pi-reference'?{id:'pi_reference',vertices:[],triangles:[]}:{checks:[]}}),Image:class{constructor(){this.width=this.height=1}set src(v){requests.push(v)}async decode(){}},requestAnimationFrame:fn=>fn(),ResizeObserver:class{observe(){}}};
vm.createContext(box);
const initialized=vm.runInContext(fs.readFileSync('outputs/Mechanical_Design_App/viewer.js','utf8'),box);
// An assembly is opened while the baseline response is still loading.
box.window.assemblyAppearance={faceplate:'#123456',artwork:{sha256:'a'.repeat(64),x:.5,y:.5,scale:1}};
loadModel({revision:'Test baseline',parts:[{id:'faceplate',vertices:[[-10,-3,0],[10,-3,0],[0,-3,30]],triangles:[[0,1,2]]}]});
(async()=>{await initialized;await Promise.resolve();assert.equal(requests[0],'/api/artwork/'+'a'.repeat(64)+'.png');assert.equal(elements.assemblyCanvas.dataset.artwork,'preview-only');console.log('PASS saved artwork is replayed when an assembly opens before viewer initialization completes.');})().catch(e=>{console.error(e);process.exitCode=1});
