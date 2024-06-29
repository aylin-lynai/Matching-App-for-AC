let currentCard = 0;
const cards = document.querySelectorAll('.card');

function showCard() {
    cards.forEach(card => {
        card.style.opacity = '0'; // 全部卡片设置为不可见
    });
    cards[currentCard].style.opacity = '1'; // 只显示当前卡片

    currentCard = (currentCard + 1) % cards.length; // 更新当前卡片索引，循环显示
}


showCard();

setInterval(showCard, 3000);


