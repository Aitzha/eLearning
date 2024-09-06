document.addEventListener('DOMContentLoaded', function() {
    const successMessage = document.getElementById('success-message');
    const successText = localStorage.getItem('registrationSuccess');
    if (successText) {
        successMessage.textContent = successText;
        localStorage.removeItem('registrationSuccess');
    }

    document.getElementById('login-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const form = event.target;
        const errorMessage = document.getElementById('error-message');

        const data = {
            username: form.username.value,
            password: form.password.value
        };

        fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                localStorage.setItem('token', data.token);
                window.location.href = '/';
            } else {
                errorMessage.textContent = 'Invalid credentials. Please try again.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = 'Login failed. Please try again.';
        });
    });
});
