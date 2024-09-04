document.addEventListener('DOMContentLoaded', function() {
    let currentPage = 1;
    const courseContainer = document.getElementById('course-container');
    const pageInfo = document.getElementById('page-info');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');

    // Get the page number from the URL (if available)
    const urlParams = new URLSearchParams(window.location.search);
    const initialPage = parseInt(urlParams.get('page')) || 1;

    function loadCourses(page) {
        fetch(`/api/courses/?page=${page}`)
            .then(response => response.json())
            .then(data => {
                courseContainer.innerHTML = '';
                data.results.forEach(course => {
                    const courseDiv = document.createElement('div');
                    courseDiv.className = 'course';
                    courseDiv.innerHTML = `<h3>${course.title}</h3><p>${course.description}</p>`;
                    courseContainer.appendChild(courseDiv);
                });

                // Update pagination controls
                const totalPages = Math.ceil(data.count / PAGE_SIZE);
                pageInfo.textContent = `Page ${page} of ${totalPages}`;
                prevButton.disabled = !data.previous;
                nextButton.disabled = !data.next;

                // Update current page
                currentPage = page;

                // Update the URL without refreshing the page
                const newUrl = `${window.location.pathname}?page=${page}`;
                window.history.pushState({page}, '', newUrl);
            })
            .catch(error => console.error('Error fetching courses:', error));
    }

    // Load the page based on the URL, or default to page 1
    loadCourses(initialPage);

    // Add event listeners for pagination buttons
    prevButton.addEventListener('click', () => loadCourses(currentPage - 1));
    nextButton.addEventListener('click', () => loadCourses(currentPage + 1));

    // Listen for browser back/forward navigation events
    window.addEventListener('popstate', function(event) {
        if (event.state && event.state.page) {
            loadCourses(event.state.page);
        }
    });
});