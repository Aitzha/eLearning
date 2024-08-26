document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const form = event.target;
    const errorMessage = document.getElementById('error-message');

    const data = {
        username: form.username.value,
        email: form.email.value,
        password: form.password.value,
        password2: form.password2.value
    };

    if (data.password !== data.password2) {
        errorMessage.textContent = 'Passwords do not match!';
        return;
    }

    fetch(form.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/login';
        } else {
            errorMessage.textContent = 'Username is already taken';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        errorMessage.textContent = 'Error registering account.';
    });
});