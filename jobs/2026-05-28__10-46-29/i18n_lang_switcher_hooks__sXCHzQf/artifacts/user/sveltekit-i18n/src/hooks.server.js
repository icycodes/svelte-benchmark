import { allowedLocales, defaultLocale } from '$lib/i18n.js';

export async function handle({ event, resolve }) {
	const cookieLocale = event.cookies.get('locale');
	let locale = defaultLocale;

	if (cookieLocale && allowedLocales.includes(cookieLocale)) {
		locale = cookieLocale;
	}

	event.locals.locale = locale;

	return resolve(event, {
		transformPageChunk: ({ html }) => html.replace('<html lang="en">', `<html lang="${locale}">`)
	});
}
