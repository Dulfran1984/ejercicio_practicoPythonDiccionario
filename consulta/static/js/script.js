document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("documento").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            obtenerUsuario();
        }
    });

    function obtenerUsuario() {
        var documento = document.getElementById("documento").value;

        fetch('/obtener_usuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ documento: documento })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById("nombre").value = data.nombre;
                document.getElementById("apellido").value = data.apellido;
                document.getElementById("email").value = data.email;
                // Actualizar la imagen si existe la URL de la foto en los datos
                if (data.foto) {
                    document.getElementById("foto").src = data.foto;
                } else {
                    document.getElementById("foto").src = ""; // Imagen por defecto o vacío
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
