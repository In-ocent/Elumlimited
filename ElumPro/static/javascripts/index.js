document.addEventListener('DOMContentLoaded', () => {
    // --- 1. ELEMENT SELECTIONS ---
    const preloader = document.getElementById('preloader');
    const progressBar = document.getElementById('progress-bar');
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    const backToTopBtn = document.getElementById('backToTop');

    // Select internal links only (skip external, email, and phone)
    const navLinks = document.querySelectorAll('a[href]:not([target="_blank"]):not([href^="#"]):not([href^="mailto:"]):not([href^="tel:"])');

    // Setting this to 15 seconds as you wanted for that "Premium" feel
    const LOAD_TIME = 3000;

    // --- 2. PRELOADER & PAGE TRANSITION LOGIC ---
    const runLoadingSequence = (callback) => {
        if (!preloader || !progressBar) return;

        // Reset state
        preloader.style.display = 'flex';
        preloader.classList.remove('preloader-hidden');
        progressBar.style.transition = 'none';
        progressBar.style.width = '0%';

        void progressBar.offsetWidth; // Force Reflow

        // Start filling the bar
        progressBar.style.transition = `width ${LOAD_TIME}ms cubic-bezier(0.1, 0, 0.1, 1)`;
        progressBar.style.width = '100%';

        setTimeout(() => {
            // Start the smooth fade out
            preloader.classList.add('preloader-hidden');

            setTimeout(() => {
                if (callback) {
                    callback(); // Redirect to new page
                } else {
                    preloader.style.display = 'none'; // Simply hide on current page
                }
            }, 1200); // Wait for the 1.2s CSS fade transition
        }, LOAD_TIME);
    };

    // Run on first load
    runLoadingSequence();

    // Attach to internal navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const destination = link.href;
            if (destination && destination !== window.location.href) {
                e.preventDefault();
                runLoadingSequence(() => {
                    window.location.href = destination;
                });
            }
        });
    });

    // --- 3. MOBILE MENU TOGGLE ---
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isHidden = mobileMenu.classList.toggle('hidden');
            mobileMenu.classList.toggle('flex', !isHidden);

            if (menuIcon) {
                menuIcon.style.transform = isHidden ? 'rotate(0deg)' : 'rotate(90deg)';
            }
        });

        // Close menu when clicking anywhere else on the screen
        document.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
            mobileMenu.classList.remove('flex');
            if (menuIcon) menuIcon.style.transform = 'rotate(0deg)';
        });
    }

    // --- 4. BACK TO TOP BUTTON ---
    window.addEventListener('scroll', () => {
        if (backToTopBtn) {
            if (window.scrollY > 400) {
                backToTopBtn.classList.remove('opacity-0', 'translate-y-10');
                backToTopBtn.classList.add('opacity-100', 'translate-y-0');
            } else {
                backToTopBtn.classList.add('opacity-0', 'translate-y-10');
                backToTopBtn.classList.remove('opacity-100', 'translate-y-0');
            }
        }
    });

    // --- 5. SCROLL REVEAL (Intersection Observer) ---
    const revealOptions = { threshold: 0.15 };
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, revealOptions);

    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
});