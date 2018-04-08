$(document).ready(function () {
  var $navigationMenu = $('#navigation-bar').find('ul.items');
  $('.menu-button').click(function () {
    $navigationMenu.toggle();
  });
});
