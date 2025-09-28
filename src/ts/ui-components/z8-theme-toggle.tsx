import { customElement, noShadowDOM } from "solid-element";
import { createSignal, onMount } from "solid-js";
import { applyTheme, getInitialTheme, type Theme } from "@/utils/theme";
customElement("z8-theme-toggle", {}, () => {
  noShadowDOM();
  const [theme, setTheme] = createSignal<Theme>("cooperate");
  onMount(() => { const t = getInitialTheme(); setTheme(t); applyTheme(t); });

  const toggle = () => {
    const next = theme() === "night" ? "cooperate" : "night";
    setTheme(next); 
    applyTheme(next);
  };

  return (
    <button class="btn btn-sm" onClick={toggle}>
      {theme() === "night" ? "Use Light" : "Use Dark"}
    </button>
  );
});
