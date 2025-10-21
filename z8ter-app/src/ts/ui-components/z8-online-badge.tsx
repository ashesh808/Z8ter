import { useEffect, useState } from "react";
import { createRoot, type Root } from "react-dom/client";

const OnlineBadge: React.FC = () => {
  const [online, setOnline] = useState(() =>
    typeof navigator !== "undefined" ? navigator.onLine : true
  );

  useEffect(() => {
    const handleOnline = () => setOnline(true);
    const handleOffline = () => setOnline(false);
    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return (
    <span className={`badge ${online ? "badge-success" : "badge-error"}`}>
      {online ? "Online" : "Offline"}
    </span>
  );
};

class Z8OnlineBadgeElement extends HTMLElement {
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
    this.root?.render(<OnlineBadge />);
  }
}

if (!customElements.get("z8-online-badge")) {
  customElements.define("z8-online-badge", Z8OnlineBadgeElement);
}
