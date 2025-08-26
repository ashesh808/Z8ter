export default function initIndex(): void {
  const btn = document.getElementById("try-api") as HTMLButtonElement | null;
  const out = document.getElementById("api-response") as HTMLElement | null;
  if (!btn || !out) return;
  if ((btn as any)._wired) return;
  (btn as any)._wired = true;

  btn.addEventListener("click", async () => {
    out.textContent = "Loading…";
    try {
      const res = await fetch("/api/hello", { headers: { Accept: "application/json" } });
      if (!res.ok) {
        out.textContent = `Error ${res.status}: ${res.statusText}`;
        return;
      }
      const data = await res.json();
      const pre = document.createElement("pre");
      pre.className = "bg-base-300 p-3 rounded overflow-x-auto text-sm";
      pre.textContent = typeof data === "string" ? data : JSON.stringify(data, null, 2);
      out.replaceChildren(pre);
    } catch (err) {
      console.error(err);
      out.textContent = "Network error. Check console for details.";
    }
  });
}
