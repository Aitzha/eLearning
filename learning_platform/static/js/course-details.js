document.addEventListener('DOMContentLoaded', function() {
    const courseId = window.location.pathname.split('/')[2];  // Extract course ID from URL
    const enrollBtn = document.getElementById('enroll-btn');
    const modifyBtn = document.getElementById('modify-btn');
    const deleteBtn = document.getElementById('delete-btn');
    const token = localStorage.getItem('token');

    // Fetch and display course details
    fetch(`/api/courses/${courseId}/`, {
        headers: { 'Authorization': token ? 'Token ' + token : '' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.course) {
            // Set course title, description, and teacher
            document.querySelector('.course-title').textContent = data.course.title;
            document.querySelector('.course-description').textContent = data.course.description;
            document.querySelector('.course-teacher').textContent = data.course.teacher.full_name;

            // Handle button state based on user authentication and roles
            if (token) {
                // User is authenticated
                if (data.is_creator) {
                    enrollBtn.textContent = "You are the creator";
                    enrollBtn.disabled = true;  // Disable for course creator
                    modifyBtn.style.display = "inline-block";
                    deleteBtn.style.display = "inline-block";
                } else {
                    // Check if the user is enrolled or not
                    enrollBtn.textContent = data.is_enrolled ? "Withdraw" : "Enroll";
                    enrollBtn.disabled = false;  // Allow enrollment/withdrawal for authenticated users
                }

                if (data.can_view_profile) {
                    // Show 'View Enrolled Students' button for users with necessary permissions
                    document.getElementById('view-students-btn').style.display = "inline-block";
                }
            } else {
                // User is unauthenticated
                enrollBtn.textContent = "Login to Enroll";
                enrollBtn.disabled = true;  // Disable the enroll button for unauthenticated users
            }

            // Handle section dropdown logic (already implemented)
            if (data.is_creator || data.is_enrolled) {
                const sectionsList = document.querySelector('.sections-list');
                sectionsList.style.display = 'block';
                data.sections.forEach(section => {
                    const sectionDiv = document.createElement('div');
                    sectionDiv.classList.add('section');
                    const sectionTitle = document.createElement('button');
                    sectionTitle.classList.add('dropdown-btn');
                    sectionTitle.textContent = section.title;

                    const contentList = document.createElement('div');
                    contentList.classList.add('dropdown-content');
                    section.content_items.forEach(content => {
                        const contentLink = document.createElement('a');
                        contentLink.href = `/content/${content.id}/view`;
                        contentLink.textContent = content.title;
                        contentList.appendChild(contentLink);
                    });

                    sectionDiv.appendChild(sectionTitle);
                    sectionDiv.appendChild(contentList);
                    sectionsList.appendChild(sectionDiv);
                });
            }
        }
    });

    // Handle enrollment/withdrawal
    enrollBtn?.addEventListener('click', function() {
        const action = enrollBtn.textContent.trim() === 'Enroll' ? 'enroll' : 'withdraw';
        fetch(`/api/courses/${courseId}/${action}/`, {
            method: 'POST',
            headers: {
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                enrollBtn.textContent = action === 'enroll' ? 'Withdraw' : 'Enroll';
            } else {
                alert('Action failed: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            alert('Network error: ' + error);
        });
    });

    // Handle course modification
    modifyBtn?.addEventListener('click', function() {
        window.location.href = `/courses/${courseId}/edit/`;
    });

    // Handle course deletion
    deleteBtn?.addEventListener('click', function() {
        if (confirm('Are you sure you want to delete this course?')) {
            fetch(`/api/courses/${courseId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Token ' + token
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/courses/';
                } else {
                    alert('Delete action failed: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(error => {
                alert('Network error: ' + error);
            });
        }
    });
});
