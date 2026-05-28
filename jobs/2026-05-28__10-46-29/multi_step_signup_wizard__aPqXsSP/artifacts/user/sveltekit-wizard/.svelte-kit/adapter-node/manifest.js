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
		client: {start:"_app/immutable/entry/start.Bsc9LyMn.js",app:"_app/immutable/entry/app.BqWXOUs9.js",imports:["_app/immutable/entry/start.Bsc9LyMn.js","_app/immutable/chunks/C9aqCoCe.js","_app/immutable/chunks/CaSyI8Da.js","_app/immutable/chunks/rlbNfMNf.js","_app/immutable/chunks/DB5FkY7-.js","_app/immutable/entry/app.BqWXOUs9.js","_app/immutable/chunks/rlbNfMNf.js","_app/immutable/chunks/DB5FkY7-.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/CaSyI8Da.js","_app/immutable/chunks/CkqKoLcK.js","_app/immutable/chunks/CbNVLuIk.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js')),
			__memo(() => import('./nodes/3.js')),
			__memo(() => import('./nodes/4.js')),
			__memo(() => import('./nodes/5.js')),
			__memo(() => import('./nodes/6.js')),
			__memo(() => import('./nodes/7.js'))
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
			},
			{
				id: "/signup/done",
				pattern: /^\/signup\/done\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 3 },
				endpoint: null
			},
			{
				id: "/signup/review",
				pattern: /^\/signup\/review\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 4 },
				endpoint: null
			},
			{
				id: "/signup/step-1",
				pattern: /^\/signup\/step-1\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 5 },
				endpoint: null
			},
			{
				id: "/signup/step-2",
				pattern: /^\/signup\/step-2\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 6 },
				endpoint: null
			},
			{
				id: "/signup/step-3",
				pattern: /^\/signup\/step-3\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 7 },
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