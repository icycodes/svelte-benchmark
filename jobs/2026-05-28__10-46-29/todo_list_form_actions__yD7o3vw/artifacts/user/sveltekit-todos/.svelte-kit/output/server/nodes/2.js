import * as server from '../entries/pages/_page.server.js';

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export { server };
export const server_id = "src/routes/+page.server.js";
export const imports = ["_app/immutable/nodes/2.B1zkVbEZ.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/BCk_81HG.js","_app/immutable/chunks/CsnI_foH.js","_app/immutable/chunks/C4eGlgVg.js","_app/immutable/chunks/BC0heB5l.js","_app/immutable/chunks/DsbGaql9.js"];
export const stylesheets = ["_app/immutable/assets/2.CUjOThVp.css"];
export const fonts = [];
