$(document).ready(function() {
  $('button[type="submit"]').click(function(evt) {
    var action = $(this).attr('formaction');
    var form = $(this).parent();
    var subj = $(form).children('input[name="subject"]').val(),
      body = $(form).children('textarea[name="body"]').val(),
      recipient = $(form).children('input[name="recipient"]').val(),
      csrf = $(form).children('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
      context: this,
      url: action,
      method: 'post',
      data: {
        subject: subj,
        body: body,
        recipient: recipient,
        csrfmiddlewaretoken: csrf
      },
      success: function(data) {
        console.log(data);
          
        $(this).parent().parent().remove();
      },
      error: function(err) {
        alert(err);
      },
      dataType: 'json'
    });

    evt.preventDefault();
  })
});
