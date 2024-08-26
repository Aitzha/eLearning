document.addEventListener('DOMContentLoaded', function() {
    const userMenu = document.getElementById('user-menu');
    const token = localStorage.getItem('token');

    if (token) {
        fetch('/api/user/', {
            headers: { 'Authorization': 'Token ' + token }
        })
        .then(response => response.json())
        .then(user => {
            userMenu.innerHTML = `
                <div class="dropdown">
                    <button class="dropbtn">${user.username}</button>
                    <div class="dropdown-content">
                        <a href="/profile">Profile</a>
                        <a href="#" onclick="logout()" style="color: red;">Logout</a>
                    </div>
                </div>`;
        });
    } else {
        userMenu.innerHTML = '<a href="/login">Sign In/Sign Up</a>';
    }
});

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
}
