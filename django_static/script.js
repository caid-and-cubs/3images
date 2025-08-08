// AI Image Generator - Client-side functionality

// Global variables
let isGenerating = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize character counter
    const promptTextarea = document.getElementById('prompt');
    if (promptTextarea) {
        updateCharacterCount();
        promptTextarea.addEventListener('input', updateCharacterCount);
    }
    
    // Initialize form submission
    const generateForm = document.getElementById('generateForm');
    if (generateForm) {
        generateForm.addEventListener('submit', handleFormSubmission);
    }
    
    // Initialize gallery interactions
    initializeGallery();
    
    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();
    
    // Initialize tooltips
    initializeTooltips();
}

// Character counter functionality
function updateCharacterCount() {
    const textarea = document.getElementById('prompt');
    const counter = document.getElementById('charCount');
    
    if (!textarea || !counter) return;
    
    const currentLength = textarea.value.length;
    const maxLength = 1000;
    
    counter.textContent = currentLength;
    
    // Update counter color based on character count
    counter.className = '';
    if (currentLength > maxLength * 0.8) {
        counter.className = 'text-warning';
    }
    if (currentLength > maxLength * 0.95) {
        counter.className = 'text-danger';
    }
    
    // Update progress bar if it exists
    const progressBar = document.getElementById('charProgress');
    if (progressBar) {
        const percentage = (currentLength / maxLength) * 100;
        progressBar.style.width = percentage + '%';
        progressBar.setAttribute('aria-valuenow', percentage);
    }
}

// Form submission handling
function handleFormSubmission(event) {
    if (isGenerating) {
        event.preventDefault();
        return;
    }
    
    const prompt = document.getElementById('prompt').value.trim();
    
    // Validate prompt
    if (!prompt) {
        event.preventDefault();
        showAlert('Please enter a description for your image.', 'error');
        return;
    }
    
    if (prompt.length > 1000) {
        event.preventDefault();
        showAlert('Prompt is too long. Please keep it under 1000 characters.', 'error');
        return;
    }
    
    // Show loading state
    showLoadingState();
    isGenerating = true;
}

