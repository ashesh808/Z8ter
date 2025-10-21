import { useCallback, useEffect, useState } from "react";
import { createRoot, type Root } from "react-dom/client";

type Props = {
  storageKey?: string;
  label?: string;
};

const DEFAULTS: Required<Props> = {
  storageKey: "z8_island_pref",
  label: "Remember I like islands",
};

const IslandPref: React.FC<Props> = ({
  storageKey = DEFAULTS.storageKey,
  label = DEFAULTS.label,
}) => {
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    try {
      setChecked(localStorage.getItem(storageKey) === "1");
    } catch {
      setChecked(false);
    }
  }, [storageKey]);

  const handleChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const next = event.currentTarget.checked;
      setChecked(next);
      try {
        localStorage.setItem(storageKey, next ? "1" : "0");
      } catch {
        // Ignore storage errors
      }
    },
    [storageKey]
  );

  return (
    <label className="label cursor-pointer mt-2">
      <span className="label-text">{label}</span>
      <input
        type="checkbox"
        className="toggle toggle-primary"
        checked={checked}
        onChange={handleChange}
      />
    </label>
  );
};

class Z8IslandPrefElement extends HTMLElement {
  private root: Root | null = null;

  static get observedAttributes(): string[] {
    return ["storagekey", "label"];
  }

  connectedCallback(): void {
    this.ensureRoot();
    this.render();
  }

  disconnectedCallback(): void {
    this.root?.unmount();
    this.root = null;
  }

  attributeChangedCallback(): void {
    if (this.isConnected) {
      this.render();
    }
  }

  private ensureRoot(): Root {
    if (!this.root) {
      this.root = createRoot(this);
    }
    return this.root;
  }

  private getAttributeValue(name: string): string | null {
    return this.getAttribute(name) ?? this.getAttribute(name.toLowerCase());
  }

  private getProps(): Props {
    return {
      storageKey: this.getAttributeValue("storagekey") ?? DEFAULTS.storageKey,
      label: this.getAttributeValue("label") ?? DEFAULTS.label,
    };
  }

  private render(): void {
    this.ensureRoot().render(<IslandPref {...this.getProps()} />);
  }
}

if (!customElements.get("z8-island-pref")) {
  customElements.define("z8-island-pref", Z8IslandPrefElement);
}
