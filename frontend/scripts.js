let extractedSkills = [];
let extractedEducation = '';

// // Add file selection handler
// document.getElementById('resume').addEventListener('change', function(e) {
//     const fileName = e.target.files[0]?.name;
//     const fileNameDiv = document.getElementById('file-name');
//     const button = document.getElementById('browse-upload-btn');
    
//     if (fileName) {
//         fileNameDiv.textContent = fileName;
//         fileNameDiv.classList.remove('hidden');
//         button.textContent = 'Upload Now';
//     }
// });

// // Modify the browse/upload button click handler
// document.getElementById('browse-upload-btn').addEventListener('click', function(event) {
//     event.preventDefault();
//     if (this.textContent === 'Browse Files') {
//         document.getElementById('resume').click();
//     } else if (this.textContent === 'Upload Now') {
//         // Trigger the form submission
//         const formEvent = new Event('submit');
//         document.getElementById('resumeForm').dispatchEvent(formEvent);
//     }
// });

// // Your original form submission handler (modified slightly)
// document.getElementById('resumeForm').addEventListener('submit', async function(event) {
//     event.preventDefault();

//     const formData = new FormData();
//     const resumeFile = document.getElementById('resume').files[0];
//     formData.append('file', resumeFile);

//     try {
//         const response = await fetch('http://127.0.0.1:5000/upload_resume', {
//             method: 'POST',
//             body: formData
//         });

//         const resumeData = await response.json();
//         extractedSkills = resumeData.skills;
//         extractedEducation = resumeData.education;

//         // Display extracted information
//         document.getElementById('education-info').innerText = extractedEducation;
//         document.getElementById('skills-info').innerText = extractedSkills.join(', ');
//         document.getElementById('extracted-info').classList.remove('hidden');

//         // Reset the upload area after successful upload
//         document.getElementById('browse-upload-btn').textContent = 'Browse Files';
//         document.getElementById('file-name').classList.add('hidden');
        
//         alert('Resume uploaded successfully and data extracted! Now enter your experience and get recommendations.');
//     } catch (error) {
//         console.error('Error uploading resume:', error);
//     }
// });


// // Modify your existing form submit event
// document.getElementById('resumeForm').addEventListener('submit', async function(event) {
//     event.preventDefault();
// });

// Add new button click handler
// document.getElementById('browse-upload-btn').addEventListener('click', async function() {
//     const button = this;
//     const fileInput = document.getElementById('resume');
//     const fileNameDiv = document.getElementById('file-name');
//     const uploadText = document.getElementById('upload-text');

//     if (button.textContent === 'Browse Files') {
//         fileInput.click();
//     } else if (button.textContent === 'Upload Now') {
//         const formData = new FormData();
//         const resumeFile = fileInput.files[0];
        
//         if (!resumeFile) {
//             alert('Please select a file first');
//             return;
//         }

//         formData.append('file', resumeFile);

//         try {
//             const response = await fetch('http://127.0.0.1:5000/upload_resume', {
//                 method: 'POST',
//                 body: formData
//             });

//             const resumeData = await response.json();
//             extractedSkills = resumeData.skills;
//             extractedEducation = resumeData.education;

//             // Display extracted information
//             document.getElementById('education-info').innerText = extractedEducation;
//             document.getElementById('skills-info').innerText = extractedSkills.join(', ');
//             document.getElementById('extracted-info').classList.remove('hidden');

//             // Reset the upload area
//             button.textContent = 'Browse Files';
//             fileNameDiv.classList.add('hidden');
//             uploadText.textContent = '✨ Resume uploaded successfully! ✨';
//             fileInput.value = ''; // Clear the file input

//             // Show success message
//             setTimeout(() => {
//                 uploadText.textContent = '✨ Drop your resume here, let's make magic happen! ✨';
//             }, 3000); // Reset message after 3 seconds

