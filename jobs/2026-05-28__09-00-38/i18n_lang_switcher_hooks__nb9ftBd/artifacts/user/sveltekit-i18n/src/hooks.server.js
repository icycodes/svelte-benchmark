import { isValidLocale, defaultLocale } from '$lib/i18n';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
    let locale = event.cookies.get('locale');

    if (!isValidLocale(locale)) {
        locale = defaultLocale;
    }

    event.locals.locale = locale;

    return await resolve(event, {
        transformPageChunk: ({ html }) => {
            return html.replace('%lang%', locale);
        }
    });
}
