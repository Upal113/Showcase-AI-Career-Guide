// Fetch the JSON data for industries
fetch('jobs.json')
.then(response => response.json())
.then(data => {
    const industrySelect = document.getElementById('industrySelect');
    const industries = [...new Set(data.jobs.map(job => job.industry))];

    industries.forEach(industry => {
        const option = document.createElement('option');
        option.value = industry;
        option.textContent = industry;
        industrySelect.appendChild(option);
    });
})
.catch(error => console.error('Error fetching JSON:', error));

// Fetch the JSON data for courses
fetch('courses.json')
.then(response => response.json())
.then(data => {
const coursesSelect = document.getElementById('coursesSelect');

for (const university in data) {
    if (data.hasOwnProperty(university)) {
        const courses = data[university].courses;
        courses.forEach(course => {
            const option = document.createElement('option');
            option.value = course.course_code;
            option.textContent = course.course_code + ' - ' + course.course_name;
            coursesSelect.appendChild(option);
        });
    }
}
})
.catch(error => console.error('Error fetching JSON:', error));

// Function to create and display a card for a job recommendation
function displayRecommendation(job, company, industry, recommendation) {
const recommendationsDiv = document.getElementById('recommendations');

// Create a Bootstrap card
const card = document.createElement('div');
card.classList.add('card', 'mb-3');

// Create card body
const cardBody = document.createElement('div');
cardBody.classList.add('card-body');

// Add job title to the card
const jobTitle = document.createElement('h5');
jobTitle.classList.add('card-title');
jobTitle.textContent = `Job: ${job}`;
cardBody.appendChild(jobTitle);

// Add company to the card
const companyText = document.createElement('p');
companyText.classList.add('card-text');
companyText.textContent = `Company: ${company}`;
cardBody.appendChild(companyText);

// Add industry to the card
const industryText = document.createElement('p');
industryText.classList.add('card-text');
industryText.textContent = `Industry: ${industry}`;
cardBody.appendChild(industryText);

// Add recommendation to the card
const recommendationText = document.createElement('p');
recommendationText.classList.add('card-text');
recommendationText.textContent = `Recommendation: ${recommendation}`;
cardBody.appendChild(recommendationText);

card.appendChild(cardBody);

recommendationsDiv.appendChild(card);
}

document.getElementById('applyFilters').addEventListener('click', function () {
// Clear previous recommendations
document.getElementById('recommendations').innerHTML = '';

// Get selected industry and course options
const selectedIndustryOptions = Array.from(document.getElementById('industrySelect').selectedOptions).map(option => option.value);
const selectedCourseOptions = Array.from(document.getElementById('coursesSelect').selectedOptions).map(option => option.value);

// Create JSON object with selected options
const requestData = {
    "courses": selectedCourseOptions,
    "industry": selectedIndustryOptions
};

// Send a POST request to the Flask API endpoint
fetch('http://127.0.0.1:5000/recommend', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
})
.then(response => {
    console.log('Request URL:', response.url); // Log the request URL for monitoring
    return response.json();
})
.then(data => {
    console.log('Recommendation:', data.recommendation);
    // Display recommendations
    displayRecommendation(data.Job, data.Company, data.industry, data.recommendation);
})
.catch(error => console.error('Error:', error));
});