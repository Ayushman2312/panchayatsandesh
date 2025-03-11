function toggleSearchPopup() {
    const popup = document.getElementById('searchPopup');
    popup.classList.toggle('hidden');
}

document.addEventListener('DOMContentLoaded', function() {
    const scrollContainer = document.getElementById('scrollContainer');
    let scrollPosition = 0;
    const speed = 1; // Adjust speed as needed

    function animate() {
        scrollPosition -= speed;
        
        // Reset position when first set of images is fully scrolled
        if (scrollPosition <= -scrollContainer.children[0].offsetWidth) {
            scrollPosition = 0;
        }
        
        scrollContainer.style.transform = `translateX(${scrollPosition}px)`;
        requestAnimationFrame(animate);
    }

    animate();
});
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.news-container');
    const items = document.querySelectorAll('.news-item');
    const dotsContainer = document.getElementById('news-dots');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    if (!items.length) return;

    let currentIndex = 0;
    let autoScrollInterval;
    
    // Create navigation dots
    items.forEach((_, index) => {
        const dot = document.createElement('button');
        dot.classList.add('w-3', 'h-3', 'rounded-full', 'bg-[#d8982e]', 'opacity-50', 'transition-opacity', 'hover:opacity-75');
        dot.setAttribute('aria-label', `Go to slide ${index + 1}`);
        dot.addEventListener('click', () => {
            goToSlide(index);
            resetInterval();
        });
        dotsContainer.appendChild(dot);
    });

    const dots = dotsContainer.querySelectorAll('button');
    
    function updateDots() {
        dots.forEach((dot, index) => {
            dot.classList.toggle('opacity-100', index === currentIndex);
            dot.classList.toggle('opacity-50', index !== currentIndex);
        });
    }

    function goToSlide(index) {
        currentIndex = index;
        const offset = currentIndex * (100 / items.length);
        container.style.transform = `translateX(-${offset}%)`;
        updateDots();
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % items.length;
        goToSlide(currentIndex);
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        goToSlide(currentIndex);
    }

    function startAutoScroll() {
        if (autoScrollInterval) {
            clearInterval(autoScrollInterval);
        }
        autoScrollInterval = setInterval(() => {
            nextSlide();
        }, 5000);
    }

    function resetInterval() {
        clearInterval(autoScrollInterval);
        startAutoScroll();
    }

    // Event listeners for navigation buttons
    nextBtn.addEventListener('click', () => {
        nextSlide();
        resetInterval();
    });

    prevBtn.addEventListener('click', () => {
        prevSlide();
        resetInterval();
    });

    // Initialize first slide and dots
    goToSlide(0);
    
    // Start auto scroll immediately
    startAutoScroll();

    // Pause auto scroll on hover
    container.addEventListener('mouseenter', () => {
        clearInterval(autoScrollInterval);
    });

    container.addEventListener('mouseleave', () => {
        startAutoScroll();
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            prevSlide();
            resetInterval();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
            resetInterval();
        }
    });

    // Handle visibility change
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            clearInterval(autoScrollInterval);
        } else {
            startAutoScroll();
        }
    });
});

function openModal(name, designation, description, imageUrl) {
    document.getElementById('modalName').textContent = name;
    document.getElementById('modalDesignation').textContent = designation;
    document.getElementById('modalDescription').textContent = description;
    document.getElementById('modalImage').src = imageUrl;
    document.getElementById('modalImage').alt = name;
    document.getElementById('memberModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    document.getElementById('memberModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
}

// Close modal on escape key press
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Close modal when clicking outside
document.getElementById('memberModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});

// Horizontal scroll functionality
const scrollLeftBtn = document.getElementById('scrollLeftBtn');
const scrollRightBtn = document.getElementById('scrollRightBtn');
const teamContainer = document.getElementById('teamContainer');

if (scrollLeftBtn && scrollRightBtn && teamContainer) {
    scrollLeftBtn.addEventListener('click', () => {
        teamContainer.scrollBy({
            left: -300,
            behavior: 'smooth'
        });
    });

    scrollRightBtn.addEventListener('click', () => {
        teamContainer.scrollBy({
            left: 300,
            behavior: 'smooth'
        });
    });
}