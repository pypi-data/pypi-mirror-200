import { DOMWidgetModel, DOMWidgetView } from '@jupyter-widgets/base';
import { PageConfig } from '@jupyterlab/coreutils';

export class ESASkyJSModel extends DOMWidgetModel {
  initialize(
    attributes: any,
    options: { model_id: string; comm?: any; widget_manager: any }
  ): void {
    super.initialize(attributes, options);
  }
  defaults(): Backbone.ObjectHash {
    return {
      ...super.defaults(),
      _model_name: "ESASkyJSModel",
      _view_name: "ESASkyJSView",
      _model_module: "pyesasky",
      _view_module: "pyesasky",
      view_module_ids: [],
    };
  }
}

export class ESASkyJSView extends DOMWidgetView {
  base_url: string;
  modelId: string;
  oldMsgId: string;
  oldMsgIdToFront: string;
  readonly apiAddr: string = "https://sky.esa.int"
  //readonly apiAddr: string = "http://localhost:8080/esasky"

  render(): void {
    let self = this;
    var div = document.createElement("div");
    this.base_url = PageConfig.getBaseUrl();
    this.base_url = PageConfig.getBaseUrl();
    this.modelId = "esaskyFrame" + Math.random().toString(36).substr(2,10);
    var moduleIds = this.model.get('_view_module_ids')
    moduleIds.push(this.modelId)
    this.model.set('_view_module_ids', moduleIds)
    var lang = this.model.get('_view_language');
    console.log(lang);

    var iframe = document.createElement("iframe");
    iframe.setAttribute("id", this.modelId.toString());
    iframe.setAttribute("width", "100%");
    iframe.setAttribute("height", "800px");
    iframe.setAttribute("style", "border: none");
    iframe.setAttribute("src", this.apiAddr + "?hide_welcome=true&hide_sci_switch=true&sci=true&hide_banner_info=true");
    iframe.onload = function() {
      // Send init message so that esasky know of the pyesasky client and may initiate communication
      iframe.contentWindow.postMessage({'event': 'initTest', 'origin': 'pyesasky'}, self.apiAddr)
      console.log("Init message sent")
    }

    div.appendChild(iframe);
  
    this.el.appendChild(div);
    let el = this.el;
    const observer = new MutationObserver(() => {
      el.style.height = 'auto';
    });
    observer.observe(el, { attributes: true, childList: true });

    this.model.on('msg:custom' , this.handle_custom_message, this);
    this.listenTo(this.model, 'change:view_height', this.height_changed);

    this.oldMsgId = null
    this.oldMsgIdToFront = null
    var _this = this;

    window.addEventListener("message",function(e){
      var data = e.data;
      console.log("Back inside pyesasky.js");
      if(_this.oldMsgId != data.msgId){
        _this.oldMsgId = data.msgId
        _this.model.send(data,null,null);
      }
    });
    
  }

  height_changed(): void {
    console.log("Changing view height")
    var height = this.model.get('view_height');
    let modelIds = this.model.get('_view_module_ids')
    for (var i = modelIds.length-1; i >= 0; i--) {
      let currActiveId = modelIds[i]; 
      if(document.getElementById(currActiveId) != null){
        let el = document.getElementById(currActiveId);
        el.style.height = height;
        break;  
      }
    }
  }

  handle_custom_message(msg: any): void {
    let modelIds = this.model.get('_view_module_ids')
    let currActiveId : string;
    for (var i = modelIds.length - 1; i >= 0; i--) {
      currActiveId = modelIds[i]; 
      if(document.getElementById(currActiveId) != null){
        break;
      }
    }
    if(this.oldMsgIdToFront != msg.msgId){
      if(this.modelId == currActiveId){
        this.oldMsgIdToFront = msg.msgId;
        console.log('Inside pyesasky.js');
        let iFrameElement = document.getElementById(this.modelId) as HTMLIFrameElement
        iFrameElement.contentWindow.postMessage(msg, this.apiAddr)
      }
    }
  }
}
