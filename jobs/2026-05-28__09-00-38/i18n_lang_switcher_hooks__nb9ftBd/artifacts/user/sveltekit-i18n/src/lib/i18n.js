export const locales = ['en', 'de', 'fr'];
export const defaultLocale = 'en';

export const translations = {
    en: {
        greeting: 'Hello, world!'
    },
    de: {
        greeting: 'Hallo, Welt!'
    },
    fr: {
        greeting: 'Bonjour, le monde !'
    }
};

/**
 * @param {string | null | undefined} locale
 * @returns {locale is 'en' | 'de' | 'fr'}
 */
export function isValidLocale(locale) {
    return !!locale && locales.includes(locale);
}
