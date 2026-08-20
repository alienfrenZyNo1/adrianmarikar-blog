const year = document.getElementById('year');
if (year) {
  year.textContent = new Date().getFullYear();
}

const setPointer = (event) => {
  document.documentElement.style.setProperty('--mx', `${event.clientX}px`);
  document.documentElement.style.setProperty('--my', `${event.clientY}px`);
};
window.addEventListener('pointermove', setPointer, { passive: true });

const navMenu = document.querySelector('.nav-menu');
const mobileNavQuery = window.matchMedia('(max-width: 1050px)');

const syncNavForViewport = () => {
  if (!navMenu) return;
  if (mobileNavQuery.matches) {
    navMenu.removeAttribute('open');
  } else {
    navMenu.setAttribute('open', '');
  }
};

syncNavForViewport();
if (typeof mobileNavQuery.addEventListener === 'function') {
  mobileNavQuery.addEventListener('change', syncNavForViewport);
} else {
  mobileNavQuery.addListener(syncNavForViewport);
}

if (navMenu) {
  navMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      if (mobileNavQuery.matches) navMenu.removeAttribute('open');
    });
  });

  document.addEventListener('pointerdown', (event) => {
    if (mobileNavQuery.matches && navMenu.open && !navMenu.contains(event.target)) {
      navMenu.removeAttribute('open');
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && mobileNavQuery.matches && navMenu.open) {
      navMenu.removeAttribute('open');
      navMenu.querySelector('summary')?.focus();
    }
  });
}

const updateAnchorOffset = () => {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const headerHeight = Math.ceil(header.getBoundingClientRect().height);
  const gap = window.matchMedia('(max-width: 640px)').matches ? 12 : 16;
  document.documentElement.style.setProperty('--anchor-offset', `${headerHeight + gap}px`);
};

updateAnchorOffset();
window.addEventListener('resize', updateAnchorOffset, { passive: true });
window.addEventListener('orientationchange', updateAnchorOffset, { passive: true });

if ('ResizeObserver' in window) {
  const header = document.querySelector('.site-header');
  if (header) {
    new ResizeObserver(updateAnchorOffset).observe(header);
  }
}
