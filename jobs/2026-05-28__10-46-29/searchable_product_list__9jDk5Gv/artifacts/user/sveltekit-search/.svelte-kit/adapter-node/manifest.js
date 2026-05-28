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
		client: {start:"_app/immutable/entry/start.BBGWnJZQ.js",app:"_app/immutable/entry/app.Dd5VbKqh.js",imports:["_app/immutable/entry/start.BBGWnJZQ.js","_app/immutable/chunks/NJgkM_AH.js","_app/immutable/chunks/BtAD9gsq.js","_app/immutable/chunks/0KFkW98c.js","_app/immutable/entry/app.Dd5VbKqh.js","_app/immutable/chunks/BtAD9gsq.js","_app/immutable/chunks/Wal417h-.js","_app/immutable/chunks/CCaUakoW.js","_app/immutable/chunks/0KFkW98c.js","_app/immutable/chunks/Cp9TSgUD.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js')),
			__memo(() => import('./nodes/3.js'))
		],
		remotes: {
			
		},
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: __memo(() => import('./entries/endpoints/_server.js'))
			},
			{
				id: "/api/products",
				pattern: /^\/api\/products\/?$/,
				params: [],
				page: null,
				endpoint: __memo(() => import('./entries/endpoints/api/products/_server.js'))
			},
			{
				id: "/products",
				pattern: /^\/products\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 3 },
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