// Handle header
document.addEventListener('DOMContentLoaded', function() {
    const userMenu = document.getElementById('user-menu');
    const token = localStorage.getItem('token');

    if (token) {
        fetch('/api/user/', {
            headers: {
                'Authorization': `Token ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            userMenu.innerHTML = `<div>Welcome, ${data.username}! <a href="#" onclick="logout()">Logout</a></div>`;
        })
        .catch(error => console.error('Error fetching user data:', error));
    } else {
        userMenu.innerHTML = '<a href="/login">Login/Sign In</a>';
    }
});

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
}


// Handle Login
document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token);
            window.location.href = '/';
        } else {
            alert('Login failed. Please check your credentials and try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Login failed. Please try again.');
    });
});
