/** @type {readonly ['en', 'de', 'fr']} */
export const LOCALES = /** @type {const} */ (['en', 'de', 'fr']);

/** @typedef {'en' | 'de' | 'fr'} Locale */

/** @type {Record<Locale, string>} */
export const greetings = {
  en: 'Hello, world!',
  de: 'Hallo, Welt!',
  fr: 'Bonjour, le monde !'
};

export const DEFAULT_LOCALE = /** @type {Locale} */ ('en');

/**
 * Validate a string value and return a valid locale, falling back to the default.
 * @param {string | null | undefined} value
 * @returns {Locale}
 */
export function resolveLocale(value) {
  if (value && LOCALES.includes(/** @type {Locale} */ (value))) {
    return /** @type {Locale} */ (value);
  }
  return DEFAULT_LOCALE;
}
