

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/layout.svelte.js')).default;
export const imports = ["_app/immutable/nodes/0.DRSTDgqD.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/BCk_81HG.js","_app/immutable/chunks/BC0heB5l.js"];
export const stylesheets = [];
export const fonts = [];
