import{_ as e,j as i,e as t,y as r,n as d}from"./main-e3ebcc13.js";import"./c.2adfe92b.js";import"./c.758520ca.js";import"./c.2610e8cd.js";import"./c.83531278.js";import"./c.bbbd2219.js";import"./c.8e28b461.js";import"./c.728b1e0f.js";import"./c.5addf14f.js";let o=e([d("ha-selector-time")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[t({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[t()],key:"value",value:void 0},{kind:"field",decorators:[t()],key:"label",value:void 0},{kind:"field",decorators:[t()],key:"helper",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[t({type:Boolean})],key:"required",value:()=>!1},{kind:"method",key:"render",value:function(){return r`
      <ha-time-input
        .value=${this.value}
        .locale=${this.hass.locale}
        .disabled=${this.disabled}
        .required=${this.required}
        .helper=${this.helper}
        .label=${this.label}
        enable-second
      ></ha-time-input>
    `}}]}}),i);export{o as HaTimeSelector};
