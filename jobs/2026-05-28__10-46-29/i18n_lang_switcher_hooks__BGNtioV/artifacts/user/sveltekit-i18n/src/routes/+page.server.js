import { redirect } from '@sveltejs/kit';
import { resolveLocale } from '$lib/i18n';

/** @type {import('./$types').PageServerLoad} */
export function load({ locals }) {
  return {
    locale: locals.locale
  };
}

/** @type {import('./$types').Actions} */
export const actions = {
  default: async ({ request, cookies }) => {
    const formData = await request.formData();
    const locale = resolveLocale(formData.get('locale')?.toString());

    cookies.set('locale', locale, {
      path: '/',
      httpOnly: false,
      secure: false,
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 365
    });

    redirect(303, '/');
  }
};
