$(document).ready(function () {
  var today = new Date();
  var date =
    today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
  document.querySelector("#date").innerHTML += date;

  if($('.urgently-slider').length){
    $('.urgently-slider').slick({
      dots: false,
      arrows: true,
      slidesToScroll: 1,
      autoplay: true,
      cssEase: "linear",
    })
  }

  if ($(".books-slider").length) {
    $(".books-slider").slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      autoplay: true,
      Infinit: true,
      cssEase: "linear",
      arrows: false,
      responsive: [
        {
          breakpoint: 800,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
          },
        },
        {
          breakpoint: 524,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
          },
        },
      ],
    });
  }

  $(".marqueed").simplemarquee({
    direction: "right",
    speed: 60,
    cycles: 5,
    delayBetweenCycles: 2500,
    handleResize: true,
    space: 0,
  });

  $('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
    if (!$(this).next().hasClass('show')) {
      $(this).parents('.dropdown-menu').first().find('.show').removeClass('show');
    }
    var $subMenu = $(this).next('.dropdown-menu');
    $subMenu.toggleClass('show');
  
  
    $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
      $('.dropdown-submenu .show').removeClass('show');
    });
  
  
    return false;
  });

});

function httpAjax(url, mFunction) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      mFunction(JSON.parse(this.responseText));
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}
function changeCountry() {
  var c_value = document.getElementById("cid").value;
  httpAjax(
    "//timesprayer.com/ajax.php?do=loadCities&language=ar&cid=" + c_value,
    function (result) {
      if (result.status == 1) {
        document.getElementById("ciid").innerHTML = result.msg;
      }
    }
  );
}
function changecity() {
  var ci_value = document.getElementById("ciid").value;
  var thisurl = window.location.href;
  var newUrl = thisurl.replace("name=assiut", "name=" + ci_value);
  window.location.href = newUrl;
}
var city_offset = "2";
var reminingtime = 17066000;
var soundfile = "fajer";
var douration_sound = "280";
var clean_url = "timesprayer.com";

(function (i, s, o, g, r, a, m) {
  i.GoogleAnalyticsObject = r;
  (i[r] =
    i[r] ||
    function () {
      (i[r].q = i[r].q || []).push(arguments);
    }),
    (i[r].l = 1 * new Date());
  (a = s.createElement(o)), (m = s.getElementsByTagName(o)[0]);
  a.async = 1;
  a.src = g;
  m.parentNode.insertBefore(a, m);
})(window, document, "script", "//www.google-analytics.com/analytics.js", "ga");
ga("create", "UA-51636779-1", "timesprayer.com");
ga("send", "pageview");
