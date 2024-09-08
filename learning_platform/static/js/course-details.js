document.addEventListener('DOMContentLoaded', function() {
    const courseId = window.location.pathname.split('/')[2];
    const enrollBtn = document.getElementById('enroll-btn');
    const modifyBtn = document.getElementById('modify-btn');
    const deleteBtn = document.getElementById('delete-btn');
    const token = localStorage.getItem('token');

    // Handle enrollment/withdrawal
    enrollBtn?.addEventListener('click', function() {
        const action = enrollBtn.textContent.trim() === 'Enroll' ? 'enroll' : 'withdraw';
        fetch(`/api/courses/${courseId}/${action}`, {
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
        window.location.href = `/courses/${courseId}/edit`;
    });

    // Handle course deletion
    deleteBtn?.addEventListener('click', function() {
        if (confirm('Are you sure you want to delete this course?')) {
            fetch(`/api/courses/${courseId}/delete`, {
                method: 'DELETE',
                headers: {
                    'Authorization': 'Token ' + token
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/courses';
                } else {
                    alert('Delete action failed: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(error => {
                alert('Network error: ' + error);
            });
        }
    });

    // Fetch and display course details
    fetch(`/api/courses/${courseId}`, {
        headers: { 'Authorization': token ? 'Token ' + token : '' }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        console.log(data.course)
        console.log(data.course.title)
        if (data.course) {
            document.querySelector('.course-title').textContent = data.course.title;
            document.querySelector('.course-description').textContent = data.course.description;
            document.querySelector('.course-teacher').textContent = data.course.teacher.name;

            // Handle section dropdown
            if (data.sections.length > 0) {
                const sectionsList = document.querySelector('.sections-list');
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
});
