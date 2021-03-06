window.onload = function() {
  $('.submit.btn').on('click', (e) => call(e));
  const menuList = document.querySelectorAll('.menu-element');
  menuList.forEach(function(element) {
    element.addEventListener('click', (event) => {
      event.preventDefault();
      const elementLink = element.dataset.link;
      document.getElementById(elementLink).scrollIntoView({ behavior: 'smooth'});
    });
  });
}

function call (e) {
  e.preventDefault();
  id_tovara=document.getElementById("id_tovara").value;
  
  const msg = $('#exampleForm').serialize();
  $.ajax({
    // Метод передачи
    type: 'POST',
     // Файл которому передаем запрос и получаем ответ
    url: 'http://localhost:8000/request',
     // Кеширование
    cache: false,
     // Верямя ожидания ответа, в мили секундах 1000 мс = 1 сек
    timeout:3000,
    data: msg,
    // Функция сработает при успешном получении данных
    success: (data) => {
      // Отображаем данные в форме
      $('#status').html('');
      console.log(data);
      showResult(data);
    },
    // Функция срабатывает в период ожидания данных
    beforeSend: (data) => {
      $('#status').html('<p>Ожидание данных...</p>');
    },
     // Тип данных
    dataType:"html",
     // Функция сработает в случае ошибки
    error: (data) => {
      $('#status').html('<p>Возникла неизвестная ошибка. Пожалуйста, попробуйте чуть позже...</p>');
    }
  });
}


function showResult(data) {
	const dataJSON = JSON.parse(data);
 
  $('.main-title-description').html('Найдено совпадений: '+dataJSON.similar_link.length)
  $('#selected_product').html('Выбраный товар '+'<a href = '+dataJSON.first+'  target="_blank"><img src='+dataJSON.img_ferst+'></a>')

  for (var f in dataJSON.similar_link)
  {
    document.getElementById("similar_product").innerHTML+= '<a href = '+dataJSON.similar_link[f]+'  target="_blank"><img src='+dataJSON.image[f]+'></a>'
  }


    
}
