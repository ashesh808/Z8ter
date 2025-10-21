import { useEffect, useState } from "react";
import { createRoot, type Root } from "react-dom/client";

const Clock: React.FC = () => {
  const [now, setNow] = useState(() => new Date().toLocaleTimeString());

  useEffect(() => {
    const id = window.setInterval(() => {
      setNow(new Date().toLocaleTimeString());
    }, 1000);
    return () => window.clearInterval(id);
  }, []);

  return <span className="badge badge-ghost">{now}</span>;
};

class Z8ClockElement extends HTMLElement {
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
    this.root?.render(<Clock />);
  }
}

if (!customElements.get("z8-clock")) {
  customElements.define("z8-clock", Z8ClockElement);
}
