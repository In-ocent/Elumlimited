document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.slider-img');
    const indicator = document.getElementById('slide-indicator');
    let currentIndex = 0;

    function nextSlide() {
        // Hide current image
        images[currentIndex].classList.replace('opacity-100', 'opacity-0');

        // Move to next index
        currentIndex = (currentIndex + 1) % images.length;

        // Show next image
        images[currentIndex].classList.replace('opacity-0', 'opacity-100');

        // Update indicator text
        if (indicator) {
            indicator.innerText = `0${currentIndex + 1} / 0${images.length}`;
        }
    }

    // Change slide every 5 seconds
    setInterval(nextSlide, 5000);
});