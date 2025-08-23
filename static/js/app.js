"use strict";
const pagesPath = "/static/js/pages/";
function onReady(fn) {
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", fn, { once: true });
    }
    else {
        fn();
    }
}
function pageIdFromDOM() {
    const id = document.body?.dataset?.page?.trim();
    return id && id.length > 0 ? id : "default";
}
function idToPath(id) {
    const segs = id.split(".").join("/");
    return `${pagesPath}${segs}.js`;
}
async function loadAndRun(id) {
    const path = idToPath(id);
    try {
        const mod = (await import(/* @vite-ignore */ path));
        await mod.default?.({ pageId: id, id, body: document.body });
        console.debug("[router] loaded:", id, "→", path);
    }
    catch {
        console.warn("[router] missing module:", id, "→", path);
    }
}
onReady(async () => {
    const pid = pageIdFromDOM();
    await loadAndRun("common");
    await loadAndRun(pid);
});
