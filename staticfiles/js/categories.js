document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.category-card');

    cards.forEach((card, index) => {
        const news = [
            { title: "Trending News Title 1", description: "This is a sample description 1..." },
            { title: "Trending News Title 2", description: "Another interesting news piece..." },
            { title: "Trending News Title 3", description: "Yet another news piece..." }
        ];

        let currentNewsIndex = 0;

        setInterval(() => {
            currentNewsIndex = (currentNewsIndex + 1) % news.length;
            card.querySelector('.news-title').innerText = news[currentNewsIndex].title;
            card.querySelector('.news-description').innerText = news[currentNewsIndex].description;
        }, 3000);
    });
});
