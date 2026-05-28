import * as universal from '../entries/pages/products/_page.js';

export const index = 3;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/products/_page.svelte.js')).default;
export { universal };
export const universal_id = "src/routes/products/+page.js";
export const imports = ["_app/immutable/nodes/3.BvP3w2_W.js","_app/immutable/chunks/CCaUakoW.js","_app/immutable/chunks/BtAD9gsq.js","_app/immutable/chunks/Wal417h-.js","_app/immutable/chunks/NJgkM_AH.js","_app/immutable/chunks/0KFkW98c.js"];
export const stylesheets = [];
export const fonts = [];
