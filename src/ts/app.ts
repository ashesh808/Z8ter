type PageCtx = { pageId: string; id: string; body: HTMLElement };
type PageModule = { default?: (ctx: PageCtx) => void | Promise<void> };
const pagesPath: string = "/static/js/pages/"

function onReady(fn: () => void): void {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fn, { once: true });
  } else {
    fn();
  }
}

function pageIdFromDOM(): string {
  const id = document.body?.dataset?.page?.trim();
  return id && id.length > 0 ? id : "default";
}

function idToPath(id: string): string {
  const segs = id.split(".").join("/");
  return `${pagesPath}${segs}.js`;
}

async function loadAndRun(id: string): Promise<void> {
  const path = idToPath(id);
  try {
    const mod = (await import(/* @vite-ignore */ path)) as PageModule;
    await mod.default?.({ pageId: id, id, body: document.body });
    console.debug("[router] loaded:", id, "→", path);
  } catch {
    console.warn("[router] missing module:", id, "→", path);
  }
}

onReady(async () => {
  const pid = pageIdFromDOM();
  await loadAndRun("common");
  await loadAndRun(pid);
});
