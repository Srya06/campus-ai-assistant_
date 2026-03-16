// API Configuration
const API_URL = 'http://localhost:8000';
let currentOutput = '';

// Handle form submission
async function handleSubmit(event) {
    event.preventDefault();
    
    // Get form values
    const type = document.getElementById('type').value;
    const message = document.getElementById('message').value.trim();
    const tone = document.getElementById('tone').value;
    const length = document.getElementById('length').value;
    
    // Validate inputs
    if (!type || !message || !tone || !length) {
        showError('Please fill in all fields');
        return;
    }
    
    if (message.length < 5) {
        showError('Message must be at least 5 characters long');
        return;
    }
    
    // Show loading state
    setLoading(true);
    hideError();
    
    try {
        const response = await fetch(`${API_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: type,
                message: message,
                tone: tone,
                length: length
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate message');
        }
        
        const data = await response.json();
        displayOutput(data.output);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred while generating the message');
    } finally {
        setLoading(false);
    }
}

// Display generated output
function displayOutput(text) {
    currentOutput = text;
    const outputElement = document.getElementById('output');
    const outputSection = document.getElementById('outputSection');
    
    outputElement.textContent = text;
    outputSection.style.display = 'block';
    
    // Scroll to output
    outputSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Copy to clipboard
async function copyToClipboard() {
    if (!currentOutput) return;
    
    try {
        await navigator.clipboard.writeText(currentOutput);
        showTemporaryMessage('📋 Copied to clipboard!');
    } catch (err) {
        console.error('Failed to copy:', err);
        showError('Failed to copy to clipboard');
    }
}

// Download as text file
function downloadOutput() {
    if (!currentOutput) return;
    
    const type = document.getElementById('type').value;
    const blob = new Blob([currentOutput], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    
    a.href = url;
    a.download = `${type.toLowerCase().replace(' ', '_')}_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showTemporaryMessage('💾 File downloaded!');
}

// Show temporary success message
function showTemporaryMessage(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.style.backgroundColor = '#4CAF50';
    
    setTimeout(() => {
        errorDiv.style.display = 'none';
        errorDiv.style.backgroundColor = '#f44336';
    }, 2000);
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Hide error message
function hideError() {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.style.display = 'none';
}

// Set loading state
function setLoading(isLoading) {
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.loading-spinner');
    
    submitBtn.disabled = isLoading;
    
    if (isLoading) {
        btnText.style.display = 'none';
        spinner.style.display = 'inline';
        submitBtn.style.opacity = '0.7';
    } else {
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
        submitBtn.style.opacity = '1';
    }
}

// Character counter
document.getElementById('message').addEventListener('input', function() {
    const count = this.value.length;
    const charCount = document.getElementById('charCount');
    charCount.textContent = count;
    
    // Visual feedback for character limit
    if (count > 900) {
        charCount.style.color = '#ff9800';
    } else if (count >= 1000) {
        charCount.style.color = '#f44336';
    } else {
        charCount.style.color = '#666';
    }
});

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    console.log('Campus Communication Assistant loaded');
    
    // Check API health
    fetch(`${API_URL}/health`)
        .then(response => response.json())
        .then(data => console.log('API Status:', data))
        .catch(error => console.error('API not available:', error));
});