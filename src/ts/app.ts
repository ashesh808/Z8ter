type PageCtx = { pageId: string; id: string; body: HTMLElement };
type PageModule = { default?: (ctx: PageCtx) => void | Promise<void> };

const pages = import.meta.glob<PageModule>("./pages/**/*.ts", { eager: false });

function pageIdFromDOM(): string {
  return document.body?.dataset?.page?.trim() || "default";
}
function idToKey(id: string): string {
  return `./pages/${id.split(".").join("/")}.ts`;
}

async function run(id: string) {
  const key = idToKey(id);
  console.debug("[z8] pageId:", id, "key:", key, "seen keys:", Object.keys(pages));
  const importer = pages[key];
  if (!importer) {
    console.warn("[z8] missing page module:", key);
    return;
  }
  const mod = await importer();
  await mod.default?.({ pageId: id, id, body: document.body });
}

document.addEventListener("DOMContentLoaded", async () => {
  await run("common");
  await run(pageIdFromDOM());
});
