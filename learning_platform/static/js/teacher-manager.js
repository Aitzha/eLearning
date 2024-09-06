document.addEventListener('DOMContentLoaded', function() {
    let currentPage = 1;
    const teacherContainer = document.getElementById('teacher-container');
    const addTeacherButton = document.getElementById('add-teacher-btn');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');
    const token = localStorage.getItem('token');
    const credentialBox = document.getElementById('credential-box');

    function loadTeachers(page = 1) {
        fetch(`/api/users?role=Teacher&page=${page}`)
            .then(response => response.json())
            .then(data => {
                teacherContainer.innerHTML = '';
                data.results.forEach(teacher => {
                    const teacherDiv = document.createElement('div');
                    teacherDiv.className = 'teacher';
                    teacherDiv.innerHTML = `<h3>${teacher.username}</h3>`;
                    teacherContainer.appendChild(teacherDiv);
                });

                // Handle pagination
                prevButton.disabled = !data.previous;
                nextButton.disabled = !data.next;

                // Update current page info
                pageInfo.textContent = `Page ${currentPage} of ${Math.ceil(data.count / PAGE_SIZE)}`;
            })
            .catch(error => console.error('Error fetching teachers:', error));
    }

    // Call the function to load teachers on page load
    loadTeachers(currentPage);

    // Event listener for adding a new teacher
    addTeacherButton.addEventListener('click', function() {
        fetch('/api/add-teacher', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            },
        })
        .then(response => {
            // Check if the response is OK and pass the data to the next .then() call
            if (!response.ok) {
                throw new Error('Failed to create teacher');
            }
            return response.json();
        })
        .then(data => {
            // Display the credentials at the top of the page in the credential box
            credentialBox.innerHTML = `
                <div class="credential-box">
                    <p><strong>New Teacher Created!</strong></p>
                    <p>Username: ${data.username}</p>
                    <p>Password: ${data.password}</p>
                </div>
            `;

            // Reload the teacher list to include the new teacher
            loadTeachers(currentPage);
        })
        .catch(error => console.error('Error creating teacher:', error));
    });

    // Pagination event listeners
    prevButton.addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            loadTeachers(currentPage);
        }
    });

    nextButton.addEventListener('click', function() {
        currentPage++;
        loadTeachers(currentPage);
    });
});
