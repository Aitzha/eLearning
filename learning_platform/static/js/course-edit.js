document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    const courseId = window.location.pathname.split('/')[2];  // Assuming URL is /courses/<course_id>/edit/

    fetch(`/api/courses/${courseId}`, {
        headers: { 'Authorization': 'Token ' + token }
    })
    .then(response => response.json())
    .then(data => {
        const sectionsContainer = document.getElementById('sections-container');
        data.sections.forEach((section) => {
            const sectionDiv = document.createElement('div');
            sectionDiv.classList.add('section-item');

            // Create clickable section title
            sectionDiv.innerHTML = `
                <a href="/sections/${section.id}/edit" class="section-link">${section.title}</a>
                <div>
                    <button class="modify-section-btn" data-section-id="${section.id}">Modify</button>
                    <button class="delete-section-btn" data-section-id="${section.id}">Delete</button>
                </div>
            `;
            sectionsContainer.appendChild(sectionDiv);

            // Modify section listener
            sectionDiv.querySelector('.modify-section-btn').addEventListener('click', function() {
                const newTitle = prompt('Enter new section title:', section.title);
                if (newTitle) {
                    modifySection(section.id, newTitle);
                }
            });

            // Delete section listener
            sectionDiv.querySelector('.delete-section-btn').addEventListener('click', function() {
                if (confirm('Are you sure you want to delete this section?')) {
                    deleteSection(section.id);
                }
            });
        });
    });

    // Function to modify a section
    function modifySection(sectionId, newTitle) {
        fetch(`/api/sections/${sectionId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token
            },
            body: JSON.stringify({ title: newTitle })
        })
        .then(() => location.reload());  // Reload the page after modifying the section
    }

    // Function to delete a section
    function deleteSection(sectionId) {
        fetch(`/api/sections/${sectionId}/`, {
            method: 'DELETE',
            headers: { 'Authorization': 'Token ' + token }
        })
        .then(() => location.reload());  // Reload the page after deleting the section
    }

    // Add new section event listener
    document.getElementById('add-section-btn').addEventListener('click', function() {
        const newSectionTitle = prompt('Enter the new section title:');
        if (newSectionTitle) {
            fetch(`/api/courses/${courseId}/sections`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + token
                },
                body: JSON.stringify({ title: newSectionTitle })
            })
            .then(() => location.reload());  // Refresh the page to show the new section
        }
    });
});
