document$.subscribe(function() {
  const checkboxes = document.querySelectorAll('.md-typeset input[type="checkbox"]');
  const path = window.location.pathname;

  checkboxes.forEach((checkbox, index) => {
    // Enable the checkbox
    checkbox.disabled = false;
    
    // Create a unique ID for storage
    const storageKey = `recipe-wiki:${path}:${index}`;

    // Load saved state
    const savedState = localStorage.getItem(storageKey);
    if (savedState === 'true') {
      checkbox.checked = true;
      checkbox.parentElement.classList.add('task-list-item-checked'); // Visual styling if needed
    }

    // Add click listener
    checkbox.addEventListener('change', function() {
      localStorage.setItem(storageKey, this.checked);
      
      // Update parent class for strike-through styling if the theme supports it
      if (this.checked) {
          this.parentElement.classList.add('task-list-item-checked');
      } else {
          this.parentElement.classList.remove('task-list-item-checked');
      }
    });
  });
});
