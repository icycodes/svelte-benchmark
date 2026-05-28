import { redirect } from '@sveltejs/kit';
import { allowedLocales, defaultLocale } from '$lib/i18n.js';

export const actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();
		const locale = data.get('locale');

		if (locale && allowedLocales.includes(locale)) {
			cookies.set('locale', locale, { path: '/' });
		} else {
			cookies.set('locale', defaultLocale, { path: '/' });
		}

		throw redirect(303, '/');
	}
};
