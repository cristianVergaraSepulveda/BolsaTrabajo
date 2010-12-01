var ev

$(function() {
    $('.reply_comment_link').click(function(event) {
        event.preventDefault()
        id = $(this).parent().attr('id')
        
        $('.reply_comment_link').show()
        $('#js_form').appendTo($(this).parent()).show()
        $('#parent_id').val(id)
        
        $(this).hide()

    })
})
