document.addEventListener('DOMContentLoaded', function() {
    const contentId = window.location.pathname.split('/')[2];  // Assuming URL is /content/<content_id>/edit/
    const token = localStorage.getItem('token');

    // Fetch content details to populate the form
    fetch(`/api/content-items/${contentId}/`, {
        headers: { 'Authorization': 'Token ' + token }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('title').value = data.title;
        document.getElementById('content_type').value = data.content_type;

        if (data.content_type === 'video') {
            document.getElementById('video-url-field').style.display = 'block';
            document.getElementById('file-field').style.display = 'none';
            document.getElementById('video_url').value = data.video_url;
        } else if (data.content_type === 'pdf') {
            document.getElementById('video-url-field').style.display = 'none';
            document.getElementById('file-field').style.display = 'block';
        }
    });

    // Handle form submission
    document.getElementById('modify-content-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData();
        formData.append('title', document.getElementById('title').value);
        formData.append('content_type', document.getElementById('content_type').value);

        if (document.getElementById('content_type').value === 'video') {
            formData.append('video_url', document.getElementById('video_url').value);
        } else if (document.getElementById('content_type').value === 'pdf') {
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
                window.location.href = `/sections/${data.section_id}/edit/`;  // Redirect back to section edit page
            } else {
                alert('Failed to update content.');
            }
        });
    });
});
