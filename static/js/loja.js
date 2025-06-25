document.addEventListener('DOMContentLoaded', function () {
  const flashes = document.querySelectorAll('.flash-message');
  if (flashes.length) {
    setTimeout(() => {
      flashes.forEach(el => {
        el.classList.add('fade-out');
        setTimeout(() => el.remove(), 500);
      });
    }, 3000);
  }

  // reveal product cards with a staggered effect
  const produtos = document.querySelectorAll('.produto');
  produtos.forEach((card, idx) => {
    setTimeout(() => card.classList.add('reveal'), idx * 100);
  });
});
