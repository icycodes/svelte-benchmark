import { randomUUID } from 'crypto';

/** @typedef {{ email?: string; password?: string; firstName?: string; lastName?: string; }} SessionData */

/** @type {Map<string, SessionData>} */
const store = new Map();

const COOKIE_NAME = 'wizard_sid';
const COOKIE_MAX_AGE = 60 * 60 * 24; // 24 hours

/**
 * Get the session data for the current request.
 * Creates a new session if none exists.
 * @param {import('@sveltejs/kit').Cookies} cookies
 * @returns {{ id: string; data: SessionData }}
 */
export function getSession(cookies) {
  let id = cookies.get(COOKIE_NAME);
  if (!id || !store.has(id)) {
    id = randomUUID();
    store.set(id, {});
    cookies.set(COOKIE_NAME, id, {
      path: '/',
      httpOnly: true,
      sameSite: 'lax',
      maxAge: COOKIE_MAX_AGE
    });
  }
  return { id, data: /** @type {SessionData} */ (store.get(id)) };
}

/**
 * Save session data (merges with existing data).
 * @param {import('@sveltejs/kit').Cookies} cookies
 * @param {Partial<SessionData>} updates
 */
export function saveSession(cookies, updates) {
  const { id, data } = getSession(cookies);
  Object.assign(data, updates);
  store.set(id, data);
}

/**
 * Clear wizard fields from the session (keeps the session cookie alive).
 * @param {import('@sveltejs/kit').Cookies} cookies
 */
export function clearSession(cookies) {
  const { id } = getSession(cookies);
  store.set(id, {});
}
