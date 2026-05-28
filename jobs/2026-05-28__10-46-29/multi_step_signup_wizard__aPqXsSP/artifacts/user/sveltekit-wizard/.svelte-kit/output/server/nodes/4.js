import * as server from '../entries/pages/signup/review/_page.server.js';

export const index = 4;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/signup/review/_page.svelte.js')).default;
export { server };
export const server_id = "src/routes/signup/review/+page.server.js";
export const imports = ["_app/immutable/nodes/4.DOdHn2An.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/rlbNfMNf.js","_app/immutable/chunks/DB5FkY7-.js","_app/immutable/chunks/CkqKoLcK.js","_app/immutable/chunks/CbNVLuIk.js","_app/immutable/chunks/DMMJaSdm.js","_app/immutable/chunks/C9aqCoCe.js","_app/immutable/chunks/CaSyI8Da.js"];
export const stylesheets = ["_app/immutable/assets/4.DJcT4LyA.css"];
export const fonts = [];
