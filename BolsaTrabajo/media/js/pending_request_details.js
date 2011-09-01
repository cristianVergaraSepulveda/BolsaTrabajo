$(function() {
    $('#reject_link').click(function(event) {
        event.preventDefault()
        
        var answer = confirm('¿Está seguro que quiere borrar esta solicitud? Este proceso no se puede revertir')
        if (answer)
            window.location = 'reject'
    })
})
