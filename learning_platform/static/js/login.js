document.addEventListener('DOMContentLoaded', function() {
    const successMessage = document.getElementById('success-message');
    const successText = localStorage.getItem('registrationSuccess');
    if (successText) {
        console.log(successText)
        console.log("I was here")
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
        .then(response => {
            if (response.ok) {
                window.location.href = '/';
            } else {
                errorMessage.textContent = data.message || 'Invalid credentials. Please try again.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            errorMessage.textContent = 'Login failed. Please try again.';
        });
    });
});
