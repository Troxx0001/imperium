document.addEventListener('DOMContentLoaded', function () {
  const flashes = document.querySelectorAll('.flash-message');
  if (flashes.length) {
    setTimeout(() => {
      flashes.forEach(el => el.style.display = 'none');
    }, 3000);
  }
});
