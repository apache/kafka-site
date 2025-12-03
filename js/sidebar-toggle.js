document.addEventListener('DOMContentLoaded', function () {
    const sidebarToggles = document.querySelectorAll('.td-sidebar__toggle');

    sidebarToggles.forEach(toggle => {
        // Remove any existing event listeners by cloning and replacing the node
        // This is a nuclear option to ensure we kill the conflicting listener
        const newToggle = toggle.cloneNode(true);
        toggle.parentNode.replaceChild(newToggle, toggle);

        newToggle.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();

            console.log('Sidebar toggle clicked (custom handler)');

            // Try to find target ID from various attributes
            let targetId = this.getAttribute('aria-controls') ||
                this.getAttribute('data-target') ||
                this.getAttribute('data-bs-target');

            // Default to standard ID if not found
            if (!targetId) targetId = 'td-section-nav';

            // Clean up ID selector if present
            if (targetId.startsWith('#')) {
                targetId = targetId.substring(1);
            }

            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                // Toggle visibility manually
                if (targetElement.classList.contains('show')) {
                    targetElement.classList.remove('show');
                    targetElement.style.height = '0';
                    targetElement.style.display = 'none'; // Force hide
                    this.setAttribute('aria-expanded', 'false');
                } else {
                    targetElement.classList.add('show');
                    targetElement.style.height = 'auto';
                    targetElement.style.display = 'block'; // Force show
                    this.setAttribute('aria-expanded', 'true');
                }
            } else {
                console.warn('Sidebar toggle: Target element not found', targetId);
            }
        });
    });
});
