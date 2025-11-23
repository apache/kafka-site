/**
 * Pause YouTube videos when carousel slides change
 * This prevents multiple videos from playing simultaneously
 */
(function() {
  'use strict';

  // Function to pause a YouTube video by iframe
  function pauseYouTubeVideo(iframe) {
    if (!iframe) return;
    
    try {
      // Method 1: Use postMessage API (works with enablejsapi=1)
      iframe.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
    } catch (e) {
      // Method 2: If postMessage fails, reload iframe src to stop playback
      try {
        const src = iframe.src;
        iframe.src = src.split('?')[0] + '?enablejsapi=1';
      } catch (e2) {
        console.warn('Could not pause YouTube video:', e2);
      }
    }
  }

  // Function to pause all YouTube videos in a carousel
  function pauseAllVideosInCarousel(carouselElement) {
    const iframes = carouselElement.querySelectorAll('iframe[src*="youtube.com"], iframe[src*="youtu.be"]');
    iframes.forEach(function(iframe) {
      pauseYouTubeVideo(iframe);
    });
  }

  // Initialize when DOM is ready
  function init() {
    // Find all carousels on the page
    const carousels = document.querySelectorAll('.carousel');
    
    carousels.forEach(function(carousel) {
      // Listen for Bootstrap carousel slide events
      carousel.addEventListener('slide.bs.carousel', function(event) {
        // Pause all videos in the carousel before sliding
        pauseAllVideosInCarousel(carousel);
      });
      
      carousel.addEventListener('slid.bs.carousel', function(event) {
        // Also pause after slide completes (in case any started during transition)
        pauseAllVideosInCarousel(carousel);
      });
    });
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    // DOM is already ready
    init();
  }
})();

