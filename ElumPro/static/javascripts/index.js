document.addEventListener('DOMContentLoaded', () => {
    const preloader = document.getElementById('preloader');
    const progressBar = document.getElementById('progress-bar');
    // Select links but exclude external ones or hash anchors
    const navLinks = document.querySelectorAll('a[href]:not([target="_blank"]):not([href^="#"]):not([href^="mailto:"]):not([href^="tel:"])');

    // 10 seconds is much safer than 20, but I'll keep it long as you requested
    const LOAD_TIME = 1000;

    const runLoadingSequence = (callback) => {
        if (!preloader || !progressBar) return;

        // 1. Reset everything instantly
        preloader.style.display = 'flex'; // Ensure it's visible
        preloader.classList.remove('preloader-hidden');
        progressBar.style.transition = 'none';
        progressBar.style.width = '0%';

        // 2. Force reflow
        void progressBar.offsetWidth;

        // 3. Start the visible animation
        progressBar.style.transition = `width ${LOAD_TIME}ms cubic-bezier(0.22, 1, 0.36, 1)`;
        progressBar.style.width = '100%';

        // 4. THE FIX: Explicitly hide after the time is up
        setTimeout(() => {
            if (callback) {
                callback();
            } else {
                // Add the fade-out class
                preloader.classList.add('preloader-hidden');

                // Physical removal from view after fade completes
                setTimeout(() => {
                    preloader.style.display = 'none';
                }, 1000);
            }
        }, LOAD_TIME);
    };

    // Run on initial page load
    runLoadingSequence();

    // Show on link clicks
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const destination = link.href;
            // Prevent double-triggering
            if (destination && destination !== window.location.href) {
                e.preventDefault();
                runLoadingSequence(() => {
                    window.location.href = destination;
                });
            }
        });
    });
});