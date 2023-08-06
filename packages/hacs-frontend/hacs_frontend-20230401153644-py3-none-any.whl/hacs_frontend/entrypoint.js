
try {
  new Function("import('/hacsfiles/frontend/main-e3ebcc13.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-e3ebcc13.js';
  el.type = 'module';
  document.body.appendChild(el);
}
  