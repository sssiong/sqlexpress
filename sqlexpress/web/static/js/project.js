// Pills highlighting
$(window).on('load', function onLoad() {
  $(`a[href*="${this.location.pathname}"]`).addClass('active');
  $('.never_active').removeClass('active');
});