(function () {
  const qs = (sel, ctx = document) => ctx.querySelector(sel);
  const qsa = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  document.addEventListener('DOMContentLoaded', () => {
    // Flash messages fade out after a delay
    const flashes = qsa('.flash-message');
    if (flashes.length) {
      setTimeout(() => {
        flashes.forEach(msg => {
          msg.style.transition = 'opacity 0.4s ease';
          msg.style.opacity = '0';
          setTimeout(() => msg.remove(), 400);
        });
      }, 3000);
    }

    // Drawer toggle
    const menuToggle = qs('#menuToggle');
    const drawer = qs('#mainDrawer');
    const closeDrawer = qs('#drawerClose');
    const backdrop = qs('#drawerBackdrop');

    const toggleDrawer = (forceOpen) => {
      const willOpen = forceOpen !== undefined ? forceOpen : !drawer.classList.contains('is-open');
      drawer.classList.toggle('is-open', willOpen);
      backdrop.classList.toggle('is-visible', willOpen);
      menuToggle?.setAttribute('aria-expanded', String(willOpen));
      drawer?.setAttribute('aria-hidden', String(!willOpen));
    };

    menuToggle?.addEventListener('click', () => toggleDrawer());
    closeDrawer?.addEventListener('click', () => toggleDrawer(false));
    backdrop?.addEventListener('click', () => toggleDrawer(false));

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && drawer.classList.contains('is-open')) {
        toggleDrawer(false);
      }
    });

    // Hero slider logic
    const slider = qs('#heroSlider');
    if (slider) {
      const slides = qsa('.hero-slide', slider);
      const nextBtn = qs('[data-direction="next"]', slider);
      const prevBtn = qs('[data-direction="prev"]', slider);
      let current = slides.findIndex(slide => slide.classList.contains('is-active'));
      if (current < 0) current = 0;
      let timer;

      const activate = (index) => {
        slides.forEach((slide, idx) => {
          slide.classList.toggle('is-active', idx === index);
        });
        current = index;
      };

      const next = () => activate((current + 1) % slides.length);
      const prev = () => activate((current - 1 + slides.length) % slides.length);

      const startAuto = () => {
        clearInterval(timer);
        timer = setInterval(next, 6000);
      };

      nextBtn?.addEventListener('click', () => {
        next();
        startAuto();
      });
      prevBtn?.addEventListener('click', () => {
        prev();
        startAuto();
      });

      if (slides.length > 1) {
        startAuto();
      }
    }

    // Reveal animation for product cards
    qsa('.product-card').forEach((card, index) => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(12px)';
      setTimeout(() => {
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, 100 * index);
    });
  });
})();
