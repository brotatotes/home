const buttons = [...document.querySelectorAll('.theme-button')];
const themeColor = document.querySelector('meta[name="theme-color"]');
const systemDark = window.matchMedia('(prefers-color-scheme: dark)');

function resolvedTheme(theme) {
  return theme === 'system' ? (systemDark.matches ? 'dark' : 'light') : theme;
}

function applyTheme(theme) {
  const resolved = resolvedTheme(theme);
  document.body.dataset.theme = resolved === 'dark' ? 'dark' : '';
  themeColor?.setAttribute('content', resolved === 'dark' ? '#0d1117' : '#f2ecdf');
  buttons.forEach((button) => {
    const active = button.dataset.theme === theme;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  try { localStorage.setItem('home-theme', theme); } catch (error) { /* optional */ }
}

buttons.forEach((button) => button.addEventListener('click', () => applyTheme(button.dataset.theme)));
systemDark.addEventListener('change', () => {
  if (document.querySelector('.theme-button.active')?.dataset.theme === 'system') applyTheme('system');
});

let saved = 'system';
try { saved = localStorage.getItem('home-theme') || localStorage.getItem('atlas-theme') || 'system'; } catch (error) { /* optional */ }
if (saved === 'atlas') saved = 'light';
applyTheme(['system', 'light', 'dark'].includes(saved) ? saved : 'system');
