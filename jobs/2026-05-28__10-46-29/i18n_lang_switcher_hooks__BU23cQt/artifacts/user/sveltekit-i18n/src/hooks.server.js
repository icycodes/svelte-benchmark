import { defaultLocale, isSupportedLocale } from '$lib/i18n';

const resolveLocale = (cookieValue) =>
	cookieValue && isSupportedLocale(cookieValue) ? cookieValue : defaultLocale;

export const handle = async ({ event, resolve }) => {
	const locale = resolveLocale(event.cookies.get('locale'));
	event.locals.locale = locale;

	return resolve(event, {
		transformPageChunk: ({ html }) => html.replace('<html lang="en">', `<html lang="${locale}">`)
	});
};
