import { customElement, noShadowDOM } from "solid-element";
import { createSignal } from "solid-js";

type Props = { text?: string; label?: string; copiedLabel?: string };
customElement<Props>("z8-copy-button",
  { text: "pip install -e .", label: "Copy install", copiedLabel: "Copied!" },
  (p) => {
    noShadowDOM();
    const [label, setLabel] = createSignal(p.label!);
    const click = async () => {
      try { await navigator.clipboard.writeText(p.text!); setLabel(p.copiedLabel!); }
      catch { setLabel("Copy failed"); }
      setTimeout(() => setLabel(p.label!), 1200);
    };
    return <button class="btn btn-sm btn-outline" onClick={click}>{label()}</button>;
  }
);
