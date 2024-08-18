// app.js
function apiRequest(url, method, data) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': localStorage.getItem('token') ? `Token ${localStorage.getItem('token')}` : ''
        },
        body: data ? JSON.stringify(data) : null
    }).then(response => response.json());
}

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    apiRequest('/api/login/', 'POST', { username, password })
        .then(data => {
            localStorage.setItem('token', data.token);
            document.getElementById('login-form').style.display = 'none';
            loadProfile();
        });
}

function register() {
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;
    const email = document.getElementById('reg-email').value;
    apiRequest('/api/register/', 'POST', { username, password, email })
        .then(data => {
            alert('Registration Successful!');
        });
}

function loadProfile() {
    apiRequest('/api/profile/', 'GET')
        .then(data => {
            document.getElementById('profile').style.display = 'block';
            document.getElementById('profile-info').innerText = `Hello, ${data.username}`;
        });
}

function logout() {
    apiRequest('/api/logout/', 'POST')
        .then(data => {
            localStorage.removeItem('token');
            document.getElementById('profile').style.display = 'none';
            document.getElementById('login-form').style.display = 'block';
        });
}
