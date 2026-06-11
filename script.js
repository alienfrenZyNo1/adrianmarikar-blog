const year = document.getElementById('year');
if (year) {
  year.textContent = new Date().getFullYear();
}

const setPointer = (event) => {
  document.documentElement.style.setProperty('--mx', `${event.clientX}px`);
  document.documentElement.style.setProperty('--my', `${event.clientY}px`);
};
window.addEventListener('pointermove', setPointer, { passive: true });

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
