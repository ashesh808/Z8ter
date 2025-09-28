import { customElement, noShadowDOM} from "solid-element";
import { createSignal, onCleanup, onMount } from "solid-js";

customElement("z8-clock", {}, () => {
  noShadowDOM();
  const [now, setNow] = createSignal(new Date().toLocaleTimeString());
  let id: number | undefined;
  onMount(() => { id = window.setInterval(() => setNow(new Date().toLocaleTimeString()), 1000); });
  onCleanup(() => { if (id) clearInterval(id); });
  return <span class="badge badge-ghost">{now()}</span>;
});
