import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { createRoot, type Root } from "react-dom/client";

type Props = {
  endpoint?: string;
};

const DEFAULT_ENDPOINT = "/api/hello";

const Ping: React.FC<Props> = ({ endpoint = DEFAULT_ENDPOINT }) => {
  const [status, setStatus] = useState<number | null>(null);
  const [ms, setMs] = useState<number | null>(null);
  const [body, setBody] = useState<unknown | null>(null);
  const [loading, setLoading] = useState(false);
  const aliveRef = useRef(true);

  useEffect(() => {
    aliveRef.current = true;
    return () => {
      aliveRef.current = false;
    };
  }, []);

  const ok = useMemo(() => {
    return status !== null && status > 0 && status < 400;
  }, [status]);

  const renderableJson = useMemo(() => {
    if (!body || typeof body !== "object") {
      return null;
    }
    return body;
  }, [body]);

  const bench = useCallback(async () => {
    const alive = aliveRef;
    setLoading(true);
    setBody(null);
    setStatus(null);
    setMs(null);

    const t0 = performance.now();
    try {
      const res = await fetch(endpoint, { headers: { Accept: "application/json" } });
      if (!alive.current) {
        return;
      }
      setStatus(res.status);

      let data: unknown = null;
      const contentType = res.headers.get("content-type") || "";
      if (contentType.includes("application/json")) {
        try {
          data = await res.json();
        } catch {
          data = null;
        }
      } else {
        try {
          data = await res.text();
        } catch {
          data = null;
        }
      }
      if (!alive.current) {
        return;
      }
      setBody(data);
    } catch {
      if (!alive.current) {
        return;
      }
      setStatus(-1);
      setBody({ error: "Network error" });
    } finally {
      if (!alive.current) {
        return;
      }
      setMs(Math.round(performance.now() - t0));
      setLoading(false);
    }
  }, [endpoint]);

  return (
    <div>
      <button className="btn btn-primary btn-sm" disabled={loading} onClick={bench} type="button">
        {loading ? "Pinging…" : `Benchmark ${endpoint}`}
      </button>

      <div className="mt-3 text-sm">
        {status !== null ? (
          <div className="flex items-center gap-2">
            <span className={`badge ${ok ? "badge-success" : "badge-error"}`}>
              {status === -1 ? "ERR" : status}
            </span>
            {ms !== null ? <span className="badge badge-ghost">{ms} ms</span> : null}
          </div>
        ) : null}

        {renderableJson ? (
          <pre className="bg-base-300 mt-2 p-3 rounded overflow-x-auto text-xs">
            {JSON.stringify(renderableJson, null, 2)}
          </pre>
        ) : null}

        {typeof body === "string" ? (
          <pre className="bg-base-300 mt-2 p-3 rounded overflow-x-auto text-xs">{body}</pre>
        ) : null}
      </div>
    </div>
  );
};

class Z8PingElement extends HTMLElement {
  private root: Root | null = null;

  static get observedAttributes(): string[] {
    return ["endpoint"];
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

  private getEndpoint(): string {
    return this.getAttribute("endpoint") ?? DEFAULT_ENDPOINT;
  }

  private render(): void {
    this.ensureRoot().render(<Ping endpoint={this.getEndpoint()} />);
  }
}

if (!customElements.get("z8-ping")) {
  customElements.define("z8-ping", Z8PingElement);
}
