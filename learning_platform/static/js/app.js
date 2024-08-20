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
                    <a href="#" onclick="logout()" style="color: red;">Logout</a>
                </div>
            </div>
        `;
    } else {
        userMenu.innerHTML = '<a href="/login">Login/Sign In</a>';
    }
});

function logout() {
    console.log('Logout logic here');
    // Add logout functionality
}
