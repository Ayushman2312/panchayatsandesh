document.querySelector('.menu-toggle').addEventListener('click', function() {
    const navLinks = document.querySelector('.mobile-nav');
    
    if (navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
        navLinks.style.maxHeight = '0';
        navLinks.style.opacity = '0';
    } else {
        navLinks.classList.add('active');
        navLinks.style.maxHeight = navLinks.scrollHeight + 'px';
        navLinks.style.opacity = '1';
    }
});
//scrolling-section
const scrollingContent = document.querySelector('.scrolling-content');
            let d = 0;

            function scroll() {
                d += 1; // Adjust the speed of scrolling here
                scrollingContent.style.transform = `translateX(-${d}px)`;

                // Reset scroll when the content is completely out of view
                if (d > scrollingContent.scrollWidth) {
                    d = 0;
                }

                requestAnimationFrame(scroll);
            }

            scroll();
// latest-lifestyle-post
const carousel = document.getElementById('carousel');
        let scrollAmount = 0;

        function autoScroll() {
            const maxScrollLeft = carousel.scrollWidth - carousel.clientWidth;
            if (scrollAmount < maxScrollLeft) {
                scrollAmount += carousel.clientWidth;
            } else {
                scrollAmount = 0;
            }
            carousel.scrollTo({
                left: scrollAmount,
                behavior: 'smooth'
            });
        }

setInterval(autoScroll, 3000); // Scrolls every 3 seconds

// donation
// function openUPI(){
//     var amount = document.getElementById("amount").value;
//     var name = document.getElementById("name").value;
//     var mobile = document.getElementById("mobile").value;
//     var email = document.getElementById("email").value;
    
//     UPI URL scheme
//     var upiLink = `upi://pay?pa=ayushman4678@ibl&pn=${name}&am=${amount}&cu=INR`;

//     Open UPI link
//     window.location.href = upiLink;
// }

//jj
function isMobileDevice() {
    return /Mobi|Android/i.test(navigator.userAgent);
}

function openUPI() {
    var name = document.getElementById("name").value;
    var mobile = document.getElementById("mobile").value;
    var email = document.getElementById("email").value;
    var amount = document.getElementById("amount").value;
    
    // Validation for form fields
    if (!name || !mobile || !email || !amount) {
        alert('Please fill in all fields.');
        return false;
    }

    // UPI URL with user input values
    var upiLink = `upi://pay?pa=ayushman4678@ibl&pn=${name}&am=${amount}&cu=INR`;

    // Check if user is on a mobile device
    if (isMobileDevice()) {
        // Redirect to the UPI link (PhonePe app)
        window.location.href = upiLink;
    } else {
        // Display a message for desktop users
        alert('UPI payments only work on mobile devices. Please complete this payment on your mobile.');
    }

    return false; // Prevent form submission
}