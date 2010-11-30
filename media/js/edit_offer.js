$(function() {
    $('#reject_link').click(function(event) {
        event.preventDefault()
        
        var answer = confirm('¿Está seguro que quiere cerrar esta oferta? Este proceso no se puede revertir')
        if (answer)
            window.location = 'close'
    })
})
