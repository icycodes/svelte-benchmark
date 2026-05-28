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
		client: {start:"_app/immutable/entry/start.BFUTVg90.js",app:"_app/immutable/entry/app.7TNcrbAn.js",imports:["_app/immutable/entry/start.BFUTVg90.js","_app/immutable/chunks/C7CvRu5q.js","_app/immutable/chunks/BjbxEtvn.js","_app/immutable/chunks/BkjzzIGc.js","_app/immutable/entry/app.7TNcrbAn.js","_app/immutable/chunks/BkjzzIGc.js","_app/immutable/chunks/BjbxEtvn.js","_app/immutable/chunks/CWj6FrbW.js","_app/immutable/chunks/_nBKQTo4.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
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
