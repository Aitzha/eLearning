document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    const coursesList = document.getElementById('courses-list');

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


        // Fetch the user enrollments
        fetch('/api/user-enrollments', {
            headers: {
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                coursesList.innerHTML = '';  // Clear any placeholder text

                // Loop through the courses and add them to the list
                data.forEach(course => {
                    const courseItem = document.createElement('li');
                    courseItem.textContent = course.title;
                    coursesList.appendChild(courseItem);
                });
            } else {
                coursesList.innerHTML = '<li>No courses enrolled yet.</li>';
            }
        })
        .catch(error => {
            coursesList.innerHTML = '<li>Error fetching enrolled courses.</li>';
            console.error('Error fetching enrolled courses:', error);
        });
    }
});
