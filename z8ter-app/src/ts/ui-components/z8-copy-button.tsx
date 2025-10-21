import { useCallback, useEffect, useRef, useState } from "react";
import { createRoot, type Root } from "react-dom/client";

type Props = {
  text?: string;
  label?: string;
  copiedLabel?: string;
};

const DEFAULTS: Required<Props> = {
  text: "pip install -e .",
  label: "Copy install",
  copiedLabel: "Copied!",
};

const CopyButton: React.FC<Props> = ({
  text = DEFAULTS.text,
  label = DEFAULTS.label,
  copiedLabel = DEFAULTS.copiedLabel,
}) => {
  const [currentLabel, setCurrentLabel] = useState(label);
  const timeoutRef = useRef<number | null>(null);

  useEffect(() => {
    setCurrentLabel(label);
  }, [label]);

  useEffect(() => {
    return () => {
      if (timeoutRef.current !== null) {
        window.clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  const handleClick = useCallback(async () => {
    if (timeoutRef.current !== null) {
      window.clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }

    try {
      await navigator.clipboard.writeText(text);
      setCurrentLabel(copiedLabel);
    } catch {
      setCurrentLabel("Copy failed");
    }

    timeoutRef.current = window.setTimeout(() => {
      setCurrentLabel(label);
      timeoutRef.current = null;
    }, 1200);
  }, [text, label, copiedLabel]);

  return (
    <button className="btn btn-sm btn-outline" onClick={handleClick} type="button">
      {currentLabel}
    </button>
  );
};

class Z8CopyButtonElement extends HTMLElement {
  private root: Root | null = null;

  static get observedAttributes(): string[] {
    return ["text", "label", "copiedlabel", "copied-label"];
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
      text: this.getAttributeValue("text") ?? DEFAULTS.text,
      label: this.getAttributeValue("label") ?? DEFAULTS.label,
      copiedLabel:
        this.getAttributeValue("copiedlabel") ??
        this.getAttribute("copied-label") ??
        DEFAULTS.copiedLabel,
    };
  }

  private render(): void {
    this.ensureRoot().render(<CopyButton {...this.getProps()} />);
  }
}

if (!customElements.get("z8-copy-button")) {
  customElements.define("z8-copy-button", Z8CopyButtonElement);
}
