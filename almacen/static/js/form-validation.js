document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("loginForm"); // Asegúrate de que tu formulario tenga este ID
    form.addEventListener("submit", function(event) {
        let valid = true;

        // Validar nombre de usuario
        const username = document.getElementById("id_username").value;
        if (username.trim() === "") {
            valid = false;
            alert("El nombre de usuario es obligatorio.");
        }

        // Validar contraseña
        const password = document.getElementById("id_password").value;
        if (password.trim() === "") {
            valid = false;
            alert("La contraseña es obligatoria.");
        }

        if (!valid) {
            event.preventDefault(); // Evitar el envío del formulario si hay errores
        }
    });
});