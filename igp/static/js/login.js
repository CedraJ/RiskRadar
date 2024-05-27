function validateForm() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    if (username === "" || password === "") {
        alert("Please enter both username and password.");
        return false; 
    }
    return true; 
}

document.addEventListener('DOMContentLoaded', function () {
    // Password visibility toggle setup
    document.querySelectorAll('.toggle-password').forEach(icon => {
        icon.addEventListener('click', function () {
            const input = document.getElementById(this.dataset.input);
            if (input.type === "password") {
                input.type = "text";
                this.classList.replace('fa-eye-slash', 'fa-eye');
            } else {
                input.type = "password";
                this.classList.replace('fa-eye', 'fa-eye-slash');
            }
        });
    });
});
