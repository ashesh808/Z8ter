const THEME_KEY = "z8_theme";
const ISLAND_PREF_KEY = "z8_island_pref";
function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try {
        localStorage.setItem(THEME_KEY, theme);
    }
    catch { }
}
function getInitialTheme() {
    try {
        const t = localStorage.getItem(THEME_KEY);
        if (t === "luxury" || t === "light")
            return t;
    }
    catch { }
    const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches;
    return prefersDark ? "luxury" : "light";
}
function escapeHtml(s) {
    return s.replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}
export default function initAbout() {
    const root = document.getElementById("about-root");
    if (!root)
        return;
    if (root._wired)
        return;
    root._wired = true;
    root.innerHTML = `
    <!-- Hero -->
    <section class="hero bg-base-200 rounded-2xl p-8 md:p-12">
      <div class="hero-content flex-col gap-4 text-center">
        <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight">About Z8ter</h1>
        <p class="opacity-90 text-lg">Async Python, SSR-first — small, fast, and convention-driven.</p>

        <!-- Client-only toolbar -->
        <div class="mt-4 flex flex-wrap items-center justify-center gap-3">
          <button id="about-theme" class="btn btn-sm">Toggle theme</button>
          <button id="about-copy" class="btn btn-sm btn-outline">Copy install</button>
          <span id="about-net" class="badge badge-outline">…</span>
          <span class="badge badge-ghost"><span id="about-clock">--:--:--</span></span>
        </div>
      </div>
    </section>

    <!-- Two-up: What & Principles -->
    <section class="mt-10 grid md:grid-cols-2 gap-8">
      <div class="card bg-base-200">
        <div class="card-body">
          <h2 class="card-title">What is Z8ter?</h2>
          <p class="opacity-80">
            A minimal full-stack framework built on Starlette + Jinja2. File-based routing for views,
            decorator-driven APIs, and a tiny per-page JS loader for just-enough interactivity.
          </p>
        </div>
      </div>

      <div class="card bg-base-200">
        <div class="card-body">
          <h2 class="card-title">Principles</h2>
          <ul class="space-y-2 text-sm">
            <li class="flex items-start gap-3"><span>📂</span><span>Conventions over config</span></li>
            <li class="flex items-start gap-3"><span>⚡</span><span>Async-first, SSR-first</span></li>
            <li class="flex items-start gap-3"><span>🧩</span><span>Small surface area, sharp tools</span></li>
          </ul>
          <label class="label cursor-pointer mt-4">
            <span class="label-text">Remember I like islands</span>
            <input id="about-island-pref" type="checkbox" class="toggle toggle-primary" />
          </label>
        </div>
      </div>
    </section>

    <!-- Client-only demos -->
    <section class="mt-10">
      <div class="card bg-base-200">
        <div class="card-body">
          <h2 class="card-title">Client demos</h2>
          <p class="opacity-80">Benchmark an API call locally and pretty-print the JSON.</p>
          <div class="flex gap-3">
            <button id="about-ping" class="btn btn-primary btn-sm">Benchmark /api/hello</button>
          </div>
          <div id="about-ping-out" class="mt-3 text-sm"></div>
        </div>
      </div>
    </section>
  `;
    // THEME (client preference)
    applyTheme(getInitialTheme());
    const themeBtn = root.querySelector("#about-theme");
    themeBtn?.addEventListener("click", () => {
        const next = (document.documentElement.getAttribute("data-theme") === "luxury") ? "light" : "luxury";
        applyTheme(next);
        themeBtn.blur();
    });
    // CLIPBOARD (browser-only)
    const copyBtn = root.querySelector("#about-copy");
    copyBtn?.addEventListener("click", async () => {
        const label = "pip install -e .";
        try {
            await navigator.clipboard.writeText(label);
            copyBtn.textContent = "Copied!";
            setTimeout(() => (copyBtn.textContent = "Copy install"), 1200);
        }
        catch {
            copyBtn.textContent = "Copy failed";
            setTimeout(() => (copyBtn.textContent = "Copy install"), 1200);
        }
    });
    // ONLINE/OFFLINE (realtime browser state)
    const net = root.querySelector("#about-net");
    const updateNet = () => {
        if (!net)
            return;
        const online = navigator.onLine;
        net.className = `badge ${online ? "badge-success" : "badge-error"}`;
        net.textContent = online ? "Online" : "Offline";
    };
    window.addEventListener("online", updateNet);
    window.addEventListener("offline", updateNet);
    updateNet();
    // CLOCK (local time, live)
    const clock = root.querySelector("#about-clock");
    const tick = () => { if (clock)
        clock.textContent = new Date().toLocaleTimeString(); };
    tick();
    const clockId = window.setInterval(tick, 1000);
    // Optional cleanup if you ever unmount:
    root._cleanup = () => clearInterval(clockId);
    // PERSISTED PREFERENCE (localStorage)
    const pref = root.querySelector("#about-island-pref");
    try {
        if (pref)
            pref.checked = localStorage.getItem(ISLAND_PREF_KEY) === "1";
    }
    catch { }
    pref?.addEventListener("change", () => {
        try {
            localStorage.setItem(ISLAND_PREF_KEY, pref.checked ? "1" : "0");
        }
        catch { }
    });
    // LATENCY BENCHMARK + PRETTY JSON (client-side formatting)
    const pingBtn = root.querySelector("#about-ping");
    const pingOut = root.querySelector("#about-ping-out");
    pingBtn?.addEventListener("click", async () => {
        if (!pingOut || !pingBtn)
            return;
        pingBtn.disabled = true;
        pingOut.textContent = "Pinging…";
        const t0 = performance.now();
        try {
            const res = await fetch("/api/hello", { headers: { Accept: "application/json" } });
            const t1 = performance.now();
            const ms = Math.round(t1 - t0);
            let body = null;
            try {
                body = await res.json();
            }
            catch { }
            const statusBadge = `<span class="badge ${res.ok ? "badge-success" : "badge-error"}">${res.status}</span>`;
            const timeBadge = `<span class="badge badge-ghost ml-2">${ms} ms</span>`;
            const pre = body != null
                ? `<pre class="bg-base-300 mt-2 p-3 rounded overflow-x-auto text-xs">${escapeHtml(JSON.stringify(body, null, 2))}</pre>`
                : "";
            pingOut.innerHTML = statusBadge + timeBadge + pre;
        }
        catch (err) {
            console.error(err);
            pingOut.textContent = "Network error. See console.";
        }
        finally {
            pingBtn.disabled = false;
        }
    });
}
