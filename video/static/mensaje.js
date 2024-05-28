// script.js

$(document).ready(function(){
    $('#registration-form').submit(function(e){
        e.preventDefault(); // Evitar el envío del formulario normal

        // Realizar una solicitud AJAX al servidor
        $.ajax({
            type: 'POST',
            url: '/submit',
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData: false,
            success: function(data){
                // Mostrar el modal de éxito
                $('#success-modal').modal('show');
            },
            error: function(xhr, status, error){
                // Mostrar el modal de error
                $('#error-modal').modal('show');
            }
        });
    });
});
