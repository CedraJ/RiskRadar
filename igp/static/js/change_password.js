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

    // Password criteria validation setup
    const passwordInput = document.getElementById('new-password');
    const tooltip = document.getElementById('password-tooltip');
    const criteria = {
        length: document.getElementById('criteria-length'),
        lowercase: document.getElementById('criteria-lowercase'),
        uppercase: document.getElementById('criteria-uppercase'),
        numbers: document.getElementById('criteria-numbers'),
        special: document.getElementById('criteria-special'),
        consecutive: document.getElementById('criteria-consecutive')
    };

    passwordInput.addEventListener('input', function () {
        const value = this.value;
        criteria.length.className = value.length >= 12 ? 'valid' : 'invalid';
        criteria.lowercase.className = /[a-z]/.test(value) ? 'valid' : 'invalid';
        criteria.uppercase.className = /[A-Z]/.test(value) ? 'valid' : 'invalid';
        criteria.numbers.className = /\d/.test(value) ? 'valid' : 'invalid';
        criteria.special.className = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/.test(value) ? 'valid' : 'invalid';
        criteria.consecutive.className = !/(.)\1{2,}/.test(value) ? 'valid' : 'invalid';
    });

    passwordInput.addEventListener('focus', function () {
        tooltip.style.display = 'block'; 
    });

    passwordInput.addEventListener('blur', function () {
        tooltip.style.display = 'none'; 
    });
});
