import { customElement, noShadowDOM} from "solid-element";
import { createSignal, onMount } from "solid-js";

type Props = { storageKey?: string; label?: string };
customElement<Props>("z8-island-pref", { storageKey: "z8_island_pref", label: "Remember I like islands" }, (p) => {
  noShadowDOM();
  const [checked, setChecked] = createSignal(false);
  onMount(() => { try { setChecked(localStorage.getItem(p.storageKey!) === "1"); } catch {} });
  const onChange = (e: Event) => {
    const v = (e.currentTarget as HTMLInputElement).checked;
    setChecked(v); try { localStorage.setItem(p.storageKey!, v ? "1" : "0"); } catch {}
  };
  return (
    <label class="label cursor-pointer mt-2">
      <span class="label-text">{p.label}</span>
      <input type="checkbox" class="toggle toggle-primary" checked={checked()} onChange={onChange} />
    </label>
  );
});
