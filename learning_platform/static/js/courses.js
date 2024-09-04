document.addEventListener('DOMContentLoaded', function() {
    let currentPage = 1;
    const courseContainer = document.getElementById('course-container');
    const pageInfo = document.getElementById('page-info');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');

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
                pageInfo.textContent = `Page ${page} of ${Math.ceil(data.count / PAGE_SIZE)}`;
                prevButton.disabled = !data.previous;
                nextButton.disabled = !data.next;

                // Update current page
                currentPage = page;
            })
            .catch(error => console.error('Error fetching courses:', error));
    }

    // Load the first page of courses
    loadCourses(currentPage);

    // Add event listeners for pagination buttons
    prevButton.addEventListener('click', () => loadCourses(currentPage - 1));
    nextButton.addEventListener('click', () => loadCourses(currentPage + 1));
});
