// Remember the language a visitor picks.
document.querySelectorAll('.langs a[data-lang]').forEach(function (a) {
  a.addEventListener('click', function () {
    try { localStorage.setItem('sm365-lang', a.dataset.lang); } catch (e) {}
  });
});

// Real reviews only: rendered from data/reviews.json; the section stays hidden while the file is empty.
(function () {
  var list = document.querySelector('.reviews__list');
  if (!list || !window.fetch) return;
  fetch(list.dataset.src, { cache: 'no-cache' })
    .then(function (r) { return r.ok ? r.json() : []; })
    .then(function (items) {
      if (!Array.isArray(items) || !items.length) return;
      items.forEach(function (it) {
        if (!it || !it.text || !it.source) return;
        var li = document.createElement('li');
        var q = document.createElement('blockquote');
        q.textContent = it.text;
        var who = document.createElement('p');
        who.className = 'who';
        who.textContent = [it.author, it.date].filter(Boolean).join(', ') + ' ';
        var a = document.createElement('a');
        a.href = it.source; a.target = '_blank'; a.rel = 'noopener';
        a.textContent = list.dataset.sourceLabel;
        who.appendChild(a);
        li.appendChild(q); li.appendChild(who);
        list.appendChild(li);
      });
      if (list.children.length) document.getElementById('reviews').hidden = false;
    })
    .catch(function () {});
})();
