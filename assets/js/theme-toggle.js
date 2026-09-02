/*!
 * Dark / Light Mode Switcher for Apache Kafka Site
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'theme';

  const getStoredTheme = () => localStorage.getItem(STORAGE_KEY);
  const setStoredTheme = (theme) => localStorage.setItem(STORAGE_KEY, theme);

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme();
    if (storedTheme) {
      return storedTheme;
    }
    return 'auto';
  };

  const getEffectiveTheme = (theme) => {
    if (theme === 'auto') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return theme;
  };

  const setTheme = (theme) => {
    const effectiveTheme = getEffectiveTheme(theme);
    document.documentElement.setAttribute('data-bs-theme', effectiveTheme);
    document.documentElement.setAttribute('data-theme-setting', theme);
    
    // Also update class for backward compatibility or direct CSS hooks
    if (effectiveTheme === 'dark') {
      document.documentElement.classList.add('theme-dark');
      document.documentElement.classList.remove('theme-light');
    } else {
      document.documentElement.classList.add('theme-light');
      document.documentElement.classList.remove('theme-dark');
    }
  };

  const updateToggleUI = (theme) => {
    const themeToggles = document.querySelectorAll('[data-bs-theme-value]');
    const activeIcons = document.querySelectorAll('.theme-toggle-active-icon');
    const effectiveTheme = getEffectiveTheme(theme);

    // Update icons
    activeIcons.forEach((icon) => {
      if (theme === 'light') {
        icon.className = 'theme-toggle-active-icon fa-solid fa-sun';
      } else if (theme === 'dark') {
        icon.className = 'theme-toggle-active-icon fa-solid fa-moon';
      } else {
        // Auto mode
        icon.className = 'theme-toggle-active-icon fa-solid fa-circle-half-stroke';
      }
    });

    // Update active checkmarks in dropdown menus
    themeToggles.forEach((element) => {
      const value = element.getAttribute('data-bs-theme-value');
      const isSelected = value === theme;
      element.classList.toggle('active', isSelected);
      element.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
      
      const checkIcon = element.querySelector('.theme-check-icon');
      if (checkIcon) {
        checkIcon.classList.toggle('d-none', !isSelected);
      }
    });

    // Dispatch custom event for any listeners (e.g., charts or external widgets)
    document.dispatchEvent(new CustomEvent('themeChanged', {
      detail: { theme: theme, effectiveTheme: effectiveTheme }
    }));
  };

  // Set initial theme as early as possible
  const currentTheme = getPreferredTheme();
  setTheme(currentTheme);

  // Listen for OS system theme change if in 'auto' mode
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const storedTheme = getStoredTheme();
    if (!storedTheme || storedTheme === 'auto') {
      setTheme('auto');
      updateToggleUI('auto');
    }
  });

  // Attach event listeners when DOM is ready
  window.addEventListener('DOMContentLoaded', () => {
    const preferredTheme = getPreferredTheme();
    updateToggleUI(preferredTheme);

    // Bind click events on all theme switcher options
    document.querySelectorAll('[data-bs-theme-value]').forEach((toggle) => {
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const theme = toggle.getAttribute('data-bs-theme-value');
        setStoredTheme(theme);
        setTheme(theme);
        updateToggleUI(theme);
      });
    });
  });
})();

