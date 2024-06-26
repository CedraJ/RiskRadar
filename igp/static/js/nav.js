document.addEventListener("DOMContentLoaded", function() {
    const navLinks = document.querySelectorAll('.header nav ul li a');
    const currentPath = window.location.pathname; 
    
    navLinks.forEach(link => {
      if (link.href.includes(currentPath)) {
        link.classList.add('active'); 
      }
    });
  });