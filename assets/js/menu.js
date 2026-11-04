/* Mobile menu: build a <select> from the main menu (the old site did this with the tinynav plugin). */
(function () {
  var menu = document.querySelector('#main-menu > ul.menu');
  if (!menu) return;
  var select = document.createElement('select');
  select.className = 'tinynav';
  select.setAttribute('aria-label', 'Navigation');
  function add(a, depth) {
    var o = document.createElement('option');
    o.value = a.getAttribute('href');
    o.textContent = (depth ? '– ' : '') + a.textContent;
    if (a.className.indexOf('active') !== -1) o.selected = true;
    select.appendChild(o);
  }
  var top = menu.children;
  for (var i = 0; i < top.length; i++) {
    var a = top[i].querySelector(':scope > a'); if (a) add(a, 0);
    var subs = top[i].querySelectorAll(':scope > ul a');
    for (var j = 0; j < subs.length; j++) add(subs[j], 1);
  }
  select.addEventListener('change', function () { if (this.value) window.location.href = this.value; });
  menu.parentNode.insertBefore(select, menu);
})();
