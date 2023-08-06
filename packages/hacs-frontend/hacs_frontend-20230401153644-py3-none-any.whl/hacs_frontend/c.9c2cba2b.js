import{_ as e,j as a,e as t,y as i,O as d,n as l}from"./main-e3ebcc13.js";import"./c.4787926e.js";import"./c.83531278.js";import"./c.5fe2e3ab.js";import"./c.f8856f91.js";import"./c.bbbd2219.js";import"./c.8e28b461.js";import"./c.728b1e0f.js";import"./c.5addf14f.js";let r=e([l("ha-selector-object")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[t()],key:"hass",value:void 0},{kind:"field",decorators:[t()],key:"value",value:void 0},{kind:"field",decorators:[t()],key:"label",value:void 0},{kind:"field",decorators:[t()],key:"helper",value:void 0},{kind:"field",decorators:[t()],key:"placeholder",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[t({type:Boolean})],key:"required",value:()=>!0},{kind:"method",key:"render",value:function(){return i`<ha-yaml-editor
        .hass=${this.hass}
        .readonly=${this.disabled}
        .label=${this.label}
        .required=${this.required}
        .placeholder=${this.placeholder}
        .defaultValue=${this.value}
        @value-changed=${this._handleChange}
      ></ha-yaml-editor>
      ${this.helper?i`<ha-input-helper-text>${this.helper}</ha-input-helper-text>`:""} `}},{kind:"method",key:"_handleChange",value:function(e){const a=e.target.value;e.target.isValid&&this.value!==a&&d(this,"value-changed",{value:a})}}]}}),a);export{r as HaObjectSelector};
