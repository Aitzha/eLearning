document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    if (token) {
        fetch('/api/profile', {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('username').textContent = data.username;
            document.getElementById('full-name').textContent = 'Name: ' + data.first_name + ' ' + data.last_name;
            document.getElementById('email').textContent = 'Email: ' + data.email;

        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
