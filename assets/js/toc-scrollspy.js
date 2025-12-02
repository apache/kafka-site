document.addEventListener('DOMContentLoaded', function () {
    const tocLinks = document.querySelectorAll('.td-toc-content a');
    const headings = Array.from(document.querySelectorAll('main h2, main h3, main h4'));

    if (tocLinks.length === 0 || headings.length === 0) return;

    // Create a map of heading IDs to TOC links for O(1) lookup
    const linkMap = new Map();
    tocLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('#')) {
            linkMap.set(href.substring(1), link);
        }
    });

    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -80% 0px', // Trigger when heading is near the top (20% from top)
        threshold: 0
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Remove active class from all links
                tocLinks.forEach(link => link.classList.remove('active'));

                // Add active class to the corresponding link
                const id = entry.target.id;
                const activeLink = linkMap.get(id);
                if (activeLink) {
                    activeLink.classList.add('active');

                    // Scroll active link into view within the sticky container
                    activeLink.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

                    // Also highlight parent links if nested
                    let parent = activeLink.parentElement;
                    while (parent) {
                        if (parent.tagName === 'LI') {
                            // Check if this LI has a direct link child
                            const parentLink = parent.querySelector(':scope > a');
                            if (parentLink) parentLink.classList.add('active');
                        }
                        if (parent.classList.contains('td-sidebar-toc')) break;
                        parent = parent.parentElement;
                    }
                }
            }
        });
    }, observerOptions);

    headings.forEach(heading => observer.observe(heading));
});
