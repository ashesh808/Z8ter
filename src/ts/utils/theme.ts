export type Theme = "cooperate" | "night";
const THEME_KEY = "z8_theme";

export function applyTheme(theme: Theme) {
  document.documentElement.setAttribute("data-theme", theme);
  try { localStorage.setItem(THEME_KEY, theme); } catch {}
}

export function getInitialTheme(): Theme {
  try {
    const t = localStorage.getItem(THEME_KEY);
    if (t === "cooperate" || t === "night") return t;
  } catch {}
  const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
  return prefersDark ? "cooperate" : "night";
}
