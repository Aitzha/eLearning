document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    const sectionId = window.location.pathname.split('/')[2];  // Assuming URL is /sections/<section_id>/content/

    fetch(`/api/sections/${sectionId}/content-items`, {
        headers: { 'Authorization': 'Token ' + token }
    })
    .then(response => response.json())
    .then(data => {
        const contentContainer = document.getElementById('content-items-container');
        data.content_items.forEach(contentItem => {
            const contentDiv = document.createElement('div');
            contentDiv.classList.add('content-item');
            contentDiv.innerHTML = `
                <p>${contentItem.title}</p>
                ${contentItem.content_type === 'video' ? `<iframe src="${contentItem.video_url}" frameborder="0" allowfullscreen></iframe>` : ''}
                ${contentItem.content_type === 'pdf' ? `<a href="${contentItem.file}" target="_blank">Download PDF</a>` : ''}
                <button class="modify-content-btn" data-content-id="${contentItem.id}">Modify</button>
                <button class="delete-content-btn" data-content-id="${contentItem.id}">Delete</button>
            `;
            contentContainer.appendChild(contentDiv);

            // Modify content listener
            contentDiv.querySelector('.modify-content-btn').addEventListener('click', function() {
                window.location.href = `/content/${contentItem.id}/edit/`;  // Redirect to modify content page
            });

            // Delete content listener
            contentDiv.querySelector('.delete-content-btn').addEventListener('click', function() {
                if (confirm('Are you sure you want to delete this content?')) {
                    fetch(`/api/content-items/${contentItem.id}/`, {
                        method: 'DELETE',
                        headers: { 'Authorization': 'Token ' + token }
                    })
                    .then(() => location.reload());  // Reload the page after deletion
                }
            });
        });
    });

    // Add new content event listener
    document.getElementById('add-content-btn').addEventListener('click', function() {
        window.location.href = `/sections/${sectionId}/content/new/`;  // Redirect to add new content page
    });
});
