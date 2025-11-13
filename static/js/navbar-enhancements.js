// Navbar enhancements for Apache Kafka site
(function() {
  'use strict';
  
  // Wait for DOM to be ready
  document.addEventListener('DOMContentLoaded', function() {
    
    // Add hover support for dropdowns on desktop only
    function setupDesktopHover() {
      if (window.innerWidth >= 992) {
        const dropdowns = document.querySelectorAll('.td-navbar .dropdown');
        
        dropdowns.forEach(function(dropdown) {
          dropdown.addEventListener('mouseenter', function() {
            const dropdownMenu = this.querySelector('.dropdown-menu');
            if (dropdownMenu) {
              dropdownMenu.classList.add('show');
              this.classList.add('show');
            }
          });
          
          dropdown.addEventListener('mouseleave', function() {
            const dropdownMenu = this.querySelector('.dropdown-menu');
            if (dropdownMenu) {
              dropdownMenu.classList.remove('show');
              this.classList.remove('show');
            }
          });
        });
      }
    }
    
    // Setup mobile dropdown click handling
    function setupMobileDropdowns() {
      if (window.innerWidth < 992) {
        const dropdownToggles = document.querySelectorAll('.td-navbar .dropdown-toggle');
        
        dropdownToggles.forEach(function(toggle) {
          toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const parent = this.closest('.dropdown');
            const dropdownMenu = parent.querySelector('.dropdown-menu');
            
            // Close other dropdowns
            document.querySelectorAll('.td-navbar .dropdown').forEach(function(otherDropdown) {
              if (otherDropdown !== parent) {
                otherDropdown.classList.remove('show');
                const otherMenu = otherDropdown.querySelector('.dropdown-menu');
                if (otherMenu) {
                  otherMenu.classList.remove('show');
                }
              }
            });
            
            // Toggle current dropdown
            parent.classList.toggle('show');
            if (dropdownMenu) {
              dropdownMenu.classList.toggle('show');
            }
          });
        });
      }
    }
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
      const navbar = document.querySelector('.td-navbar');
      const navbarToggler = document.querySelector('.navbar-toggler');
      const navbarCollapse = document.querySelector('#main_navbar');
      
      if (navbar && navbarToggler && navbarCollapse) {
        const isClickInside = navbar.contains(event.target);
        const isTogglerClick = navbarToggler.contains(event.target);
        
        // Close menu if clicking outside (but not on the toggler itself)
        // The toggler has its own handler that will manage open/close
        if (!isClickInside && !isTogglerClick && navbarCollapse.classList.contains('show')) {
          navbarCollapse.classList.remove('show');
          navbarToggler.setAttribute('aria-expanded', 'false');
          
          // Close all dropdowns
          navbarCollapse.querySelectorAll('.dropdown.show').forEach(function(dropdown) {
            dropdown.classList.remove('show');
            const menu = dropdown.querySelector('.dropdown-menu');
            if (menu) {
              menu.classList.remove('show');
            }
          });
        }
      }
    });
    
    // Ensure hamburger toggles the menu properly
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('#main_navbar');
    
    if (navbarToggler && navbarCollapse) {
      // Remove any existing Bootstrap data-bs-toggle behavior and handle manually
      navbarToggler.removeAttribute('data-bs-toggle');
      navbarToggler.removeAttribute('data-bs-target');
      
      navbarToggler.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Simple toggle without Bootstrap's Collapse API
        const isExpanded = navbarCollapse.classList.contains('show');
        
        if (isExpanded) {
          // Close menu
          navbarCollapse.classList.remove('show');
          this.setAttribute('aria-expanded', 'false');
          
          // Close all dropdowns inside
          navbarCollapse.querySelectorAll('.dropdown.show').forEach(function(dropdown) {
            dropdown.classList.remove('show');
            const menu = dropdown.querySelector('.dropdown-menu');
            if (menu) {
              menu.classList.remove('show');
            }
          });
        } else {
          // Open menu
          navbarCollapse.classList.add('show');
          this.setAttribute('aria-expanded', 'true');
        }
      });
    }
    
    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function() {
        // Close mobile menu on resize to desktop
        if (window.innerWidth >= 992) {
          const navbarCollapse = document.querySelector('#main_navbar');
          if (navbarCollapse && navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
          }
          // Reset all dropdowns
          document.querySelectorAll('.dropdown.show').forEach(function(dropdown) {
            dropdown.classList.remove('show');
            const menu = dropdown.querySelector('.dropdown-menu');
            if (menu) {
              menu.classList.remove('show');
            }
          });
        }
        
        // Reinitialize hover/click handlers based on new screen size
        setupDesktopHover();
        setupMobileDropdowns();
      }, 250);
    });
    
    // Initial setup
    setupDesktopHover();
    setupMobileDropdowns();
  });
})();

