// get current year
(function () {
    var yearEl = document.querySelector("#currentYear");
    if (yearEl) {
        yearEl.innerHTML = new Date().getFullYear();
    }
})();

// Flip cards: tap/keyboard toggle (mobile + a11y)
(function () {
    var cards = document.querySelectorAll(".service-flip");
    if (!cards.length) return;

    function flipCard(card) {
        var isOpen = card.classList.contains("is-flipped");
        cards.forEach(function (el) {
            el.classList.remove("is-flipped");
        });
        if (!isOpen) {
            card.classList.add("is-flipped");
        }
    }

    cards.forEach(function (card) {
        card.addEventListener("click", function () {
            flipCard(card);
        });

        card.addEventListener("keydown", function (event) {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                flipCard(card);
            }
        });
    });
})();
