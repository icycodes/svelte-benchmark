import * as server from '../entries/pages/_page.server.js';

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export { server };
export const server_id = "src/routes/+page.server.js";
export const imports = ["_app/immutable/nodes/2.CoyhL5tn.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/BkjzzIGc.js","_app/immutable/chunks/BjbxEtvn.js","_app/immutable/chunks/C7CvRu5q.js"];
export const stylesheets = ["_app/immutable/assets/2.C60SjyOd.css"];
export const fonts = [];
