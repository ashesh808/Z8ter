import { useCallback, useEffect, useState } from "react";
import { createRoot, type Root } from "react-dom/client";
import { applyTheme, getInitialTheme, type Theme } from "@/utils/theme";

const ThemeToggle: React.FC = () => {
  const [theme, setTheme] = useState<Theme>("cooperate");

  useEffect(() => {
    const initial = getInitialTheme();
    setTheme(initial);
    applyTheme(initial);
  }, []);

  const toggle = useCallback(() => {
    setTheme((current) => {
      const next = current === "night" ? "cooperate" : "night";
      applyTheme(next);
      return next;
    });
  }, []);

  return (
    <button className="btn btn-sm" onClick={toggle}>
      {theme === "night" ? "Use Light" : "Use Dark"}
    </button>
  );
};

class Z8ThemeToggleElement extends HTMLElement {
  private root: Root | null = null;

  connectedCallback(): void {
    if (!this.root) {
      this.root = createRoot(this);
    }
    this.render();
  }

  disconnectedCallback(): void {
    this.root?.unmount();
    this.root = null;
  }

  private render(): void {
    this.root?.render(<ThemeToggle />);
  }
}

if (!customElements.get("z8-theme-toggle")) {
  customElements.define("z8-theme-toggle", Z8ThemeToggleElement);
}
