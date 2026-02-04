document.addEventListener('DOMContentLoaded', () => {
    const roleCards = document.querySelectorAll('.role-card');

    roleCards.forEach(card => {
        card.addEventListener('click', () => {
            const role = card.dataset.role;
            
            // Add selection animation
            card.classList.add('selected');
            
            // Wait for animation then navigate
            setTimeout(() => {
                window.location.href = `roadmap.html?role=${role}`;
            }, 400);
        });
    });
});
