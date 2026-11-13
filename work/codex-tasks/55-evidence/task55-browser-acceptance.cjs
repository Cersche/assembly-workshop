// Operator-only browser acceptance; not imported or served by Bench.
// Uses the already installed Playwright runtime. No packages are installed.
const {chromium} = require('C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const assert = require('node:assert/strict');
const base = 'http://127.0.0.1:8875';
const repo = process.cwd();
const out = path.join(repo, 'work/codex-tasks/55-screens');
const log = [];
const record = (label, value) => {log.push({label,value}); console.log(label, JSON.stringify(value));};
let browser;
async function request(route, method='GET', body) {
  const state = method === 'GET' ? null : await request('/api/state');
  const response = await fetch(base+route, {method, headers:body ? {'Content-Type':'application/json','X-Bench-Token':state.token} : {}, body:body ? JSON.stringify(body) : undefined});
  assert.equal(response.status, 200, route);
  return response.json();
}
(async () => {
 const root = (await fs.readFile('tools/bench/task55-temp-root.txt','utf8')).trim();
 const catalog = path.join(root,'work/bench/projects.json');
 const original = await fs.readFile(catalog,'utf8');
 browser = await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 try {
  for (const width of [1280,375]) {
   const fixture = JSON.parse(original);
   for (const p of fixture.projects) if (p.id.startsWith('accept-')) {
    p.status=p.id.slice(7); p.updated='2026-11-01'; p.notes='Keep original notes';
    if(p.id==='accept-idea') Object.assign(p,{title:'Acceptance idea',device_cards:['docs/devices/lab-rax-top.md','docs/devices/fan-200mm.md'],sources:['outputs/Final_3MF/README.md','work/workbench/Workflow_Log.md']});
   }
   fixture.projects.push({id:'accept-overdue',title:'Acceptance overdue',prefixes:['QAOVERDUE'],status:'printing',updated:'2020-01-01',notes:'',device_cards:[],sources:[],workflow_log:''});
   fixture.projects.push({id:'accept-no-release',title:'Acceptance no release',prefixes:['QANORELEASE'],status:'report-due',updated:'2026-11-01',notes:'',device_cards:[],sources:[],workflow_log:''});
   await fs.writeFile(catalog,JSON.stringify(fixture,null,2),'utf8'); await request('/api/refresh','POST',{});
   const context = await browser.newContext({viewport:{width,height:900},colorScheme:'dark'});
   // Explicitly authorized by Brian: test confirm paths without native dialogs.
   await context.addInitScript(() => {window.__benchConfirmCalls=0;window.__benchConfirmResult=false;window.confirm=()=>{window.__benchConfirmCalls++;return window.__benchConfirmResult;};});
   const errors=[],nativeDialogs=[],expectedHttpErrors=[];let conflictExpected=false;
   const consoleError=m=>{if(m.type()!=='error')return;if(conflictExpected && /status of 409/.test(m.text()))expectedHttpErrors.push(m.text());else errors.push(m.text());};
   const page = await context.newPage();
   context.on('page', p => {p.on('pageerror',e=>errors.push(String(e)));p.on('console',consoleError);p.on('dialog',async d=>{nativeDialogs.push(d.type());await d.dismiss();});});
   page.on('pageerror',e=>errors.push(String(e)));page.on('console',consoleError);
   page.on('dialog',async d=>{nativeDialogs.push(d.type());await d.dismiss();});
   await page.goto(base);await page.locator('#main > .heading h2').waitFor();
   const clickProject = async id => {
    await page.locator('#projects [data-project="'+id+'"]').click();
    await page.waitForFunction(id=>document.querySelector('#projects [data-project="'+id+'"]').getAttribute('aria-current')==='true',id);
   };
   const statusIs = async value => {
    await page.waitForFunction(v=>document.querySelector('#status')?.value===v,value);
    await page.waitForFunction(()=>[...document.querySelectorAll('[data-status]')].every(b=>!b.disabled));
   };
   const snap = async name => {
    const size=await page.evaluate(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth}));
    assert.equal(size.width,width);assert.ok(size.documentWidth<=width,JSON.stringify(size));
    await page.screenshot({path:path.join(out,width+'-'+name+'.png')});record(width+' '+name,size);
   };
   await clickProject('fan');await page.locator('#viewer iframe').scrollIntoViewIfNeeded();
   await page.getByRole('button',{name:'TF-D_grille',exact:true}).waitFor();
   const checked = async () => page.frameLocator('#viewer iframe').locator('#parts input[type=checkbox]').evaluateAll(es=>es.map(e=>e.checked));
   assert.deepEqual(await checked(),[true,true,true,true]);
   await page.getByRole('button',{name:'TF-D_grille',exact:true}).click();
   await page.waitForFunction(()=>document.querySelector('#part-buttons button:last-child').getAttribute('aria-pressed')==='true');
   // Cross-frame changes are asynchronous: wait in the frame on the authoritative checkbox state.
   const frame = page.frames().find(f=>f.url().endsWith('/viewer/TF-D.html'));
   await frame.waitForFunction(()=>[...document.querySelectorAll('#parts input[type=checkbox]')].filter(c=>c.checked).length===1);
   assert.deepEqual(await checked(),[false,false,false,true]);
   assert.equal(await page.locator('#open-viewer').getAttribute('href'),'/viewer/TF-D.html#solo=TF-D_grille');
   await snap('solo');
   const popupPromise=page.waitForEvent('popup');await page.getByRole('link',{name:'Open 3D in new tab'}).click();const popup=await popupPromise;
   await popup.waitForLoadState('load');
   assert.deepEqual(await popup.locator('#parts input[type=checkbox]').evaluateAll(es=>es.map(e=>e.checked)),[false,false,false,true]);
   assert.ok(popup.url().endsWith('#solo=TF-D_grille'));await popup.screenshot({path:path.join(out,width+'-standalone.png')});await popup.close();
   await page.getByRole('button',{name:'All parts',exact:true}).click();
   await frame.waitForFunction(()=>[...document.querySelectorAll('#parts input[type=checkbox]')].every(c=>c.checked));
   assert.deepEqual(await checked(),[true,true,true,true]);assert.equal(await page.locator('#open-viewer').getAttribute('href'),'/viewer/TF-D.html');await snap('all-parts');
   await page.locator('#viewer-choice').selectOption({label:'TF-D_second.html'});
   await page.waitForFunction(()=>document.querySelector('#part-buttons button')?.getAttribute('aria-pressed')==='true');
   assert.equal(await page.locator('#open-viewer').getAttribute('href'),'/viewer/TF-D_second.html');assert.deepEqual(await checked(),[true,true,true,true]);
   await page.getByRole('button',{name:'TF-C',exact:true}).click();await page.getByRole('button',{name:'TF-C',exact:true}).getAttribute('aria-pressed').then(v=>assert.equal(v,'true'));
   assert.equal(await page.locator('#part-buttons').isVisible(),false); // fixture has no part list
   await clickProject('accept-idea');assert.equal(await page.locator('#open-viewer').count(),0);
   await page.getByRole('button',{name:'Edit details',exact:true}).click();
   assert.equal(await page.locator('#details-form [name=id]').count(),0);
   assert.equal(await page.locator('#detail-cards').inputValue(),'docs/devices/lab-rax-top.md\ndocs/devices/fan-200mm.md');
   assert.equal(await page.locator('#detail-sources').inputValue(),'outputs/Final_3MF/README.md\nwork/workbench/Workflow_Log.md');
   await page.locator('#detail-title').fill('Acceptance edited '+width);
   await page.locator('#detail-prefixes').fill('QATEST0, QAX'+width);
   await page.locator('#detail-workflow').fill('Cable management bracket (front to rear posts)');
   assert.equal(await page.getByRole('button',{name:'Start draft',exact:true}).isEnabled(),false);
   assert.equal(await page.locator('#quick-hint').innerText(),'Save or cancel your edits first');
   await snap('details');await page.getByRole('button',{name:'Save details',exact:true}).click();
   await page.waitForFunction(()=>document.querySelector('#message').textContent==='Job details saved.');
   assert.equal(await page.locator('#main > .heading h2').innerText(),'Acceptance edited '+width);
   const saved=(await request('/api/state')).projects.find(p=>p.id==='accept-idea');
   assert.equal(saved.workflow_log,'Cable management bracket (front to rear posts)');assert.equal(saved.device_cards.length,2);assert.equal(saved.sources.length,2);
   await page.locator('#notes').fill('Unsaved notes '+width);assert.equal(await page.getByRole('button',{name:'Start draft',exact:true}).isEnabled(),false);
   await page.getByRole('button',{name:'Edit details',exact:true}).click();await page.locator('#detail-title').fill('Independent detail save '+width);
   await page.getByRole('button',{name:'Save details',exact:true}).click();await page.waitForFunction(()=>document.querySelector('#message').textContent==='Job details saved.');
   assert.equal(await page.locator('#notes').inputValue(),'Unsaved notes '+width);
   assert.equal((await request('/api/state')).projects.find(p=>p.id==='accept-idea').notes,'Keep original notes');
   await page.getByRole('button',{name:'Cancel notes and status edits',exact:true}).click();assert.equal(await page.locator('#notes').inputValue(),'Keep original notes');
   // Confirm Cancel and Discard explicitly use the approved in-memory override.
   await page.getByRole('button',{name:'Edit details',exact:true}).click();await page.locator('#detail-title').fill('Discardable detail '+width);
   await page.evaluate(()=>{window.__benchConfirmResult=false;});
   await page.locator('#projects [data-project="accept-done"]').click();
   assert.equal(await page.locator('#detail-title').inputValue(),'Discardable detail '+width);
   assert.equal(await page.locator('#main > .heading h2').innerText(),'Independent detail save '+width);
   await page.evaluate(()=>{window.__benchConfirmResult=true;});await clickProject('accept-done');
   assert.equal(await page.locator('#main > .heading h2').innerText(),'Acceptance done');
   await page.evaluate(()=>{window.__benchConfirmResult=false;});record(width+' confirm Cancel/Discard',{calls:await page.evaluate(()=>window.__benchConfirmCalls),method:'window.confirm override; no native click'});
   // Notes use the same guard, checked independently.
   await page.locator('#notes').fill('Guarded notes');await page.locator('#projects [data-project="accept-idea"]').click();assert.equal(await page.locator('#notes').inputValue(),'Guarded notes');
   await page.evaluate(()=>{window.__benchConfirmResult=true;});await clickProject('accept-idea');await page.evaluate(()=>{window.__benchConfirmResult=false;});
   // Stale details preserve typed text and remain explicitly retryable.
   await page.getByRole('button',{name:'Edit details',exact:true}).click();await page.locator('#detail-title').fill('Stale draft kept '+width);
   conflictExpected=true;await fs.appendFile(catalog,'\n');await page.getByRole('button',{name:'Save details',exact:true}).click();
   await page.waitForFunction(()=>document.querySelector('#message').textContent.includes('your typed changes are kept'));
   assert.equal(await page.locator('#detail-title').inputValue(),'Stale draft kept '+width);conflictExpected=false;await snap('stale-details');
   await page.getByRole('button',{name:'Save details',exact:true}).click();await page.waitForFunction(()=>document.querySelector('#main > .heading h2').textContent.startsWith('Stale draft kept'));
   for (const [id,label,next] of [['idea','Start draft','draft'],['measuring','Start draft','draft'],['draft',"I'm printing it",'printing'],['printing','Printed, report due','report-due'],['report-due','Mark done','done'],['done','Reopen as draft','draft'],['parked','Reopen as draft','draft']]) {
    await clickProject('accept-'+id);
    if(id==='report-due') {
     await page.getByRole('button',{name:'Write fit report',exact:true}).click();assert.equal(await page.locator('#fit-id').inputValue(),'QATEST4-A');assert.equal(await page.locator('#status').inputValue(),'report-due');await snap('fit-report');
    }
    await page.getByRole('button',{name:label,exact:true}).click();await statusIs(next);
    const actual=(await request('/api/state')).projects.find(p=>p.id==='accept-'+id);assert.equal(actual.status,next);assert.equal(actual.notes,'Keep original notes');record(width+' quick '+id,next);
   }
   await clickProject('accept-no-release');await page.getByRole('button',{name:'Write fit report',exact:true}).click();assert.equal(await page.locator('#fit-id').inputValue(),'');assert.ok((await page.locator('#message').innerText()).includes('No release found.'));
   await clickProject('accept-idea');conflictExpected=true;await fs.appendFile(catalog,'\n');await page.getByRole('button',{name:"I'm printing it",exact:true}).click();
   await page.waitForFunction(()=>document.querySelector('#message').textContent.includes('your typed changes are kept'));assert.equal(await page.locator('#status').inputValue(),'draft');conflictExpected=false;
   await page.getByRole('button',{name:"I'm printing it",exact:true}).click();await statusIs('printing');
   await page.locator('#queue-view').click();await page.locator('#queue-view[aria-pressed=true]').waitFor();
   const queue=(await request('/api/state')).queue;assert.deepEqual(await page.locator('#projects [data-project]').evaluateAll(es=>es.map(e=>e.dataset.project)),queue.map(p=>p.id));
   const overdue=page.locator('#projects [data-project="accept-overdue"]');assert.ok((await overdue.innerText()).includes('no release found'));assert.ok((await overdue.innerText()).includes('overdue'));
   await snap('queue');await clickProject('accept-overdue');assert.equal(await page.locator('#main > .heading h2').innerText(),'Acceptance overdue');
   await page.reload();await page.locator('#queue-view[aria-pressed=true]').waitFor();record(width+' queue remembers view',true);
   const empty=JSON.parse(await fs.readFile(catalog,'utf8'));for(const p of empty.projects)p.status='done';await fs.writeFile(catalog,JSON.stringify(empty,null,2),'utf8');
   await page.getByRole('button',{name:'Refresh',exact:true}).click();await page.getByText('Nothing printing or waiting for a fit report.',{exact:true}).waitFor();await snap('empty-queue');
   record(width+' deliberately expected HTTP 409 logs',expectedHttpErrors);assert.equal(expectedHttpErrors.length,2);record(width+' browser errors',errors);record(width+' native fallback dialogs',nativeDialogs);
   assert.deepEqual(errors,[]);assert.deepEqual(nativeDialogs,[]);
   await context.close();
  }
 } finally {await fs.writeFile(catalog,original,'utf8');await request('/api/refresh','POST',{});await browser.close();}
 record('RESULT','PASS');
})().catch(async e=>{record('FAILURE',e.stack||String(e));try{await browser?.close();}catch{}process.exitCode=1;}).finally(async()=>{await fs.writeFile('tools/bench/task55-resumed-browser.json',JSON.stringify(log,null,2),'utf8');});
