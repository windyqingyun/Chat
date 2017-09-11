$('.chat-user').click(function () {
    alert('sss')
    this.addClass('active')
    $('.chat-user').not(this).removeClass('active')
});
