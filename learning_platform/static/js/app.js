document.addEventListener('DOMContentLoaded', function() {
    const userMenu = document.getElementById('user-menu');
    const token = localStorage.getItem('token');

    if (token) {
        fetch('/api/user', {
            headers: { 'Authorization': 'Token ' + token }
        })
        .then(response => response.json())
        .then(user => {
            let dropdownContent = '<a href="/profile">Profile</a>';

            // Check if the user has the 'add_userprofile' permission
            if (user.perms && user.perms.includes('add_userprofile')) {
                dropdownContent += '<a href="/teacher-manager">Teacher Manager</a>';
            }

            dropdownContent += '<a href="#" onclick="logout()" style="color: red;">Logout</a>'

            userMenu.innerHTML = `
                <div class="dropdown">
                    <button class="dropbtn">${user.username}</button>
                    <div class="dropdown-content">
                        ${dropdownContent}
                    </div>
                </div>
            `;
        });
    } else {
        userMenu.innerHTML = '<a href="/login">Sign In/Sign Up</a>';
    }
});

function logout() {
    fetch('/api/logout', {
        method: 'POST',
        headers: {
            'Authorization': 'Token ' + localStorage.getItem('token'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        } else {
            alert('Logout failed. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Logout failed. Please try again.');
    });
}
