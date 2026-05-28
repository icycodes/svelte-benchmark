export const locales = ['en', 'de', 'fr'];

export const translations = {
	en: 'Hello, world!',
	de: 'Hallo, Welt!',
	fr: 'Bonjour, le monde !'
};

export const defaultLocale = 'en';

export const isSupportedLocale = (locale) => locales.includes(locale);
