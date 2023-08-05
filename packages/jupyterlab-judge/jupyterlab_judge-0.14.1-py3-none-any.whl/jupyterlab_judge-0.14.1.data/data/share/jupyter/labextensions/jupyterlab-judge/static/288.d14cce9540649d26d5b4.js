"use strict";(self.webpackChunkjupyterlab_judge=self.webpackChunkjupyterlab_judge||[]).push([[288],{3288:(e,t,s)=>{s.r(t),s.d(t,{IJudgePanelFactoryRegistry:()=>L,IJudgeSignal:()=>B,IJudgeSubmissionAreaFactoryRegistry:()=>$,IJudgeTerminalFactoryRegistry:()=>D,IProblemProviderRegistry:()=>R,ISubmissionListFactoryRegistry:()=>W,default:()=>Me,openOrCreateFromId:()=>T});var n=s(9239),o=s(2884),i=s(8604),r=s(3215),a=s(5257),l=s(4221),d=s(4003),u=s(9713),c=s(3849),m=s(6271),h=s.n(m);const g="jupyterlab-judge",p="judgedrive",b=".jce-judge",_="jupyterlab-judge";var y;!function(e){function t(e,t){const s=t.load(g);function n(){if(e.context.model.readOnly)return(0,o.showDialog)({title:s.__("Cannot Save"),body:s.__("Document is read-only"),buttons:[o.Dialog.okButton({label:s.__("Ok")})]});e.context.save().then((()=>{if(!e.isDisposed)return e.context.createCheckpoint()}))}return(0,o.addToolbarButtonClass)(o.ReactWidget.create(m.createElement(o.UseSignal,{signal:e.context.fileChanged},(()=>m.createElement(o.ToolbarButtonComponent,{icon:r.saveIcon,onClick:n,tooltip:s.__("Save the judge contents and create checkpoint"),enabled:!!(e&&e.context&&e.context.contentsModel&&e.context.contentsModel.writable)})))))}e.createSaveButton=t,e.getDefaultItems=function(e,s,n){return[{name:"save",widget:t(e,s)}]}}(y||(y={}));var C=s(1431);class f extends C.BoxPanel{constructor(e){super(),this.addClass("jp-JudgePanel"),this._context=e.context,this._translator=e.translator,this._trans=this._translator.load(g),this._submitted=e.submitted,this.id="jce-judge-panel",this.title.closable=!0;const t=new C.SplitPanel({spacing:0});t.addClass("jp-JudgePanel-splitPanel"),this._editorWidget=new a.CodeEditorWrapper({model:this.model.codeModel,factory:(new u.CodeMirrorEditorFactory).newInlineEditor,config:Object.assign(Object.assign({},e.editorConfig),{lineNumbers:!0})}),this._editorWidget.addClass("jp-JudgePanel-editor"),this._markdownRenderer=e.rendermime.createRenderer("text/markdown"),this._markdownRenderer.addClass("jp-JudgePanel-markdown"),this.renderProblem(),this.model.problemChanged.connect(((e,t)=>{this.renderProblem(),(null==t?void 0:t.title)&&(this.title.label=`${null==t?void 0:t.title}.judge`)})),this._terminal=e.judgeTerminalFactory({panel:this,model:this.model.outputAreaModel,rendermime:e.rendermime,translator:this._translator}),this._terminal.addClass("jp-JudgePanel-terminal");const s=e.judgeSubmissionAreaFactory({panel:this,model:this.model,translator:this._translator,submissionListFactory:e.submissionListFactory});s.addClass("jp-JudgePanel-submissionPanel"),t.addWidget(this._markdownRenderer);const n=new C.SplitPanel({orientation:"vertical",spacing:0});n.addClass("jp-JudgePanel-rightPanel"),n.addWidget(this._editorWidget),n.addWidget(this._terminal),n.addWidget(s),t.addWidget(n),this.addWidget(t),this.session.isReady||this.session.initialize()}get model(){return this.context.model}get editor(){return this._editorWidget.editor}get session(){return this.context.sessionContext}get context(){return this._context}renderProblem(){var e,t;this._markdownRenderer.renderModel(new d.MimeModel({data:{"text/markdown":null!==(t=null===(e=this.model.problem)||void 0===e?void 0:e.content)&&void 0!==t?t:this._trans.__("Problem Not Available.")}}))}handleEvent(e){this.model&&"mousedown"===e.type&&this._ensureFocus()}onAfterAttach(e){super.onAfterAttach(e),this.node.addEventListener("mousedown",this)}onBeforeDetach(e){this.node.removeEventListener("mousedown",this)}onActivateRequest(e){this._ensureFocus()}_ensureFocus(){this.session.pendingInput||this.editor.hasFocus()||this.editor.focus()}async execute(){if(this.session.hasNoKernel&&(await o.sessionContextDialogs.selectKernel(this.session),this.session.hasNoKernel))return(0,o.showDialog)({title:this._trans.__("Cell not executed due to missing kernel"),body:this._trans.__("The cell has not been executed because no kernel selected. Please select a kernel to execute the cell."),buttons:[o.Dialog.okButton({label:this._trans.__("Ok")})]}),null;if(this.session.pendingInput)return(0,o.showDialog)({title:this._trans.__("Cell not executed due to pending input"),body:this._trans.__("The cell has not been executed to avoid kernel deadlock as there is another pending input! Submit your pending input and try again."),buttons:[o.Dialog.okButton({label:this._trans.__("Ok")})]}),null;let e;try{const t=this.model.source;e=await c.OutputArea.execute(t,this._terminal.outputArea,this.session,{})}catch(e){if(!(e instanceof Error&&"Canceled future for execute_request message before replies were done"===e.message))throw e}return await this.session.restartKernel(),e||null}async judge(){var e,t;const s=this.model.problem;if(null===s)throw new Error("Problem cannot be found.");const n=null===(e=this.session.session)||void 0===e?void 0:e.kernel;if(!n)return void o.sessionContextDialogs.selectKernel(this.session);const i=new o.SessionContext({sessionManager:this.session.sessionManager,specsManager:this.session.specsManager,name:"Judge"});await i.initialize(),await i.changeKernel(await n.spec);const r=null===(t=i.session)||void 0===t?void 0:t.kernel;if(!r)return void o.sessionContextDialogs.selectKernel(i);const a=await this.model.getTestCases(),l=[];this.model.submissionStatus={inProgress:!0,runCount:0,totalCount:a.length};for(const e of a){const t=await this.runWithInput(r,s,e);l.push(t),this.model.submissionStatus={inProgress:!0,runCount:l.length,totalCount:a.length}}let d=null;const u=await this.model.validate(l.map((e=>e.output)));d=u.acceptedCount===u.totalCount?"AC":l.some((e=>"RE"===e.status))?"RE":l.some((e=>"OLE"===e.status))?"OLE":l.some((e=>"TLE"===e.status))?"TLE":"WA",await r.shutdown(),r.dispose();const c=await this.model.submit({problemId:s.id,status:d,code:this.model.source,cpuTime:l.map((e=>e.cpuTime)).reduce(((e,t)=>e+t),0)/l.length,acceptedCount:u.acceptedCount,totalCount:u.totalCount,token:u.token,language:"python",memory:0});this.model.submissionStatus={inProgress:!1,runCount:0,totalCount:0},this._submitted.emit({widget:this,submission:c,problem:s})}async runWithInput(e,t,s,n=!1){const o={code:this.model.source,stop_on_error:!0,allow_stdin:!0};n&&await e.restart();const i=new Promise(((t,s)=>{const n=(s,o)=>{"idle"===o&&(e.statusChanged.disconnect(n),t())};"idle"===e.status?t():e.statusChanged.connect(n)}));await i;let r=[];r="one_line"===t.inputTransferType?s.split(/\r?\n/):[s];const a=Date.now(),l=e.requestExecute(o,!0,{});l.onStdin=e=>{if("input_request"===e.header.msg_type){const t=r.shift();l.sendInputReply({value:null!=t?t:"",status:"ok"},e.header)}};const d={output:"",status:"OK",cpuTime:0};l.onIOPub=e=>{switch(e.header.msg_type){case"stream":{const t=e;"stdout"===t.content.name&&(d.output=d.output.concat(t.content.text));break}case"error":d.status="RE"}};const u=1e3*t.timeout,c=new Promise((e=>{setTimeout((()=>{e(0)}),1.2*u)}));if(0===await Promise.race([l.done,c]))l.dispose(),await e.interrupt(),d.status="TLE";else{const e=Date.now()-a;e>u?d.status="TLE":d.cpuTime=e}return d}}class w extends l.DocumentWidget{constructor(e){super(e),y.getDefaultItems(this.content,e.translator).forEach((e=>{this.toolbar.addItem(e.name,e.widget)}))}}class x extends l.ABCWidgetFactory{constructor(e){super(e.factoryOptions),this._rendermime=e.rendermime,this._commands=e.commands,this._editorConfig=e.editorConfig,this._judgePanelFactory=e.judgePanelFactory,this._judgeSubmissionAreaFactory=e.judgeSubmissionAreaFactory,this._judgeTerminalFactory=e.judgeTerminalFactory,this._submissionListFactory=e.submissionListFactory,this._submitted=e.submitted}createNewWidget(e){const t=this._judgePanelFactory({rendermime:this._rendermime,editorConfig:this._editorConfig,context:e,translator:this.translator,submitted:this._submitted,judgeSubmissionAreaFactory:this._judgeSubmissionAreaFactory,judgeTerminalFactory:this._judgeTerminalFactory,submissionListFactory:this._submissionListFactory});return t.title.icon=r.textEditorIcon,new w({content:t,context:e,commands:this._commands,translator:this.translator})}}var v,S=s(5613),j=s(4501),I=s(3559),P=s(7953),F=s(1840),k=s(3207);class E{constructor(e){this._contentChanged=new F.Signal(this),this._stateChanged=new F.Signal(this),this._isDisposed=!1,this._problemChanged=new F.Signal(this),this._submissionsChanged=new F.Signal(this),this._submissionStatus={inProgress:!1,runCount:0,totalCount:0},this._submissionStatusChanged=new F.Signal(this),this.modelDB=new P.ModelDB,this.sharedModel=new E.YJudge,this.sharedModel.changed.connect((async(e,t)=>{t.problemIdChange&&(this._problem=await this._problemProvider.getProblem(t.problemIdChange),this._problemChanged.emit(this._problem))})),this._codeModel=new k.CodeCellModel({}),this._codeModel.mimeType="text/x-python",this.sharedModel.ycodeCellChanged.connect(((e,t)=>{this._codeModel.switchSharedModel(t,!0)})),this._problem=null,this._problemProvider=e}get contentChanged(){return this._contentChanged}get stateChanged(){return this._stateChanged}get dirty(){return this.sharedModel.dirty}set dirty(e){e!==this.dirty&&(this.sharedModel.dirty=e)}get readOnly(){return!1}set readOnly(e){}get isDisposed(){return this._isDisposed}dispose(){this.isDisposed||(this._isDisposed=!0,F.Signal.clearData(this))}initialize(){}get defaultKernelName(){return`Judge: Problem ${this.sharedModel.getProblemId()}`}get defaultKernelLanguage(){return"python"}get codeModel(){return this._codeModel}get source(){return this.sharedModel.getSource()}set source(e){this.sharedModel.setSource(e)}get outputAreaModel(){return this._codeModel.outputs}get problem(){return this._problem}get problemChanged(){return this._problemChanged}async submissions(){return await this._problemProvider.getSubmissions(this.sharedModel.getProblemId())}get submissionsChanged(){return this._submissionsChanged}get submissionStatus(){return this._submissionStatus}set submissionStatus(e){this._submissionStatus=e,this._submissionStatusChanged.emit(this._submissionStatus)}get submissionStatusChanged(){return this._submissionStatusChanged}toString(){return JSON.stringify(this.toJSON())}fromString(e){try{this.fromJSON(JSON.parse(e))}catch(e){if(!(e instanceof SyntaxError))throw e;this.fromJSON({problem_id:"",code:"",judge_format:1})}}toJSON(){return{problem_id:this.sharedModel.getProblemId(),code:this.sharedModel.getSource(),judge_format:1}}fromJSON(e){var t,s;this.sharedModel.createCellModelFromSource(null!==(t=e.code)&&void 0!==t?t:"# 파일이 손상되었습니다. 파일을 삭제하고 새로 생성해주세요."),this.sharedModel.setProblemId(null!==(s=e.problem_id)&&void 0!==s?s:"")}async getTestCases(){return await this._problemProvider.getTestCases(this.sharedModel.getProblemId())}async validate(e){return await this._problemProvider.validate(this.sharedModel.getProblemId(),e)}async submit(e){const t=await this._problemProvider.submit(e);return this._submissionsChanged.emit(await this._problemProvider.getSubmissions(this.sharedModel.getProblemId())),t}}async function T(e,t,s){const n=await e.getProblem(s);if(n){const o=n.title,i=`${p}:${b}/${s}/${o}.judge`,r=`${p}:${b}`;await t.services.contents.save(r,{name:r,type:"directory"});const a=`${p}:${b}/${s}`;return await t.services.contents.save(a,{name:a,type:"directory"}),await async function(e,t,s,n){try{await t.services.contents.get(s)}catch(o){throw o instanceof S.ServerConnection.ResponseError&&404===o.response.status&&await t.services.contents.save(s,{name:s,type:"file",format:"text",content:await E.newFileContent(e,n)}),o}finally{return t.openOrReveal(s)}}(e,t,i,s)}}!function(e){e.JudgeModelFactory=class{constructor(e){this._disposed=!1,this._problemProviderFactory=e.problemProviderFactory}get name(){return"judge-model"}get contentType(){return"file"}get fileFormat(){return"text"}get isDisposed(){return this._disposed}dispose(){this._disposed=!0}preferredLanguage(e){return"python"}createNew(t,s){return new e(this._problemProviderFactory())}};class t extends j.YDocument{constructor(){super(),this.undoManager=new I.UndoManager([this._cell()],{trackedOrigins:new Set([this])}),this._yproblemId=this.ydoc.getText("problemId"),this._ycodeCellChanged=new F.Signal(this),this._yproblemId.observe((e=>{this._changed.emit({problemIdChange:this.getProblemId()})})),this._ycodeCell=null,this._cell().observe(((e,t)=>{e.changes.keys.get("id")&&this._switchCodeCell(this._cell())}))}createCellModelFromSource(e){this.transact((()=>{const t=this._cell();t.set("source",new I.Text(e)),t.set("metadata",{}),t.set("cell_type","code"),t.set("id",""),t.set("execution_count",0),t.set("outputs",new I.Array)})),this._switchCodeCell(this._cell())}_cell(){return this.ydoc.getMap("cell")}_switchCodeCell(e){const t=this._ycodeCell;this._ycodeCell=new s(e,this),this._ycodeCell.undoManager=this.undoManager,this.undoManager.clear(),this._ycodeCellChanged.emit(this._ycodeCell),this._ycodeCell.changed.connect(((e,t)=>{t.sourceChange&&(this.dirty=!0)})),null==t||t.dispose()}get changed(){return this._changed}get ycodeCellChanged(){return this._ycodeCellChanged}dispose(){}get yCodeCell(){return this._ycodeCell}getProblemId(){return this._yproblemId.toString()}setProblemId(e){this.transact((()=>{const t=this._yproblemId;t.delete(0,t.length),t.insert(0,e)}))}getSource(){var e,t;return null!==(t=null===(e=this._ycodeCell)||void 0===e?void 0:e.getSource())&&void 0!==t?t:""}setSource(e){this._ycodeCell&&this._ycodeCell.setSource(e)}}e.YJudge=t;class s extends j.YCodeCell{constructor(e,t){super(e),this._yjudge=t}get awareness(){return this._yjudge.awareness}}e.newFileContent=async function(e,t){var s,n;const o={problem_id:t,code:null!==(n=null===(s=await e.getProblem(t))||void 0===s?void 0:s.skeletonCode)&&void 0!==n?n:"# 여기에 입력하세요",judge_format:1};return JSON.stringify(o)}}(E||(E={})),function(e){e.open=`${_}:plugin:open`,e.openOrCreateFromId=`${_}:plugin:open-or-create-from-id`,e.execute=`${_}:plugin:execute`}(v||(v={}));var M=s(3619),N=s(5643),A=s(9448),J=s(1194),O=s(1526);const R=new O.Token(`${_}:IProblemProviderRegistry`),L=new O.Token(`${_}:IJudgePanelFactoryRegistry`),$=new O.Token(`${_}:IJudgeSubmissionAreaFactoryRegistry`),D=new O.Token(`${_}:IJudgeTerminalFactoryRegistry`),W=new O.Token(`${_}:ISubmissionListFactoryRegistry`),B=new O.Token(`${_}:IJudgeSignal`);var z=s(3848),K=s(8149),q=s.n(K);const H=q().div`
  background: var(--jp-layout-color2);
`,Q=q().button`
  display: block;
  margin-top: 12px;
  margin-left: 20px;
  margin-right: 20px;
  padding: 11px 17px;

  cursor: pointer;

  border: none;

  background: var(--jp-brand-color1);

  /* Shadow-2 */
  box-shadow: 0px 0.15px 0.45px rgba(0, 0, 0, 0.11),
    0px 0.8px 1.8px rgba(0, 0, 0, 0.13);
  border-radius: 8px;

  font-family: var(--jp-ui-font-family);
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 22px;
  /* identical to box height, or 138% */

  color: var(--jp-ui-inverse-font-color0);

  :disabled {
    background: var(--jp-layout-color3);
    cursor: not-allowed;
  }

  :not(:disabled):hover {
    background: var(--jp-brand-color0);
  }
`;var U=s(6848);const Y=q().span``,G=q().li`
  display: flex;
  padding: 5px 12px;
  height: 16px;

  font-family: var(--jp-ui-font-family);
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
`,V=q()((function(e){const t=(0,m.useContext)(he);let s="",n="";switch(e.status){case"AC":s=`👍 ${t.__("Accepted")}`;break;case"WA":s=`❌ ${t.__("Wrong")}`,n=`(${e.acceptedCount}/${e.totalCount})`;break;case"RE":s=`🚫 ${t.__("Error")}`;break;case"TLE":s=`🕓 ${t.__("Time Limit")}`;break;case"OLE":s=`👀 ${t.__("Output Limit")}`;break;case"IE":s=`☠ ${t.__("Please Try Again")}`}return h().createElement(Y,{className:e.className,title:n},s)}))`
  height: 16px;
  flex-grow: 0;
  flex-shrink: 0;

  width: 101px;
  margin-right: 8px;
`,X=q().button`
  height: 16px;
  flex-grow: 0;
  flex-shrink: 0;

  all: unset;
  cursor: pointer;

  font-family: var(--jp-ui-font-family);
  font-style: normal;
  font-weight: 700;
  font-size: 12px;
  line-height: 16px;
  color: var(--jp-brand-color1);
`,Z=q().span`
  height: 16px;
  flex-grow: 1;
  flex-shrink: 1;

  text-align: right;

  font-family: var(--jp-ui-font-family);
  font-style: normal;
  font-weight: 400;
  font-size: 12px;
  line-height: 16px;

  color: var(--jp-ui-font-color3);
`,ee=q().span``,te=q().li`
  display: flex;
  padding: 5px 12px;
  height: 16px;

  font-family: var(--jp-ui-font-family);
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
`,se=q()((function(e){const{status:t}=e,s=(0,m.useContext)(he);return t.inProgress?h().createElement(ee,{className:e.className},`⌛ ${s.__("In Progress")} (${t.runCount}/${t.totalCount})`):h().createElement(h().Fragment,null)}))`
  height: 16px;
  flex-grow: 0;
  flex-shrink: 0;

  width: 101px;
  margin-right: 8px;
`;function ne(e){const t=(0,m.useContext)(he);if(null===e.problemId)return h().createElement(ae,{className:e.className},"⌛ ",t.__("Loading History"));const{data:s,isLoading:n}=(0,z.useQuery)(["submissions",e.problemId],e.getSubmissions);if(n)return h().createElement(ae,{className:e.className},"⌛ ",t.__("Loading History"));if(void 0===s)return h().createElement(ae,{className:e.className},"🚫 ",t.__("History Not Available"));const o=e.submissionStatus&&e.submissionStatus.inProgress;return 0!==s.length||o?h().createElement(oe,{className:e.className},e.submissionStatus&&e.submissionStatus.inProgress&&h().createElement(re,{status:e.submissionStatus}),s.map((t=>h().createElement(ie,{submission:t,key:t.id,setCode:e.setCode})))):h().createElement(le,{className:e.className},t.__("Submit your code to get results here."))}const oe=q().ul`
  padding: 7px 0px 0px 0px;
  margin: 0px;

  overflow-y: auto;

  /* width */
  ::-webkit-scrollbar {
    width: 2px;
  }

  /* Handle */
  ::-webkit-scrollbar-thumb {
    background: var(--jp-border-color0);
    border-radius: 12px;
  }
`,ie=q()((function(e){const t=(0,m.useContext)(he),s=U.Time.formatHuman(new Date(e.submission.createdAt)),n=U.Time.format(new Date(e.submission.createdAt),"lll");return h().createElement(G,{className:e.className},h().createElement(V,{status:e.submission.status,acceptedCount:e.submission.acceptedCount,totalCount:e.submission.totalCount}),h().createElement(X,{onClick:()=>{e.setCode(e.submission.code)},title:e.submission.code.substring(0,1e3)},t.__("Load this submission")),h().createElement(Z,{title:n},s))}))``,re=q()((function(e){return h().createElement(te,{className:e.className},h().createElement(se,{status:e.status}))}))``,ae=q().div`
  text-align: center;
  padding: 5px;
  font-size: var(--jp-ui-font-size2);
`,le=q().div`
  padding: 12px;
  font-weight: 700;
  font-size: 12px;
  line-height: 16px;
  color: var(--jp-ui-font-color3);
`;function de(e){const t=(0,m.useContext)(he);return null===e.model?h().createElement("div",null,t.__("No Submission History Found.")):h().createElement(ue,null,h().createElement(ce,{model:e.model}),h().createElement(me,{panel:e.panel}))}const ue=q().div`
  display: flex;
  border-top: 4px solid var(--jp-border-color0);
  font-size: var(--jp-ui-font-size1);

  height: 100%;
`,ce=q()((function(e){const t=(0,z.useQueryClient)(),{submissionListFactory:s}=(0,m.useContext)(ge);return h().createElement(o.UseSignal,{signal:e.model.problemChanged,initialSender:e.model,initialArgs:e.model.problem},((n,i)=>h().createElement(o.UseSignal,{signal:e.model.submissionsChanged,initialSender:e.model},((n,r)=>{var a;const l=null!==(a=null==i?void 0:i.id)&&void 0!==a?a:null;return l&&t.invalidateQueries(["submissions",l]),h().createElement(o.UseSignal,{signal:e.model.submissionStatusChanged,initialSender:e.model,initialArgs:e.model.submissionStatus},((t,n)=>h().createElement(s,{className:e.className,problemId:l,getSubmissions:async()=>{const t=await e.model.submissions();return null!=t?t:[]},setCode:t=>{e.model.source=t},submissionStatus:null!=n?n:null})))}))))}))`
  flex-grow: 1;
  flex-shrink: 1;

  margin-right: 2px;
`,me=q()((function(e){const t=(0,m.useContext)(he),[s,n]=(0,m.useState)(!1);return h().createElement(H,{className:e.className},h().createElement(Q,{onClick:async()=>{n(!0),await e.panel.judge(),n(!1)},disabled:s},t.__("Submit")))}))`
  flex-grow: 0;
  flex-shrink: 0;
`,he=h().createContext(i.nullTranslator.load(g)),ge=h().createContext({submissionListFactory:ne});class pe extends o.ReactWidget{constructor(e){super(),this.queryClient=new z.QueryClient,this._panel=e.panel,this._model=e.model,this._translator=e.translator,this._submissionListFactory=e.submissionListFactory}render(){var e,t;return h().createElement(ge.Provider,{value:{submissionListFactory:this._submissionListFactory}},h().createElement(he.Provider,{value:this._translator.load(g)},h().createElement(z.QueryClientProvider,{client:this.queryClient},h().createElement(de,{key:null!==(t=null===(e=this._model.problem)||void 0===e?void 0:e.id)&&void 0!==t?t:"",panel:this._panel,model:this._model}))))}}const be="jp-OutputArea-output";class _e extends c.OutputArea{constructor(e){super(e),this.addClass("jp-JudgeOutputArea");const t=e.translator.load(g),s=document.createElement("div");s.className="jp-JudgeOutputArea-placeholder",s.textContent=t.__("Execution result will be shown here"),this.node.appendChild(s)}createOutputItem(e){const t=this.createRenderedMimetype(e);return t&&t.addClass(be),t}onInputRequest(e,t){const s=this.contentFactory,n=e.content.prompt,o=e.content.password,i=new C.Panel;i.addClass("jp-OutputArea-child"),i.addClass("jp-OutputArea-stdin-item");const r=s.createStdin({prompt:n,password:o,future:t});r.addClass(be),i.addWidget(r),this.layout.addWidget(i),r.value.then((e=>{this.model.add({output_type:"stream",name:"stdin",text:e+"\n"}),i.dispose()}))}}class ye extends C.Panel{constructor(e){super(),this.addClass("jp-JudgeTerminal");const t=e.translator.load(g),s=new C.Widget;s.addClass("jp-JudgeTerminal-toolbar");const n=document.createElement("button");n.className="jp-JudgeTerminal-executeButton",r.runIcon.element({container:n});const o=document.createElement("span");o.className="jp-JudgeTerminal-executeButtonLabel",o.textContent=t.__("Execute"),n.addEventListener("click",(async()=>{n.disabled=!0;try{await e.panel.execute()}catch(e){throw n.disabled=!1,e}n.disabled=!1})),n.appendChild(o);const i=document.createElement("div");i.className="jp-JudgeTerminal-seperator";const a=document.createElement("button");a.className="jp-JudgeTerminal-stopButton",r.stopIcon.element({container:a});const l=document.createElement("span");l.className="jp-JudgeTerminal-stopButtonLabel",l.textContent=t.__("Stop"),a.addEventListener("click",(async()=>{await e.panel.session.shutdown()})),a.appendChild(l),s.node.appendChild(n),s.node.appendChild(i),s.node.appendChild(a),this.addWidget(s),this._outputArea=new _e(e),this.addWidget(this._outputArea)}get outputArea(){return this._outputArea}}const Ce=new F.Signal({}),fe={id:`${_}:IJudgeSignal`,provides:B,activate:e=>({get submitted(){return Ce}}),autoStart:!0};let we=new class{constructor(){this.problems={1:{id:"1",title:"덧셈",timeout:1,inputTransferType:"one_line",skeletonCode:null,content:"\n  # 덧셈\n  ## 문제\n  두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.\n  ## 입력\n  첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)\n  ## 출력\n  첫째 줄에 A+B를 출력한다.\n          ",userId:null,testCases:["2 4","6 12","10000 21111","-1234 30"],outputs:["6","18","31111","-1204"]},2:{id:"2",title:"작은 별",timeout:1,inputTransferType:"one_line",skeletonCode:null,content:"\n  # 작은 별\n  ## 문제\n  정수 N을 입력받은 다음 다음과 같이 N줄의 별을 출력하는 프로그램을 작성하시오.\n  ## 입력\n  첫째 줄에 N이 주어진다. (0 < N < 10)\n  ## 출력\n  첫째 줄에는 별 1개, 둘째 줄에는 별 2개, ... N번째 줄에는 별 N개를 출력한다.\n          ",userId:null,testCases:["1","2","4","9"],outputs:["*","*\n**","*\n**\n***\n****","*\n**\n***\n****\n*****\n******\n*******\n********\n*********"]}},this._idToSubmissions={}}async getTestCases(e){return this.problems[e].testCases}async validate(e,t){const s=this.problems[e].outputs;if(s.length!==t.length)return{token:null,totalCount:s.length,acceptedCount:0};let n=0;for(let e=0;e<s.length;e++)s[e].trim()===t[e].trim()&&(n+=1);return{token:null,totalCount:s.length,acceptedCount:n}}async getProblem(e){return this.problems[e]}async getSubmissions(e){var t;return null!==(t=this._idToSubmissions[e])&&void 0!==t?t:[]}async submit(e){void 0===this._idToSubmissions[e.problemId]&&(this._idToSubmissions[e.problemId]=[]);const t=Object.assign(Object.assign({},e),{id:this._idToSubmissions[e.problemId].length.toString(),image:"",userId:"",createdAt:(new Date).toISOString()});return this._idToSubmissions[e.problemId].push(t),t}};const xe={id:`${_}:IProblemProviderRegistry`,provides:R,activate:e=>({register:e=>{we=e}}),autoStart:!0};let ve=e=>new f(e);const Se={id:`${_}:IJudgePanelFactoryRegistry`,provides:L,activate:e=>({register:e=>{ve=e}}),autoStart:!0};let je=e=>new pe(e);const Ie={id:`${_}:IJudgeSubmissionAreaFactoryRegistry`,provides:$,activate:e=>({register:e=>{je=e}}),autoStart:!0};let Pe=e=>new ye(e);const Fe={id:`${_}:IJudgeTerminalFactoryRegistry`,provides:D,activate:e=>({register:e=>{Pe=e}}),autoStart:!0};let ke=ne;const Ee={id:`${_}:ISubmissionListFactoryRegistry`,provides:W,activate:e=>({register:e=>{ke=e}}),autoStart:!0},Te={id:`${_}:plugin`,autoStart:!0,requires:[i.ITranslator,a.IEditorServices,d.IRenderMimeRegistry,M.IDocumentManager,N.IFileBrowserFactory,A.IMainMenu,o.ICommandPalette],optional:[J.ISettingRegistry,n.ILayoutRestorer],activate:async(e,t,s,n,i,r,a,l,d,u)=>{const c=t.load(g),m=new o.WidgetTracker({namespace:"judge"}),h=c.__("Judge");let b=null;b=d?(await d.load("@jupyterlab/notebook-extension:tracker")).get("codeCellConfig").composite:{};const _=new x({editorServices:s,rendermime:n,commands:e.commands,editorConfig:b,judgePanelFactory:ve,judgeSubmissionAreaFactory:je,judgeTerminalFactory:Pe,submissionListFactory:ke,submitted:Ce,factoryOptions:{name:h,modelName:"judge-model",fileTypes:["judge"],defaultFor:["judge"],preferKernel:!0,canStartKernel:!0,shutdownOnClose:!0,translator:t}});_.widgetCreated.connect(((e,t)=>{t.context.pathChanged.connect((()=>{m.save(t)})),m.add(t)})),e.docRegistry.addWidgetFactory(_),e.docRegistry.addModelFactory(new E.JudgeModelFactory({problemProviderFactory:()=>we})),e.docRegistry.addFileType({name:"judge",contentType:"file",fileFormat:"text",displayName:c.__("Judge File"),extensions:[".judge"],mimeTypes:["text/json","application/json"]}),function(e,t,s,n,o){e.addCommand(v.open,{execute:async e=>{s.openOrReveal(e.path)},label:t.__("Open Judge")}),e.addCommand(v.openOrCreateFromId,{execute:async e=>{e.problemId&&await T(o,s,e.problemId)},label:t.__("Open or Create Judge From Id")}),e.addCommand(v.execute,{execute:async e=>{n.currentWidget&&n.currentWidget.content.execute()},label:t.__("Execute")})}(e.commands,c,i,m,we),function(e,t,s){!function(e,t){const s={tracker:t,undo:e=>{e.content.editor.undo()},redo:e=>{e.content.editor.redo()}};e.editMenu.undoers.add(s)}(e,t),function(e,t,s){const n={tracker:t,runLabel:e=>s.__("Run Code"),run:async e=>{await e.content.execute()},runAllLabel:e=>s.__("Run All Code"),runAll:async e=>{await e.content.execute()}};e.runMenu.codeRunners.add(n)}(e,t,s)}(a,m,c),l.addItem({command:v.openOrCreateFromId,category:"Judge",args:{problemId:"1"}}),u&&u.restore(m,{command:v.open,args:e=>({path:e.context.path}),name:e=>e.context.path}),e.serviceManager.contents.addDrive(new S.Drive({name:p})),r.createFileBrowser("judgebrowser",{driveName:p})}},Me=[Te,xe,Se,Ie,Fe,Ee,fe]}}]);