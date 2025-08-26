import { customElement, noShadowDOM } from "solid-element";
import { createSignal, onMount } from "solid-js";
import { applyTheme, getInitialTheme, type Theme } from "@/utils/theme";
customElement("z8-theme-toggle", {}, () => {
  noShadowDOM();
  const [theme, setTheme] = createSignal<Theme>("light");
  onMount(() => { const t = getInitialTheme(); setTheme(t); applyTheme(t); });

  const toggle = () => {
    const next = theme() === "luxury" ? "light" : "luxury";
    setTheme(next); applyTheme(next);
  };

  return (
    <button class="btn btn-sm" onClick={toggle}>
      {theme() === "luxury" ? "Use Light" : "Use Dark"}
    </button>
  );
});
