document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');  // Get the token from localStorage
    const courseId = window.location.pathname.split('/').pop();  // Assuming the URL is /courses/<course_id>/

    // Fetch the course details
    fetch(`/api/courses/${courseId}/`, {
        headers: token ? { 'Authorization': 'Token ' + token } : {}
    })
    .then(response => response.json())
    .then(data => {
        // Set the course title and description
        document.getElementById('course-title').textContent = data.title;
        document.getElementById('course-description').textContent = data.description;
        document.getElementById('teacher-name').textContent = data.teacher;

        // Check if the user is enrolled or the course creator
        if (data.user_is_enrolled || data.user_is_creator) {
            // Create the sections and materials
            const sectionsContainer = document.getElementById('sections-container');
            data.sections.forEach(section => {
                const sectionDiv = document.createElement('div');
                sectionDiv.classList.add('section');

                // Section title (collapsible)
                const sectionTitle = document.createElement('button');
                sectionTitle.textContent = section.title;
                sectionTitle.classList.add('collapsible');
                sectionDiv.appendChild(sectionTitle);

                // Materials in section (collapsed by default)
                const materialList = document.createElement('div');
                materialList.classList.add('content');
                section.materials.forEach(material => {
                    const materialDiv = document.createElement('div');
                    if (material.type === 'text') {
                        materialDiv.textContent = material.content;
                    } else if (material.type === 'video') {
                        materialDiv.innerHTML = `<iframe src="${material.content}" frameborder="0" allowfullscreen></iframe>`;
                    }
                    materialList.appendChild(materialDiv);
                });
                sectionDiv.appendChild(materialList);
                sectionsContainer.appendChild(sectionDiv);
            });
        } else {
            document.getElementById('sections-container').textContent = 'You must be enrolled to view the course content.';
        }

        // Handle Enroll/Withdraw button
        const enrollWithdrawButton = document.getElementById('enroll-withdraw-button');
        if (token && !data.user_is_creator) {
            if (data.user_is_enrolled) {
                enrollWithdrawButton.innerHTML = '<button id="withdraw-button">Withdraw from Course</button>';
                document.getElementById('withdraw-button').addEventListener('click', withdrawFromCourse);
            } else {
                enrollWithdrawButton.innerHTML = '<button id="enroll-button">Enroll in Course</button>';
                document.getElementById('enroll-button').addEventListener('click', enrollInCourse);
            }
        }
    })
    .catch(error => console.error('Error fetching course details:', error));

    // Enrollment and withdrawal functions
    function enrollInCourse() {
        fetch(`/api/courses/${courseId}/enroll/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            }
        })
        .then(() => location.reload())
        .catch(error => console.error('Error enrolling in course:', error));
    }

    function withdrawFromCourse() {
        fetch(`/api/courses/${courseId}/withdraw/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            }
        })
        .then(() => location.reload())
        .catch(error => console.error('Error withdrawing from course:', error));
    }
});
