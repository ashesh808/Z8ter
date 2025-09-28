import { customElement, noShadowDOM } from "solid-element";
import { createSignal, createMemo, Show } from "solid-js";

type Props = { endpoint?: string };

customElement<Props>("z8-ping", { endpoint: "/api/hello" }, (p) => {
  noShadowDOM();
  const [status, setStatus] = createSignal<number | null>(null);
  const [ms, setMs] = createSignal<number | null>(null);
  const [body, setBody] = createSignal<unknown | null>(null);
  const [loading, setLoading] = createSignal(false);

  const ok = createMemo(() => {
    const s = status();
    return s !== null && s > 0 && s < 400;
  });

  const bench = async () => {
    setLoading(true);
    setBody(null);
    setStatus(null);
    setMs(null);

    const t0 = performance.now();
    try {
      const res = await fetch(p.endpoint!, { headers: { Accept: "application/json" } });
      setStatus(res.status);
      let data: unknown = null;
      const ct = res.headers.get("content-type") || "";
      if (ct.includes("application/json")) {
        try { data = await res.json(); } catch { data = null; }
      } else {
        try { data = await res.text(); } catch { data = null; }
      }
      setBody(data);
    } catch {
      // True network failure
      setStatus(-1);
      setBody({ error: "Network error" });
    } finally {
      setMs(Math.round(performance.now() - t0));
      setLoading(false);
    }
  };

  const renderableJson = createMemo<unknown | null>(() => {
    const b = body();
    return b && (typeof b === "object" || Array.isArray(b)) ? b : null;
  });

  return (
    <div>
      <button class="btn btn-primary btn-sm" disabled={loading()} onClick={bench}>
        {loading() ? "Pinging…" : `Benchmark ${p.endpoint}`}
      </button>

      <div class="mt-3 text-sm">
        {status() !== null ? (
          <div class="flex items-center gap-2">
            <span class={"badge " + (ok() ? "badge-success" : "badge-error")}>
              {status() === -1 ? "ERR" : status()}
            </span>
            {ms() !== null ? <span class="badge badge-ghost">{ms()} ms</span> : null}
          </div>
        ) : null}

        {renderableJson() ? (
          <pre class="bg-base-300 mt-2 p-3 rounded overflow-x-auto text-xs">
            {JSON.stringify(renderableJson(), null, 2)}
          </pre>
        ) : null}

       <Show when={typeof body() === "string"}>
          {(txt) => (
            <pre class="bg-base-300 mt-2 p-3 rounded overflow-x-auto text-xs">{txt()}</pre>
          )}
        </Show>
      </div>
    </div>
  );
});
