
// this file is generated — do not edit it


declare module "svelte/elements" {
	export interface HTMLAttributes<T> {
		'data-sveltekit-keepfocus'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-noscroll'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-preload-code'?:
			| true
			| ''
			| 'eager'
			| 'viewport'
			| 'hover'
			| 'tap'
			| 'off'
			| undefined
			| null;
		'data-sveltekit-preload-data'?: true | '' | 'hover' | 'tap' | 'off' | undefined | null;
		'data-sveltekit-reload'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-replacestate'?: true | '' | 'off' | undefined | null;
	}
}

export {};


declare module "$app/types" {
	type MatcherParam<M> = M extends (param : string) => param is (infer U extends string) ? U : string;

	export interface AppTypes {
		RouteId(): "/" | "/signup" | "/signup/done" | "/signup/review" | "/signup/step-1" | "/signup/step-2" | "/signup/step-3";
		RouteParams(): {
			
		};
		LayoutParams(): {
			"/": Record<string, never>;
			"/signup": Record<string, never>;
			"/signup/done": Record<string, never>;
			"/signup/review": Record<string, never>;
			"/signup/step-1": Record<string, never>;
			"/signup/step-2": Record<string, never>;
			"/signup/step-3": Record<string, never>
		};
		Pathname(): "/" | "/signup/done" | "/signup/review" | "/signup/step-1" | "/signup/step-2" | "/signup/step-3";
		ResolvedPathname(): `${"" | `/${string}`}${ReturnType<AppTypes['Pathname']>}`;
		Asset(): string & {};
	}
}