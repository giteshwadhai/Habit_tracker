// Main JavaScript file for HabitTracker Pro

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add animation to cards on page load
    animateOnScroll();
    
    // Add scroll event listener for animations
    window.addEventListener('scroll', animateOnScroll);
    
    // Add animation to habit cards when toggled
    setupHabitToggleAnimations();
    
    // Setup flash message auto-dismiss
    setupFlashMessages();
    
    // Setup navbar scroll behavior
    setupNavbarScroll();
    
    // Dark mode toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        const themeIcon = themeToggle.querySelector('i');
        
        // Check for saved theme preference or use preferred color scheme
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        // Apply theme based on saved preference or system preference
        if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeIcon.classList.replace('fa-moon', 'fa-sun');
        }
        
        // Toggle theme when button is clicked
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            // Update theme attribute
            document.documentElement.setAttribute('data-theme', newTheme);
            
            // Update icon
            if (newTheme === 'dark') {
                themeIcon.classList.replace('fa-moon', 'fa-sun');
            } else {
                themeIcon.classList.replace('fa-sun', 'fa-moon');
            }
            
            // Save preference
            localStorage.setItem('theme', newTheme);
        });
    }
});

/**
 * Animate elements when they come into view
 */
function animateOnScroll() {
    const elements = document.querySelectorAll('.stats-card, .habit-card, .insight-card');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('animate-in');
        }
    });
}

/**
 * Setup animations for habit toggle buttons
 */
function setupHabitToggleAnimations() {
    const toggleButtons = document.querySelectorAll('.toggle-button');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Don't prevent default so the form still submits
            const habitCard = this.closest('.habit-card');
            
            if (!habitCard.classList.contains('completed')) {
                // Add completion animation
                this.classList.add('animate-complete');
                habitCard.classList.add('animate-complete');
                
                // Update the icon
                const icon = this.querySelector('i');
                icon.classList.remove('fa-circle');
                icon.classList.add('fa-check-circle');
                
                // Add confetti effect
                createConfetti(this);
            }
        });
    });
}

/**
 * Create confetti effect when completing a habit
 */
function createConfetti(element) {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    for (let i = 0; i < 30; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = centerX + 'px';
        confetti.style.top = centerY + 'px';
        
        // Random color
        const colors = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33', '#FF33F3'];
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        
        // Random size
        const size = Math.random() * 10 + 5;
        confetti.style.width = size + 'px';
        confetti.style.height = size + 'px';
        
        // Random rotation
        confetti.style.transform = `rotate(${Math.random() * 360}deg)`;
        
        // Random direction and distance
        const angle = Math.random() * Math.PI * 2;
        const distance = Math.random() * 100 + 50;
        const x = Math.cos(angle) * distance;
        const y = Math.sin(angle) * distance;
        
        document.body.appendChild(confetti);
        
        // Animate
        confetti.animate([
            { transform: `translate(0, 0) rotate(0deg)`, opacity: 1 },
            { transform: `translate(${x}px, ${y}px) rotate(${Math.random() * 360}deg)`, opacity: 0 }
        ], {
            duration: 1000,
            easing: 'cubic-bezier(0.1, 0.8, 0.2, 1)',
            fill: 'forwards'
        });
        
        // Remove after animation
        setTimeout(() => {
            confetti.remove();
        }, 1000);
    }
}

/**
 * Setup auto-dismiss for flash messages
 */
function setupFlashMessages() {
    const flashMessages = document.querySelectorAll('.alert');
    
    flashMessages.forEach(message => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = bootstrap.Alert.getOrCreateInstance(message);
            alert.close();
        }, 5000);
    });
}

/**
 * Setup navbar scroll behavior
 */
function setupNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 10) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
}

/**
 * Progress bar animation
 */
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const value = bar.getAttribute('aria-valuenow');
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = value + '%';
        }, 100);
    });
}

// Call progress bar animation on page load
document.addEventListener('DOMContentLoaded', animateProgressBars);