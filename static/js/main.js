// Main JavaScript for Frontdesk AI application

document.addEventListener('DOMContentLoaded', function() {
    console.log('Frontdesk AI Dashboard initialized');
    
    // Auto-refresh for requests page - every 30 seconds
    if (window.location.pathname.includes('/requests')) {
        setInterval(function() {
            checkForNewRequests();
        }, 30000);
    }
    
    // Initialize any tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });
});

// Function to check for new help requests without full page reload
function checkForNewRequests() {
    console.log('Checking for new requests...');
    // In a real implementation, this would make an AJAX call to check for new requests
    // For this demo, we'll just use the current count from the page
    
    // This would be replaced with actual API call in production:
    // fetch('/api/check-new-requests')
    // .then(response => response.json())
    // .then(data => {
    //     if (data.new_requests > 0) {
    //         // Show notification or auto-refresh
    //     }
    // })
}

// Function to format timestamps
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

// Function to copy text to clipboard
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    
    // Show feedback
    alert('Copied to clipboard!');
}
