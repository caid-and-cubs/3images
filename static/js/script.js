// AI Image Generator JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Character counter for prompt textarea
    const promptTextarea = document.getElementById('prompt');
    const charCount = document.getElementById('charCount');
    const maxChars = 1000;

    if (promptTextarea && charCount) {
        function updateCharCount() {
            const currentLength = promptTextarea.value.length;
            charCount.textContent = `${currentLength}/${maxChars}`;
            
            if (currentLength > maxChars * 0.9) {
                charCount.classList.add('text-warning');
            } else {
                charCount.classList.remove('text-warning');
            }
            
            if (currentLength > maxChars) {
                charCount.classList.add('text-danger');
                charCount.classList.remove('text-warning');
            } else {
                charCount.classList.remove('text-danger');
            }
        }

        promptTextarea.addEventListener('input', updateCharCount);
        updateCharCount(); // Initial count
    }

    // Form submission with loading state
    const generateForm = document.getElementById('generateForm');
    if (generateForm) {
        generateForm.addEventListener('submit', function() {
            const submitBtn = generateForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('generating');
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating...';
            }
        });
    }

    // Delete confirmation
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const imageId = this.dataset.imageId;
            const prompt = this.dataset.prompt || 'this image';
            
            if (confirm(`Are you sure you want to delete "${prompt.substring(0, 50)}..."?`)) {
                // Create and submit delete form
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = this.href;
                
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                if (csrfToken) {
                    const csrfInput = document.createElement('input');
                    csrfInput.type = 'hidden';
                    csrfInput.name = 'csrfmiddlewaretoken';
                    csrfInput.value = csrfToken.value;
                    form.appendChild(csrfInput);
                }
                
                document.body.appendChild(form);
                form.submit();
            }
        });
    });

    // Image lazy loading and error handling
    const images = document.querySelectorAll('img[data-src]');
    if (images.length > 0 && 'IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }
});