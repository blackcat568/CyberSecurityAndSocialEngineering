(function() {
  const panel = document.getElementById('article-panel');
  if (!panel) return;

  const container = document.createElement('div');

  // Получаем имя текущего файла из адресной строки
  const currentPage = window.location.pathname.split('/').pop();

  articlesGroups.forEach(function(group) {
    // Проверяем, есть ли в группе статьи, кроме текущей
    const visibleArticles = group.articles.filter(function(article) {
      // Берём из URL только имя файла (чтобы работало и с абсолютными, и с относительными ссылками)
      const articlePage = article.url.split('/').pop();
      return articlePage !== currentPage;
    });

    // Если в группе не осталось статей — не показываем заголовок группы
    if (visibleArticles.length === 0) return;

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

    visibleArticles.forEach(function(article) {
      const li = document.createElement('li');
      li.style.margin = '0.3rem 0';
      
      // Маркер-кружок
      const marker = document.createElement('span');
      marker.textContent = '• ';
      marker.style.color = '#8b0000';     // красный, как акцент сайта
      marker.style.fontWeight = 'bold';

      const a = document.createElement('a');
      a.href = article.url;
      a.textContent = article.title;
      a.style.textDecoration = 'none';
      a.style.color = '#0366d6';
      a.style.fontSize = '0.85rem';

      li.appendChild(marker);   // ← добавить маркер первым
      li.appendChild(a);        // ← потом ссылку
      ul.appendChild(li);
    });

    container.appendChild(ul);
  });

  panel.appendChild(container);

})();


