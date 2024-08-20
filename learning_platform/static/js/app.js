// Handle header
document.addEventListener('DOMContentLoaded', function() {
    const userMenu = document.querySelector('.user-menu');
    const isLoggedIn = userMenu.getAttribute('data-logged-in') === 'true';
    const username = userMenu.getAttribute('data-username');

    if (isLoggedIn) {
        userMenu.innerHTML = `
            <div class="dropdown">
                <button class="dropbtn">${username}</button>
                <div class="dropdown-content">
                    <a href="/profile">Profile</a>
                    <a href="/logout" style="color: red;">Logout</a>
                </div>
            </div>
        `;
    } else {
        userMenu.innerHTML = '<a href="/login">Login/Sign In</a>';
    }
});


// // Handle Login
// document.getElementById('login-form').addEventListener('submit', function(event) {
//     event.preventDefault();
//     const username = document.getElementById('username').value;
//     const password = document.getElementById('password').value;
//
//     fetch('/api/login/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ username, password })
//     }).then(response => response.json())
//       .then(data => {
//           if (data.token) {
//               localStorage.setItem('token', data.token);
//               window.location.href = '/'; // Redirect to home on success
//           } else {
//               alert('Login failed!');
//           }
//       });
// });
