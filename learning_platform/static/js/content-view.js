document.addEventListener('DOMContentLoaded', function() {
    const contentId = window.location.pathname.split('/')[2];  // Extract content ID from URL
    const contentTitle = document.querySelector('.content-title');
    const contentContainer = document.getElementById('content-container');
    const token = localStorage.getItem('token');

    // Function to transform YouTube URL into embed format
    function getYouTubeEmbedUrl(videoUrl) {
        const videoId = videoUrl.split('v=')[1];  // Extract video ID
        return `https://www.youtube.com/embed/${videoId}`;
    }

    // Fetch content item details
    fetch(`/api/content-items/${contentId}/`, {
        headers: { 'Authorization': token ? 'Token ' + token : '' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.title) {
            contentTitle.textContent = data.title;

            // Display content based on type
            if (data.content_type === 'pdf') {
                const pdfViewer = document.createElement('iframe');
                pdfViewer.src = data.file;
                pdfViewer.width = '100%';
                pdfViewer.height = '600px';
                pdfViewer.style.border = 'none';
                contentContainer.appendChild(pdfViewer);
            } else if (data.content_type === 'video') {
                const embedUrl = getYouTubeEmbedUrl(data.video_url);  // Transform the YouTube URL
                const videoFrame = document.createElement('iframe');
                videoFrame.src = embedUrl;
                videoFrame.width = '100%';
                videoFrame.height = '500px';
                videoFrame.style.border = 'none';
                videoFrame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
                videoFrame.allowFullscreen = true;  // Allow fullscreen
                contentContainer.appendChild(videoFrame);
            } else {
                contentContainer.innerHTML = "<p>Unsupported content type.</p>";
            }
        } else {
            contentContainer.innerHTML = "<p>Content not found.</p>";
        }
    })
    .catch(error => {
        contentContainer.innerHTML = `<p>Error fetching content: ${error}</p>`;
    });
});
