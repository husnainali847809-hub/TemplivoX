(function () {
  'use strict';
  var d = document;
  var toggle = d.querySelector('.nav-toggle'), nav = d.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }
  var dd = d.querySelector('.dd');
  if (dd) {
    var btn = dd.querySelector('.dd-btn');
    var close = function () { dd.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); };
    btn.addEventListener('click', function (e) {
      var open = dd.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
      e.stopPropagation();
    });
    d.addEventListener('click', function (e) { if (!dd.contains(e.target)) close(); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  var form = d.getElementById('filter-form');
  if (form) {
    var q = d.getElementById('f-q'), cat = d.getElementById('f-cat'), fmt = d.getElementById('f-fmt');
    var cards = Array.prototype.slice.call(d.querySelectorAll('.card[data-name]'));
    var count = d.getElementById('result-count'), empty = d.getElementById('no-results');
    var params = new URLSearchParams(window.location.search);
    q.value = params.get('q') || '';
    cat.value = params.get('cat') || '';
    fmt.value = params.get('format') || '';
    if (cat.value !== (params.get('cat') || '')) cat.value = '';
    var apply = function () {
      var term = q.value.trim().toLowerCase(), shown = 0;
      cards.forEach(function (c) {
        var ok = (!term || c.getAttribute('data-name').indexOf(term) !== -1) &&
                 (!cat.value || c.getAttribute('data-cat') === cat.value) &&
                 (!fmt.value || c.getAttribute('data-formats').split(' ').indexOf(fmt.value) !== -1);
        c.hidden = !ok;
        if (ok) shown++;
      });
      count.textContent = 'Showing ' + shown + ' of ' + cards.length + ' templates';
      empty.hidden = shown !== 0;
    };
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    ['input', 'change'].forEach(function (ev) { form.addEventListener(ev, apply); });
    apply();
  }

  var cf = d.getElementById('contact-form');
  if (cf) {
    cf.addEventListener('submit', function (e) {
      e.preventDefault();
      var g = function (n) { return cf.elements[n].value; };
      var body = 'Name: ' + g('name') + '\nEmail: ' + g('email') + '\n\n' + g('message');
      window.location.href = 'mailto:' + cf.getAttribute('data-to') + '?subject=' + encodeURIComponent(g('subject')) + '&body=' + encodeURIComponent(body);
    });
  }
})();