//         } catch (error) {
//             console.error('Error uploading resume:', error);
//             uploadText.textContent = '❌ Error uploading file. Please try again.';
//             button.textContent = 'Browse Files';
//             fileNameDiv.classList.add('hidden');
//             fileInput.value = '';
//         }
//     }
// });

document.getElementById('resumeForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();
    const resumeFile = document.getElementById('resume').files[0];
    formData.append('file', resumeFile);

    try {
        const response = await fetch('http://127.0.0.1:5000/upload_resume', {
            method: 'POST',
            body: formData
        });

        const resumeData = await response.json();
        extractedSkills = resumeData.skills;
        extractedEducation = resumeData.education;

        // Display extracted information
        document.getElementById('education-info').innerText = extractedEducation;
        document.getElementById('skills-info').innerText = extractedSkills.join(', ');
        document.getElementById('extracted-info').classList.remove('hidden');

        alert('Resume uploaded successfully and data extracted! Now enter your experience and get recommendations.');
    } catch (error) {
        console.error('Error uploading resume:', error);
    }
});


document.getElementById('jobForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const experience = document.getElementById('experience').value;
    const num_recommendations = document.getElementById('num_recommendations').value;

    const formData = {
        skills: extractedSkills,
        education: extractedEducation,
        experience: parseFloat(experience),
        num_recommendations: parseInt(num_recommendations, 10)
    };

    // Show loading indicator
    const loadingIndicator = document.getElementById('loading');
    loadingIndicator.classList.remove('hidden');

    try {
        const response = await fetch('http://127.0.0.1:5000/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const recommendations = await response.json();
        displayRecommendations(recommendations);
    } catch (error) {
        console.error('Error fetching recommendations:', error);
    } finally {
        // Hide loading indicator
        loadingIndicator.classList.add('hidden');
    }
});

function displayRecommendations(recommendations) {
    const recommendationsContainer = document.getElementById('recommendations');
    recommendationsContainer.innerHTML = '';

    if (recommendations.length === 0) {
        recommendationsContainer.innerHTML = '<p>No matching jobs found.</p>';
        return;
    }

    recommendations.forEach(job => {
        const jobCard = document.createElement('div');
        jobCard.className = '';

        jobCard.innerHTML = `
            <div class="bg-[#0a1f1f] rounded-xl shadow-lg hover:shadow-xl text-white duration-300 p-8 space-y-6 backdrop-blur-sm border border-[#64FFDA]/20 transform hover:-translate-y-1">
            <div class="heart-container" title="Like">
            <input type="checkbox" class="checkbox" id="Give-It-An-Id">
            <div class="svg-container">
                <svg viewBox="0 0 24 24" class="svg-outline" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Zm-3.585,18.4a2.973,2.973,0,0,1-3.83,0C4.947,16.006,2,11.87,2,8.967a4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,11,8.967a1,1,0,0,0,2,0,4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,22,8.967C22,11.87,19.053,16.006,13.915,20.313Z">
                    </path>
                </svg>
                <svg viewBox="0 0 24 24" class="svg-filled" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Z">
                    </path>
                </svg>
                <svg class="svg-celebrate" width="100" height="100" xmlns="http://www.w3.org/2000/svg">
                    <polygon points="10,10 20,20"></polygon>
                    <polygon points="10,50 20,50"></polygon>
                    <polygon points="20,80 30,70"></polygon>
                    <polygon points="90,10 80,20"></polygon>
                    <polygon points="90,50 80,50"></polygon>
                    <polygon points="80,80 70,70"></polygon>
                </svg>
            </div>
        </div>
            <h3 class="text-xl font-bold">${job.job_title}</h3>
            <p><strong>Company:</strong> ${job.company}</p>
            <p><strong>Location:</strong> ${job.location}</p>
            <p><strong>Match Score:</strong> ${job.match_score}%</p>
            <p><strong>Matching Skills:</strong> ${job.matching_skills.join(', ')}</p>
            <p><strong>Skills to Learn:</strong> ${job.missing_skills.join(', ')}</p>
            </div>
        `;

        recommendationsContainer.appendChild(jobCard);
    });
}
