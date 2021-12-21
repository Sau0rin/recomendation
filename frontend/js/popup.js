// ожидаем загрузки документа
$(document).ready(() => {
  // после загрузки ищём все элементы с классом .portfolio-item
  // и задаём событие щелчка
  $('.portfolio-item').on('click', (e) => {
    e.stopPropagation();
    createPopup(e.currentTarget);
  });

  // щелчок по кнопке отзывов
  $('.control-item').on('click', (e) => {
    e.stopPropagation();
    slideTestimonials(e.currentTarget);
  });
});

// функция, выполняющаяся по клику на активный элемент
function createPopup(item) {
  console.log(item);
  // передаём HTML в jQuery переменную
  const clicked = $(item);
  // получаем ссылку из атрибута дата
  const src = clicked.data('src');
  // создаём блок-контейнер
  const container = $('<div>', {'class': 'popup-container'});
  // создаём картинку, задаём класс и путь
  const img = $('<img>', {'class':'popup', 'src': src});
  // добавляем картинку в родительский блок
  container.append(img);
  // блок с картинкой РИСУЕМ в HTML-документ
  $('body').append(container);
}


// функция, выполняющаяся по клику на НЕактивный элемент
function slideTestimonials(item) {
  // передаём HTML в jQuery переменную
  const clicked = $(item);
  // проверяем что страница неактивна
  if (clicked.hasClass('active')) {
    // прекращаем работу программы, если уже активна
    return;
  }
  // получаем номер кнопки
  const index = $('.control-item').index(clicked);
  // измеряем ширину карточки вместе с margin - ключ true
  const width = $('.testimonials-card').outerWidth(true);
  // измеряем необходимое для пролистывания расстояние и применяем к блоку-обёртке
  const scroll = width * 2 * index;
  $('.testimonials-inner').css('transform', 'translateX(-'+ scroll +'px)');

  // удаляем у всех кнопок класс active
  $('.control-item').removeClass('active');
  // задаём класс active кнопки с текущим индексом
  $('.control-item').eq(index).addClass('active');
}
