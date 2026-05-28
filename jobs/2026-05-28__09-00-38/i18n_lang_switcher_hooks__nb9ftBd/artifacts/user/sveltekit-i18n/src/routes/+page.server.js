import { redirect } from '@sveltejs/kit';
import { isValidLocale } from '$lib/i18n';

/** @type {import('./$types').Actions} */
export const actions = {
    default: async ({ request, cookies }) => {
        const data = await request.formData();
        const locale = data.get('locale');

        if (typeof locale === 'string' && isValidLocale(locale)) {
            cookies.set('locale', locale, { path: '/', httpOnly: false });
        }

        throw redirect(303, '/');
    }
};
