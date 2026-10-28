(function() {
  const panel = document.getElementById('article-panel');
  if (!panel) return;

  const list = document.createElement('ul');
  list.style.listStyle = 'none';
  list.style.padding = '0';
  list.style.margin = '0';

  articles.forEach(function(article) {
    const li = document.createElement('li');
    li.style.margin = '0.4rem 0';

    const a = document.createElement('a');
    a.href = article.url;
    a.textContent = article.title;
    a.style.textDecoration = 'none';
    a.style.color = '#0366d6';
    a.style.fontSize = '0.9rem';

    li.appendChild(a);
    list.appendChild(li);
  });

  panel.appendChild(list);
})();
