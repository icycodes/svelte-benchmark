import * as server from '../entries/pages/signup/done/_page.server.js';

export const index = 3;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/signup/done/_page.svelte.js')).default;
export { server };
export const server_id = "src/routes/signup/done/+page.server.js";
export const imports = ["_app/immutable/nodes/3.CEdC9QV7.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/rlbNfMNf.js","_app/immutable/chunks/DB5FkY7-.js"];
export const stylesheets = ["_app/immutable/assets/3.DY7B9tEU.css"];
export const fonts = [];
