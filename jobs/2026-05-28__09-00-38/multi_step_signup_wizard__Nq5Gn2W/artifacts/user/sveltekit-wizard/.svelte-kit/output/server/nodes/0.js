

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/layout.svelte.js')).default;
export const imports = ["_app/immutable/nodes/0.tbTX5BEt.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/CucmRlgg.js","_app/immutable/chunks/CFzH4bLl.js"];
export const stylesheets = [];
export const fonts = [];
