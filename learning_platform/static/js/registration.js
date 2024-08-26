document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const form = event.target;

    const data = {
        username: form.username.value,
        email: form.email.value,
        password: form.password.value,
        password2: form.password2.value
    };

    if (data.password !== data.password2) {
        alert('Passwords do not match!');
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
            alert(data.message || 'Registration failed, please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error registering account.');
    });
});