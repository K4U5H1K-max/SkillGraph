// Landing Page Transition Script

document.addEventListener('DOMContentLoaded', () => {
    const getStartedBtn = document.getElementById('getStartedBtn');
    const landingContainer = document.querySelector('.landing-container');

    // Add click event to Get Started button
    getStartedBtn.addEventListener('click', () => {
        // Add fade-out class
        landingContainer.classList.add('fade-out');

        // Wait for animation to complete, then navigate
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 600);
    });

    // Add subtle parallax effect on mouse move
    document.addEventListener('mousemove', (e) => {
        const circles = document.querySelectorAll('.circle');
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;

        circles.forEach((circle, index) => {
            const speed = (index + 1) * 20;
            const x = (mouseX - 0.5) * speed;
            const y = (mouseY - 0.5) * speed;
            
            circle.style.transform = `translate(${x}px, ${y}px)`;
        });
    });

    // Add keyboard shortcut (Enter key)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            getStartedBtn.click();
        }
    });

    // Add button press animation
    getStartedBtn.addEventListener('mousedown', () => {
        getStartedBtn.style.transform = 'scale(0.95)';
    });

    getStartedBtn.addEventListener('mouseup', () => {
        getStartedBtn.style.transform = '';
    });
});
