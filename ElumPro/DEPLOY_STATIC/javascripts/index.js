document.addEventListener("DOMContentLoaded", () => {
    // --- 1. Mobile Menu Logic ---
    const btn = document.getElementById("menu-btn");
    const menu = document.getElementById("mobile-menu");
    const icon = document.getElementById("menu-icon");

    btn?.addEventListener("click", () => {
        menu.classList.toggle("hidden");
        menu.classList.toggle("flex");

        icon.innerHTML = menu.classList.contains("hidden")
            ? `<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />`
            : `<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />`;
    });

    // --- 2. Navbar Active State ---
    const sections = document.querySelectorAll('section[id]');
    if (sections.length > 0) {
        const observerOptions = { root: null, rootMargin: '-20% 0px -70% 0px', threshold: 0 };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    document.querySelectorAll('.nav-link').forEach(link => {
                        link.classList.remove('text-[#46B4B1]', 'font-bold');
                        link.classList.add('text-gray-400');
                    });
                    const activeLink = document.querySelector(`.nav-link[href="#${id}"]`);
                    if (activeLink) activeLink.classList.add('text-[#46B4B1]', 'font-bold');
                }
            });
        }, observerOptions);
        sections.forEach((section) => observer.observe(section));
    }

    // --- 3. Preloader Logic ---
    const preloader = document.getElementById('preloader');
    const progressBar = document.getElementById('progress-bar');

    function closePreloader() {
        if (progressBar) progressBar.style.width = '100%';
        setTimeout(() => {
            if (preloader) {
                preloader.classList.add('preloader-hidden');
                setTimeout(() => preloader.style.display = 'none', 700);
            }
        }, 800);
    }

    window.addEventListener('load', closePreloader);
    setTimeout(closePreloader, 4000); // Safety timeout

    // --- 4. Back to Top Button ---
    const backToTopBtn = document.getElementById('backToTop');
    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                backToTopBtn.classList.remove('opacity-0', 'translate-y-10', 'pointer-events-none');
                backToTopBtn.classList.add('opacity-100', 'translate-y-0');
            } else {
                backToTopBtn.classList.add('opacity-0', 'translate-y-10', 'pointer-events-none');
                backToTopBtn.classList.remove('opacity-100', 'translate-y-0');
            }
        });
    }

    // --- 5. Booking Page Logic (DYNAMIC) ---
    const dateInput = document.getElementById('booking_date');
    if (dateInput) {
        const slotsContainer = document.getElementById('slots_container');
        const slotSection = document.getElementById('slot-section');
        const confirmBtn = document.getElementById('confirm_btn');
        const slotHidden = document.getElementById('selected_slot');

        dateInput.addEventListener('change', function () {
            slotSection.classList.remove('hidden');
            slotsContainer.innerHTML = '<p class="col-span-3 text-[#46B4B1] animate-pulse">Checking...</p>';

            fetch(`/get-slots/?date=${this.value}`)
                .then(res => res.json())
                .then(data => {
                    slotsContainer.innerHTML = '';
                    data.slots.forEach(slot => {
                        const b = document.createElement('button');
                        b.type = "button";
                        b.innerText = slot;
                        b.className = "py-3 border border-gray-800 rounded-lg hover:border-[#46B4B1] transition-all";
                        b.onclick = () => {
                            document.querySelectorAll('#slots_container button').forEach(el => el.classList.remove('bg-[#46B4B1]'));
                            b.classList.add('bg-[#46B4B1]');
                            slotHidden.value = slot;
                            confirmBtn.disabled = false;
                            confirmBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                        };
                        slotsContainer.appendChild(b);
                    });
                });
        });

        confirmBtn.onclick = function () {
            const formData = new FormData();
            formData.append('full_name', document.getElementById('full_name').value);
            formData.append('email', document.getElementById('email').value);
            formData.append('date', dateInput.value);
            formData.append('slot', slotHidden.value);
            formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

            fetch('/book-session/', { method: 'POST', body: formData })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        document.getElementById('booking-form').classList.add('hidden');
                        document.getElementById('success-ui').classList.remove('hidden');
                    }
                });
        };
    }
});