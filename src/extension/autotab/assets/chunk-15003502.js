var O=Object.defineProperty;var w=(n,e,s)=>e in n?O(n,e,{enumerable:!0,configurable:!0,writable:!0,value:s}):n[e]=s;var c=(n,e,s)=>(w(n,typeof e!="symbol"?e+"":e,s),s);import{R as r,s as Q,c as y,d as m,N as d,e as k,f as T,g as i,h as g,T as l,E as C,G as D,L as K,H as G,n as p,I as L,C as M,a as x,i as A,b as P,K as U}from"./chunk-f0ce9ccd.js";const S=async(n,e)=>{const s=await fetch(n,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)});if(!s.ok)throw new Error(`Server error: ${s.status}`);return(await s.json()).map(o=>({type:"codeGenResponse",...o}))},h=n=>{chrome.tabs.query({active:!0,currentWindow:!0},function(e){e[0]&&e[0].id!==void 0&&chrome.tabs.sendMessage(e[0].id,n)})};let I=r.NOT_RECORDING,N=!1;const b=n=>{I=n},a=()=>I,R=n=>{N=n},V=()=>N,f=["Meta","Shift"];class W{constructor(e){c(this,"keyQueue");c(this,"elementInteractionQueue");c(this,"tabQueue");c(this,"tabs");c(this,"currentTabId");c(this,"baseUrl");this.keyQueue=[],this.elementInteractionQueue=[],this.tabQueue=[],this.baseUrl=e,this.tabs={},this.currentTabId=""}async dumpLogToServer(){if(this.keyQueue.length===0&&this.elementInteractionQueue.length===0&&this.tabQueue.length===0)return;chrome.runtime.sendMessage(Q);const e={keyQueue:this.keyQueue,elementInteractionQueue:this.elementInteractionQueue,tabQueue:this.tabQueue};this.keyQueue=[],this.elementInteractionQueue=[],this.tabQueue=[];try{const s=await S(`${this.baseUrl}/code/generate`,e);for(const t of s){const o={type:y,newCodeGenState:m.CODE_GENERATED,codeGenResponse:t};chrome.runtime.sendMessage(o)}}catch(s){const t={type:y,newCodeGenState:m.FAILED,error:s instanceof Error?s.message:JSON.stringify(s)};chrome.runtime.sendMessage(t)}}_broadcastRecordingStateUpdate(e){b(e.newRecordingState),h(e),chrome.runtime.sendMessage(e)}toggleRecording(){if(console.log("toggleRecording, current state:",a()),a()===r.RECORDING){this.dumpLogToServer();const e={type:d,newRecordingState:r.NOT_RECORDING};this._broadcastRecordingStateUpdate(e)}else{const e={type:d,newRecordingState:r.RECORDING};this._broadcastRecordingStateUpdate(e)}}toggleSelectElement(){if(a()===r.RECORDING_SELECT_ELEMENT){const e={type:d,newRecordingState:r.NOT_RECORDING};this._broadcastRecordingStateUpdate(e)}else{a()===r.RECORDING&&this.dumpLogToServer();const e={type:d,newRecordingState:r.RECORDING_SELECT_ELEMENT};this._broadcastRecordingStateUpdate(e)}}handleKeyDown(e){if(console.log("actionQueue key-down key:",e.key,"meta:",e.metaKey,"ctrl:",e.ctrlKey,"keyQueue:",this.keyQueue),console.log(a()),!f.includes(e.key)){if(e.key===k&&e.metaKey){console.log("KeyQueue: recording started"),this.toggleRecording();return}else if(e.key===T&&e.metaKey){console.log("KeyQueue: recording select element started"),this.toggleSelectElement();return}if(a()===r.RECORDING){const s=e.key;if(this.keyQueue.length>0){const t=this.keyQueue[this.keyQueue.length-1];if(t.key===s&&t.action===i.Down)return}this.keyQueue.push(new g(s,i.Down))}}}getCurrentKeysPressed(){return this.keyQueue.slice(-8).filter(t=>t.action===i.Down)}matchKeyDownIndex(e){const t=this.getCurrentKeysPressed().filter(o=>o.key===e);if(t.length>0){const o=this.keyQueue.lastIndexOf(t[t.length-1]);return this.keyQueue[o].action=i.Press,!0}return!1}handleKeyUp(e){if(console.log("actionQueue key-up key:",e.key,"meta:",e.metaKey,"ctrl:",e.ctrlKey,"keyQueue:",this.keyQueue),f.includes(e.key))return;if(e.key===k&&e.metaKey){console.log("KeyQueue: recording started"),this.toggleRecording();return}else if(e.key===T&&e.metaKey){console.log("KeyQueue: recording select element started"),this.toggleSelectElement();return}if(a()===r.NOT_RECORDING)return;if(this.keyQueue.length===0){e.key==="Enter"&&(this.keyQueue.push(new g(e.key,i.Press,e.tabId,e.url)),this.handleKeyTriggeredDump());return}if(this.keyQueue.findIndex(u=>u.key===e.key&&u.action===i.Down)===-1&&e.key!=="Enter")return;console.log("adding key up to keyQueue");const t=e.key;console.log("keyQueue length:",this.keyQueue.length);const o=t!=="Meta"&&this.matchKeyDownIndex(t);if(console.log("didMatch:",o,"key:",t,"key === Enter",t==="Enter"),t==="Enter"){console.log("enter key"),o?this.handleKeyTriggeredDump():(this.keyQueue.push(new g(t,i.Press,e.tabId,e.url)),this.handleKeyTriggeredDump());return}o||this.keyQueue.push(new g(t,i.Up,e.tabId,e.url))}hasKeys(){return this.keyQueue.length>0}_handleOpenTab(e,s){if(console.log("_handleOpenTab tabId:",e,"url:",s),this.tabs[e]===void 0){const t={id:e,index:Object.keys(this.tabs).length};console.log("new tab, initializing:",t),this.tabs[e]=t,t.index==0?this.tabQueue.push(new l(t.id,t.index,"load_url",s)):(this.tabQueue.push(new l(t.id,t.index,"open")),this.tabQueue.push(new l(t.id,t.index,"goto")),this.tabQueue.push(new l(t.id,t.index,"load_url",s))),this.currentTabId=t.id}else if(e!=this.currentTabId){console.log("tab change, enqueuing goto");const t=this.tabs[e];this.tabQueue.push(new l(t.id,t.index,"goto")),this.currentTabId=e}}handleKeyTriggeredDump(){const e=this.keyQueue[this.keyQueue.length-1];this._handleOpenTab(e.tabId,e.url),this.dumpLogToServer()}handleCloseTab(e){if(this.tabs[e]!==void 0){const s=this.tabs[e].index;this.tabQueue.push(new l(e,s,"close")),delete this.tabs[e];for(const t in this.tabs)this.tabs[t].index>s&&this.tabs[t].index--;this.dumpLogToServer()}}handleElementInteraction(e){this.elementInteractionQueue.push(new C(e)),this._handleOpenTab(e.tabId,e.url),this.dumpLogToServer()}handleOpenTab(e,s){this._handleOpenTab(e,s),this.dumpLogToServer()}}const E=new W("https://api.autotab.com"),_=async n=>{if(console.log("handleElementInteraction"),a()===r.NOT_RECORDING){console.error("handleElementInteraction called even though is not recording");return}try{console.log("data:",n.DOM),E.handleElementInteraction(n)}catch(e){console.log("Error in chat completion:",e)}},j=async n=>{E.handleKeyDown(n.event)},Y=async n=>{E.handleKeyUp(n.event)},q=async n=>{try{chrome.runtime.sendMessage(Q),console.log("handling refine code event:",n);const e=await S("https://api.autotab.com/code/refine",n);console.log("Code gen response received in refine code",e);for(const s of e){const t={type:y,newCodeGenState:m.CODE_GENERATED,codeGenResponse:{...s,blockOrder:n.blockOrder}};chrome.runtime.sendMessage(t)}}catch(e){console.log("Error in chat completion:",e)}};console.info("chrome-ext template-react-ts background script");chrome.sidePanel.setPanelBehavior({openPanelOnActionClick:!0});chrome.runtime.onMessage.addListener((n,e,s)=>{if(console.log("background received message:",n,"sender:",e,"sendResponse:",s),!V())return!1;try{switch(n.type){case U:j(n);break;case P:Y(n);break;case A:q(n);break;case x:_(n);break;case M:case L:case G:_(n),b(r.NOT_RECORDING),chrome.runtime.sendMessage(p),h(p);break;case K:chrome.runtime.sendMessage(n);break;case D:return chrome.tabs.query({active:!0,currentWindow:!0},function(t){const o=t[0].id,u=t[0].url;o&&u?s({tabId:o,url:u}):console.error("Could not get tabId or url from tabs",o,u)}),!0;case d:console.log("backend NEW_RECORDING_STATE_EVENT:",n.newRecordingState),b(n.newRecordingState),h(n);break;default:h(n),console.log("Ignoring message",n)}}catch(t){console.log("Error in background listener:",t)}return!0});chrome.runtime.onConnect.addListener(n=>{n.name==="mySidepanel"&&(chrome.storage.local.set({isSidePanelOpen:!0}),R(!0),n.onDisconnect.addListener(()=>{h(p),chrome.storage.local.set({isSidePanelOpen:!1}),R(!1)}))});chrome.tabs.onRemoved.addListener(n=>{E.handleCloseTab(n.toString())});chrome.tabs.onUpdated.addListener((n,e,s)=>{e.url&&console.log("tab change","id:",n,"index:",s.index,"changeInfo:",e)});
