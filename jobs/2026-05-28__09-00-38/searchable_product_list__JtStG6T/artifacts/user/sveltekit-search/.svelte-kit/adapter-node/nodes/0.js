

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/layout.svelte.js')).default;
export const imports = ["_app/immutable/nodes/0.BPHvw8x3.js","_app/immutable/chunks/yXMt-SqZ.js","_app/immutable/chunks/hUH6J2zQ.js","_app/immutable/chunks/BmzXaLVv.js"];
export const stylesheets = [];
export const fonts = [];
