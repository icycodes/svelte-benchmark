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
		client: {start:"_app/immutable/entry/start.DEU_-CnK.js",app:"_app/immutable/entry/app.B_vRlr4N.js",imports:["_app/immutable/entry/start.DEU_-CnK.js","_app/immutable/chunks/CeZEYOPG.js","_app/immutable/chunks/hUH6J2zQ.js","_app/immutable/chunks/BxXlE9cE.js","_app/immutable/entry/app.B_vRlr4N.js","_app/immutable/chunks/hUH6J2zQ.js","_app/immutable/chunks/BXFSO2fk.js","_app/immutable/chunks/yXMt-SqZ.js","_app/immutable/chunks/BxXlE9cE.js","_app/immutable/chunks/BmzXaLVv.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
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
				endpoint: null
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
