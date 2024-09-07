document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');  // Get the token from localStorage

    // If no token is found, redirect to the login page
    if (!token) {
        window.location.href = '/login';  // Redirect to login if the user is not authenticated
    }

    // Correctly extract the course ID from the URL (second-to-last part of the path)
    const urlParts = window.location.pathname.split('/');
    const courseId = urlParts[urlParts.length - 2];  // This grabs '1' from '/courses/1/edit/'

    fetch(`/api/courses/${courseId}/`, {
        headers: { 'Authorization': 'Token ' + token }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch course details');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('course-title').textContent = data.title;

        // Check if 'sections' exists before accessing it
        if (data.sections && Array.isArray(data.sections)) {
            const sectionsContainer = document.getElementById('sections-container');
            data.sections.forEach(section => {
                const sectionDiv = document.createElement('div');
                sectionDiv.classList.add('section');
                sectionDiv.innerHTML = `
                    <h3 contenteditable="true">${section.title}</h3>
                    <button class="delete-section-btn" data-section-id="${section.id}">Delete Section</button>
                    <div class="materials-container" data-section-id="${section.id}">
                        <!-- Content items will go here -->
                    </div>
                    <button class="add-content-btn" data-section-id="${section.id}">Add Content</button>
                `;
                sectionsContainer.appendChild(sectionDiv);

                // Load content items if they exist
                if (section.content_items && Array.isArray(section.content_items)) {
                    section.content_items.forEach(contentItem => {
                        const contentDiv = document.createElement('div');
                        contentDiv.classList.add('content-item');
                        contentDiv.innerHTML = `
                            <p>${contentItem.title}</p>
                            ${contentItem.content_type === 'video' ? `<iframe src="${contentItem.video_url}" frameborder="0" allowfullscreen></iframe>` : ''}
                            ${contentItem.content_type === 'pdf' ? `<a href="${contentItem.file}" target="_blank">Download PDF</a>` : ''}
                            <button class="delete-content-btn" data-content-id="${contentItem.id}">Delete Content</button>
                        `;
                        sectionDiv.querySelector('.materials-container').appendChild(contentDiv);
                    });
                }
            });
        } else {
            console.warn('No sections found for this course.');
        }
    })
    .catch(error => {
        console.error('Error fetching course details:', error);
    });

        // Add new section event listener
    const addSectionButton = document.getElementById('add-section-btn');
    addSectionButton.addEventListener('click', function() {
        const newSectionTitle = prompt('Enter the new section title:');  // Prompt the user for a section title
        if (newSectionTitle) {
            // Make a POST request to the API to add a new section
            fetch(`/api/courses/${courseId}/sections`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + token
                },
                body: JSON.stringify({ title: newSectionTitle, order: 0 })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to add section');
                }
                return response.json();
            })
            .then(data => {
                // Reload the page after successfully adding the section
                location.reload();  // Refresh the page to show the new section
            })
            .catch(error => {
                console.error('Error adding section:', error);
            });
        }
    });
});
