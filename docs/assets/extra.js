// Load Google AdSense script
(function() {
  // Only load in production environment (GitHub Pages)
  if (window.location.hostname !== 'localhost' && 
      window.location.hostname !== '127.0.0.1') {
    var ad = document.createElement('script');
    ad.async = true;
    ad.crossOrigin = 'anonymous';
    ad.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7358189775686770';
    var firstScript = document.getElementsByTagName('script')[0];
    firstScript.parentNode.insertBefore(ad, firstScript);
  }
})();

// Google Analytics Opt-In
document.addEventListener('DOMContentLoaded', function() {
  var consent = document.querySelector('.md-consent');
  if (consent) {
    console.log('Cookie consent banner detected');
  }
});

// Custom JavaScript for Unraid API Documentation

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Hide "Home" text in the header topic
  const headerTopicElement = document.querySelector('.md-header__topic[data-md-component="header-topic"] span');
  if (headerTopicElement && headerTopicElement.textContent.trim() === 'Home') {
    headerTopicElement.style.display = 'none';
  }
}); 