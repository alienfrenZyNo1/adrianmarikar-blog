document.getElementById('year').textContent = new Date().getFullYear();

const setPointer = (event) => {
  document.documentElement.style.setProperty('--mx', `${event.clientX}px`);
  document.documentElement.style.setProperty('--my', `${event.clientY}px`);
};
window.addEventListener('pointermove', setPointer, { passive: true });
