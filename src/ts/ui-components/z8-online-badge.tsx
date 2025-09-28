import { customElement, noShadowDOM } from "solid-element";
import { createSignal, onCleanup, onMount } from "solid-js";

customElement("z8-online-badge", {}, () => {
  noShadowDOM();
  const [online, setOnline] = createSignal(typeof navigator !== "undefined" ? navigator.onLine : true);
  const up = () => setOnline(true), down = () => setOnline(false);
  onMount(() => { window.addEventListener("online", up); window.addEventListener("offline", down); });
  onCleanup(() => { window.removeEventListener("online", up); window.removeEventListener("offline", down); });
  return <span class={"badge " + (online() ? "badge-success" : "badge-error")}>{online() ? "Online" : "Offline"}</span>;
});
