document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    const sectionId = window.location.pathname.split('/')[2];  // Assuming URL is /sections/<section_id>/content/new/

    // Toggle between video URL or file field based on content type selection
    const contentTypeField = document.getElementById('content_type');
    const videoUrlField = document.getElementById('video-url-field');
    const fileField = document.getElementById('file-field');

    function toggleFields() {
        if (contentTypeField.value === 'video') {
            videoUrlField.style.display = 'block';
            fileField.style.display = 'none';
        } else if (contentTypeField.value === 'pdf') {
            videoUrlField.style.display = 'none';
            fileField.style.display = 'block';
        }
    }

    toggleFields();
    contentTypeField.addEventListener('change', toggleFields);

    // Handle form submission
    document.getElementById('add-content-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData();
        formData.append('title', document.getElementById('title').value);
        formData.append('content_type', document.getElementById('content_type').value);

        if (contentTypeField.value === 'video') {
            formData.append('video_url', document.getElementById('video_url').value);
        } else if (contentTypeField.value === 'pdf') {
            formData.append('file', document.getElementById('file').files[0]);
        }

        fetch(`/api/sections/${sectionId}/content-items`, {
            method: 'POST',
            headers: {
                'Authorization': 'Token ' + token
            },
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to add content');
            }
            return response.json();
        })
        .then(data => {
            window.location.href = `/sections/${sectionId}/edit`;  // Redirect back to content management page
        })
        .catch(error => {
            console.error('Error adding content:', error);
        });
    });
});
