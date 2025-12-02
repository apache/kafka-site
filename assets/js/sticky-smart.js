document.addEventListener('DOMContentLoaded', function () {
    const sidebarContent = document.querySelector('.td-sidebar .td-sticky-content');

    if (!sidebarContent) return;

    function syncSidebarScroll() {
        // Only sync if mouse is NOT hovering the sidebar (to avoid fighting user)
        if (sidebarContent.matches(':hover')) return;

        const winScroll = window.scrollY;
        const winHeight = window.innerHeight;
        const docHeight = document.documentElement.scrollHeight;

        const scrollPercent = winScroll / (docHeight - winHeight);

        const sidebarHeight = sidebarContent.scrollHeight;
        const sidebarVisibleHeight = sidebarContent.offsetHeight;

        if (sidebarHeight > sidebarVisibleHeight) {
            sidebarContent.scrollTop = scrollPercent * (sidebarHeight - sidebarVisibleHeight);
        }
    }

    window.addEventListener('scroll', syncSidebarScroll);
});
