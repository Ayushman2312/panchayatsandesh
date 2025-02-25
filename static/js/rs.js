document.addEventListener('DOMContentLoaded', function() {
    let timeLeft = 5;
    const countdownElement = document.getElementById('countdown');

    const countdownInterval = setInterval(function() {
        countdownElement.textContent = timeLeft;
        timeLeft--;

        if (timeLeft < 0) {
            clearInterval(countdownInterval);
            window.location.href = "/upcoming-events";
        }
    }, 1000);
});