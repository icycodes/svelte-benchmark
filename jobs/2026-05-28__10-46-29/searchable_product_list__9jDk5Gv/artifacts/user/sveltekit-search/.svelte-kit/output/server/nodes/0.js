

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/layout.svelte.js')).default;
export const imports = ["_app/immutable/nodes/0.gsIEo4Fc.js","_app/immutable/chunks/CCaUakoW.js","_app/immutable/chunks/BtAD9gsq.js","_app/immutable/chunks/Cp9TSgUD.js"];
export const stylesheets = [];
export const fonts = [];
