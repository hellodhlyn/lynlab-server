$(document).ready(function () {
  $('.toast > .btn.btn-clear').click(function () {
    $(this).parent().remove();
  });
});