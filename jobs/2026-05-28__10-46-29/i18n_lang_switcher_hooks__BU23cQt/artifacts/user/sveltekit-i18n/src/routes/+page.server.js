import { redirect } from '@sveltejs/kit';
import { isSupportedLocale } from '$lib/i18n';

export const actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();
		const locale = data.get('locale');

		if (typeof locale === 'string' && isSupportedLocale(locale)) {
			cookies.set('locale', locale, { path: '/' });
		}

		throw redirect(303, '/');
	}
};
