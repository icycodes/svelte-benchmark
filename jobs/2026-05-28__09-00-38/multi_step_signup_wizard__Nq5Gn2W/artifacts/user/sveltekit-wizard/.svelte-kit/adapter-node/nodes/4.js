import * as server from '../entries/pages/signup/review/_page.server.js';

export const index = 4;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/signup/review/_page.svelte.js')).default;
export { server };
export const server_id = "src/routes/signup/review/+page.server.js";
export const imports = ["_app/immutable/nodes/4.CiWPu6vu.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/CucmRlgg.js","_app/immutable/chunks/D9twIeJG.js","_app/immutable/chunks/0oeiUk_Z.js","_app/immutable/chunks/CFzH4bLl.js","_app/immutable/chunks/DPEUtAgq.js","_app/immutable/chunks/BATeZYtw.js"];
export const stylesheets = [];
export const fonts = [];
