export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {start:"_app/immutable/entry/start.f0ivJCl8.js",app:"_app/immutable/entry/app.BgfqED3q.js",imports:["_app/immutable/entry/start.f0ivJCl8.js","_app/immutable/chunks/DsbGaql9.js","_app/immutable/chunks/CsnI_foH.js","_app/immutable/chunks/BCk_81HG.js","_app/immutable/entry/app.BgfqED3q.js","_app/immutable/chunks/BCk_81HG.js","_app/immutable/chunks/CsnI_foH.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/C4eGlgVg.js","_app/immutable/chunks/BC0heB5l.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js'))
		],
		remotes: {
			
		},
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

export const prerendered = new Set([]);

export const base = "";