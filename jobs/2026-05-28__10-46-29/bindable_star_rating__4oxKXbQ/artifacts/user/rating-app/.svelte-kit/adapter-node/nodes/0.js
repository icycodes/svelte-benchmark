

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/layout.svelte.js')).default;
export const imports = ["_app/immutable/nodes/0.CqL0XDKf.js","_app/immutable/chunks/D9Qk9xDm.js","_app/immutable/chunks/By7z8LXc.js","_app/immutable/chunks/BcB2GitX.js"];
export const stylesheets = [];
export const fonts = [];