// Loading state management
function showLoadingState() {
    const generateBtn = document.getElementById('generateBtn');
    const btnText = generateBtn.querySelector('.btn-text');
    const spinner = generateBtn.querySelector('.spinner-border');
    const loadingSection = document.getElementById('loadingSection');
    
    // Update button state
    generateBtn.disabled = true;
    if (btnText) btnText.textContent = 'Generating...';
    if (spinner) spinner.classList.remove('d-none');
    
    // Show loading section
    if (loadingSection) {
        loadingSection.classList.remove('d-none');
        loadingSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    // Add pulse animation to loading elements
    const loadingElements = document.querySelectorAll('.spinner-border');
    loadingElements.forEach(el => el.classList.add('pulse'));
}

function hideLoadingState() {
    const generateBtn = document.getElementById('generateBtn');
    const btnText = generateBtn.querySelector('.btn-text');
    const spinner = generateBtn.querySelector('.spinner-border');
    const loadingSection = document.getElementById('loadingSection');
    
    // Reset button state
    generateBtn.disabled = false;
    if (btnText) btnText.textContent = 'Generate Image';
    if (spinner) spinner.classList.add('d-none');
    
    // Hide loading section
    if (loadingSection) {
        loadingSection.classList.add('d-none');
    }
    
    isGenerating = false;
}

// Gallery functionality
function initializeGallery() {
    // Add lazy loading for images
    const images = document.querySelectorAll('.gallery-image');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Add keyboard navigation for gallery
    document.addEventListener('keydown', function(event) {
        const modal = document.getElementById('imageModal');
        if (modal && modal.classList.contains('show')) {
            if (event.key === 'ArrowLeft') {
                navigateGallery('prev');
            } else if (event.key === 'ArrowRight') {
                navigateGallery('next');
            }
        }
    });
}

// Image modal functionality
function openImageModal(imageUrl, prompt, imageId) {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalPrompt = document.getElementById('modalPrompt');
    const modalDownload = document.getElementById('modalDownload');
    
    if (!modal || !modalImage || !modalPrompt || !modalDownload) return;
    
    // Set modal content
    modalImage.src = imageUrl;
    modalImage.alt = prompt;
    modalPrompt.textContent = prompt;
    modalDownload.href = modalDownload.href.replace(/\/\d+$/, '/' + imageId);
    
    // Store current image data for navigation
    modal.dataset.currentImageId = imageId;
    
    // Show modal
    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
    
    // Preload image for better UX
    const img = new Image();
    img.onload = function() {
        modalImage.style.opacity = '1';
    };
    img.src = imageUrl;
    modalImage.style.opacity = '0.5';
}

// Gallery navigation
function navigateGallery(direction) {
    // This would be implemented if we had next/prev functionality
    console.log('Gallery navigation:', direction);
}

// Delete confirmation
function confirmDelete(imageId) {
    const modal = document.getElementById('deleteModal');
    const deleteForm = document.getElementById('deleteForm');
    
    if (!modal || !deleteForm) return;
    
    // Update form action
    deleteForm.action = deleteForm.action.replace(/\/\d+$/, '/' + imageId);
    
    // Show modal
    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
}

// Prompt examples functionality
function fillPrompt(element) {
    const promptText = element.querySelector('p').textContent.replace(/"/g, '');
    const textarea = document.getElementById('prompt');
    
    if (!textarea) return;
    
    // Animate the filling
    textarea.style.transition = 'all 0.3s ease';
    textarea.style.transform = 'scale(1.02)';
    
    setTimeout(() => {
        textarea.value = promptText;
        updateCharacterCount();
        textarea.style.transform = 'scale(1)';
        textarea.focus();
        
        // Scroll to form
        textarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 150);
    
    // Add visual feedback
    element.style.transform = 'scale(0.98)';
    setTimeout(() => {
        element.style.transform = 'scale(1)';
    }, 200);
}

// Share functionality
function shareImage() {
    const imageUrl = document.getElementById('modalImage')?.src;
    const prompt = document.getElementById('modalPrompt')?.textContent;
    
    if (navigator.share && imageUrl) {
        navigator.share({
            title: 'AI Generated Image',
            text: `Check out this AI-generated image: "${prompt}"`,
            url: window.location.href
        }).catch(err => {
            console.log('Error sharing:', err);
            fallbackShare();
        });
    } else {
        fallbackShare();
    }
}

function fallbackShare() {
    const url = window.location.href;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(() => {
            showAlert('Link copied to clipboard!', 'success');
        }).catch(() => {
            showAlert('Could not copy link. Please copy manually: ' + url, 'info');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = url;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showAlert('Link copied to clipboard!', 'success');
        } catch (err) {
            showAlert('Could not copy link. Please copy manually: ' + url, 'info');
        }
        document.body.removeChild(textArea);
    }
}

// Alert system
function showAlert(message, type = 'info') {
    // Remove existing custom alerts
    const existingAlerts = document.querySelectorAll('.custom-alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show custom-alert`;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    
    const icon = type === 'error' ? 'exclamation-circle' : 
                 type === 'success' ? 'check-circle' : 'info-circle';
    
    alertDiv.innerHTML = `
        <i class="fas fa-${icon} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 300);
        }
    }, 5000);
}

// Keyboard shortcuts
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(event) {
        // Ctrl/Cmd + Enter to generate image
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            const generateForm = document.getElementById('generateForm');
            if (generateForm && !isGenerating) {
                event.preventDefault();
                generateForm.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to close modals
        if (event.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const bootstrapModal = bootstrap.Modal.getInstance(modal);
                if (bootstrapModal) {
                    bootstrapModal.hide();
                }
            });
        }
    });
}

// Tooltip initialization
function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipElements.forEach(el => new bootstrap.Tooltip(el));
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Error handling
window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
    hideLoadingState();
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    hideLoadingState();
});

// Service worker registration (for future PWA support)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Service worker would be registered here in a full PWA implementation
    });
}

// Export functions for global access
window.openImageModal = openImageModal;
window.confirmDelete = confirmDelete;
window.fillPrompt = fillPrompt;
window.shareImage = shareImage;
