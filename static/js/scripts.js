// TikTok Parser Web Interface Scripts

document.addEventListener('DOMContentLoaded', function() {
    // Form submission handling
    const parserForm = document.getElementById('parser-form');
    const submitButton = document.getElementById('submit-button');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    if (parserForm) {
        parserForm.addEventListener('submit', function() {
            // Disable submit button and show loading indicator
            if (submitButton && loadingIndicator) {
                submitButton.disabled = true;
                submitButton.innerHTML = 'Processing...';
                loadingIndicator.style.display = 'block';
            }
        });
    }
    
    // API Token field handling
    const apiTokenField = document.getElementById('api_token');
    const saveTokenCheckbox = document.getElementById('save_token');
    
    if (apiTokenField && saveTokenCheckbox) {
        // Load saved token if exists
        const savedToken = localStorage.getItem('apify_api_token');
        if (savedToken) {
            apiTokenField.value = savedToken;
            saveTokenCheckbox.checked = true;
        }
        
        // Save token when checkbox is checked
        saveTokenCheckbox.addEventListener('change', function() {
            if (this.checked && apiTokenField.value) {
                localStorage.setItem('apify_api_token', apiTokenField.value);
            } else {
                localStorage.removeItem('apify_api_token');
            }
        });
        
        // Update saved token when field changes
        apiTokenField.addEventListener('input', function() {
            if (saveTokenCheckbox.checked) {
                localStorage.setItem('apify_api_token', this.value);
            }
        });
    }
    
    // Topic tags handling
    const topicsInput = document.getElementById('topics');
    const topicTagsContainer = document.getElementById('topic-tags');
    
    if (topicsInput && topicTagsContainer) {
        // Update topic tags when input changes
        topicsInput.addEventListener('input', function() {
            updateTopicTags();
        });
        
        // Initial update
        updateTopicTags();
        
        function updateTopicTags() {
            const topics = topicsInput.value.split(',').map(topic => topic.trim()).filter(topic => topic);
            
            // Clear existing tags
            topicTagsContainer.innerHTML = '';
            
            // Create new tags
            topics.forEach(topic => {
                if (topic) {
                    const tag = document.createElement('span');
                    tag.className = 'badge bg-primary me-2 mb-2';
                    tag.textContent = topic;
                    topicTagsContainer.appendChild(tag);
                }
            });
            
            // Show/hide container based on tags
            topicTagsContainer.style.display = topics.length > 0 ? 'block' : 'none';
        }
    }
});
