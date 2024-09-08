document.addEventListener('DOMContentLoaded', function() {
    const contentTypeField = document.getElementById('content_type');
    const videoUrlField = document.getElementById('video-url-field');
    const fileField = document.getElementById('file-field');
    const backButton = document.getElementById('back-button');
    const pathParts = window.location.pathname.split('/');
    const token = localStorage.getItem('token');
    let isEditMode = pathParts[3] !== 'create';
    let sectionId = null;
    let contentId = null;

    if (isEditMode) {
        contentId = pathParts[2];
    } else {
        sectionId = pathParts[2];
    }

    function toggleFields() {
        if (contentTypeField.value === 'video') {
            videoUrlField.style.display = 'block';
            fileField.style.display = 'none';
        } else if (contentTypeField.value === 'pdf') {
            videoUrlField.style.display = 'none';
            fileField.style.display = 'block';
        }
    }

    // If editing existing content, fetch content details
    if (isEditMode) {
        fetch(`/api/content-items/${contentId}`, {
            headers: { 'Authorization': 'Token ' + token }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('title').value = data.title;
            document.getElementById('content_type').value = data.content_type;
            sectionId = data.section;  // Store section_id from API response

            // Set back button URL
            backButton.href = `/sections/${sectionId}/edit/`;

            toggleFields();

            if (data.content_type === 'video') {
                document.getElementById('video_url').value = data.video_url;
            }
        })
        .catch(error => {
            console.error('Error fetching content data:', error);
            alert('Failed to load content data.');
        });
    } else {
        // Set back button URL when in add mode (use sectionId from URL)
        backButton.href = `/sections/${sectionId}/edit/`;
        toggleFields();
    }
    contentTypeField.addEventListener('change', toggleFields);

    document.getElementById('content-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData();
        formData.append('title', document.getElementById('title').value);
        formData.append('content_type', document.getElementById('content_type').value);

        if (contentTypeField.value === 'video') {
            formData.append('video_url', document.getElementById('video_url').value);
        } else if (contentTypeField.value === 'pdf') {
            const fileInput = document.getElementById('file');
            if (fileInput.files.length > 0) {
                formData.append('file', fileInput.files[0]);
            }
        }

        // Use the correct URL and method depending on add/edit mode
        const url = isEditMode ? `/api/content-items/${contentId}` : `/api/content-items/${sectionId}/add`;
        const method = isEditMode ? 'PUT' : 'POST';

        fetch(url, {
            method: method,
            headers: { 'Authorization': 'Token ' + token },
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.href = `/sections/${sectionId}/edit/`;  // Redirect back to section edit page
            } else {
                alert('Failed to process the request.');
            }
        });
    });
});
