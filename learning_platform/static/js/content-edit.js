document.addEventListener('DOMContentLoaded', function() {
    const contentTypeField = document.getElementById('content_type');
    const videoUrlField = document.getElementById('video-url-field');
    const fileField = document.getElementById('file-field');
    const contentId = window.location.pathname.split('/')[2];  // Assuming URL is /content/<content_id>/edit/
    const token = localStorage.getItem('token');
    let sectionId = null;  // Store section ID here

    // Function to toggle the visibility of fields based on the content type
    function toggleFields() {
        if (contentTypeField.value === 'video') {
            videoUrlField.style.display = 'block';
            fileField.style.display = 'none';
        } else if (contentTypeField.value === 'pdf') {
            videoUrlField.style.display = 'none';
            fileField.style.display = 'block';
        }
    }

    // Fetch content details to populate the form
    fetch(`/api/content-items/${contentId}/`, {
        headers: { 'Authorization': 'Token ' + token }
    })
    .then(response => response.json())
    .then(data => {
        // Pre-fill the form with content data
        document.getElementById('title').value = data.title;
        document.getElementById('content_type').value = data.content_type;

        // Store section ID to use after content update
        sectionId = data.section_id;

        // Initially toggle the fields based on the content type
        toggleFields();

        if (data.content_type === 'video') {
            document.getElementById('video_url').value = data.video_url;
        }
    });

    // Call toggleFields when the content type is changed
    contentTypeField.addEventListener('change', toggleFields);

    // Handle form submission
    document.getElementById('edit-content-form').addEventListener('submit', function(event) {
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

        fetch(`/api/content-items/${contentId}/`, {
            method: 'PUT',
            headers: { 'Authorization': 'Token ' + token },
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Use the stored sectionId for redirect
                window.location.href = `/sections/${sectionId}/edit`;  // Redirect back to section edit page
            } else {
                alert('Failed to update content.');
            }
        });
    });
});
