/** @type {import('./$types').LayoutServerLoad} */
export function load({ locals }) {
  return {
    locale: locals.locale
  };
}
