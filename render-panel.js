(function() {
  const panel = document.getElementById('article-panel');
  if (!panel) return;

  const container = document.createElement('div');

  articlesGroups.forEach(function(group) {
    const h4 = document.createElement('h4');
    h4.textContent = group.group;
    h4.style.margin = '1rem 0 0.5rem 0';
    h4.style.fontSize = '1rem';
    h4.style.color = '#333';
    container.appendChild(h4);

    const ul = document.createElement('ul');
    ul.style.listStyle = 'none';
    ul.style.padding = '0';
    ul.style.margin = '0 0 0.5rem 0';

    group.articles.forEach(function(article) {
      const li = document.createElement('li');
      li.style.margin = '0.3rem 0';

      const a = document.createElement('a');
      a.href = article.url;
      a.textContent = article.title;
      a.style.textDecoration = 'none';
      a.style.color = '#0366d6';
      a.style.fontSize = '0.85rem';

      li.appendChild(a);
      ul.appendChild(li);
    });

    container.appendChild(ul);
  });

  panel.appendChild(container);
})();
