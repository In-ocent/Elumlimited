document.addEventListener('DOMContentLoaded', () => {
    const preloader = document.getElementById('preloader');
    const progressBar = document.getElementById('progress-bar');
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const backToTopBtn = document.getElementById('backToTop');

    // 1. FASTER LOAD TIME (Change 3000 to 800 for a snappy feel)
    const INITIAL_LOAD = 800;

    // 2. INITIAL PRELOADER (Only runs once when page opens)
    if (preloader && progressBar) {
        progressBar.style.transition = `width ${INITIAL_LOAD}ms ease-out`;
        progressBar.style.width = '100%';

        setTimeout(() => {
            preloader.classList.add('preloader-hidden');
            setTimeout(() => {
                preloader.style.display = 'none';
            }, 1000); // Match your CSS transition time
        }, INITIAL_LOAD);
    }

    // 3. REMOVE THE NAVLINK LISTENER (This was the "disturbing" part)
    // Most professional sites don't force a preloader on every click 
    // because it makes the site feel slow. Let the browser handle page jumps.

    // 4. MOBILE MENU (Optimized for Redmi 10 touch)
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            mobileMenu.classList.toggle('hidden');
            mobileMenu.classList.toggle('flex');
        });

        document.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
            mobileMenu.classList.remove('flex');
        });
    }

    // 5. BACK TO TOP (Throttle for performance)
    window.addEventListener('scroll', () => {
        if (backToTopBtn) {
            if (window.scrollY > 400) {
                backToTopBtn.style.opacity = "1";
                backToTopBtn.style.transform = "translateY(0)";
            } else {
                backToTopBtn.style.opacity = "0";
                backToTopBtn.style.transform = "translateY(40px)";
            }
        }
    }, { passive: true }); // Makes scrolling smoother

    // 6. SCROLL REVEAL (The "Wonder" effect)
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
});