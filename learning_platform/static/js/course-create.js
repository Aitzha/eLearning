document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('course-create-form');
    const errorMessage = document.getElementById('error-message');
    const token = localStorage.getItem('token');  // Get the token from local storage

    // If no token is found, redirect the user to the login page
    if (!token) {
        window.location.href = '/login';  // Redirect to the login page if not authenticated
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from submitting the default way

        // Collect the form data
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;

        // Send the data to the API using a POST request
        fetch('/api/courses/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token  // Include the token in the request headers
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        })
        .then(response => {
            if (response.ok) {
                // Course creation successful, redirect or show success message
                window.location.href = '/courses/';
            } else {
                return response.json();  // Get the error message if the response isn't OK
            }
        })
        .then(data => {
            if (data && data.error) {
                // Display the error message
                errorMessage.textContent = data.error || 'An error occurred. Please try again.';
            }
        })
        .catch(error => {
            errorMessage.textContent = 'An unexpected error occurred. Please try again.';
        });
    });
});
