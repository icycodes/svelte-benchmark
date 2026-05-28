import { resolveLocale } from '$lib/i18n';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
  // Read and validate the locale cookie
  const cookieLocale = event.cookies.get('locale');
  event.locals.locale = resolveLocale(cookieLocale);

  const response = await resolve(event, {
    transformPageChunk({ html }) {
      // Replace the lang attribute on the <html> element with the resolved locale
      return html.replace(/<html([^>]*) lang="[^"]*"/, `<html$1 lang="${event.locals.locale}"`);
    }
  });

  return response;
}
