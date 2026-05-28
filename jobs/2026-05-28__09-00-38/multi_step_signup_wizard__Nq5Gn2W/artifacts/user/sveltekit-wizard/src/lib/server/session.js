import crypto from 'node:crypto';

/** @type {Map<string, any>} */
const sessions = new Map();

/**
 * @param {import('@sveltejs/kit').Cookies} cookies
 */
export function getSession(cookies) {
	let sessionId = cookies.get('wizard_session');
	if (!sessionId || !sessions.has(sessionId)) {
		sessionId = crypto.randomUUID();
		cookies.set('wizard_session', sessionId, {
			path: '/',
			httpOnly: true,
			sameSite: 'strict',
			maxAge: 60 * 60 * 24 // 1 day
		});
		sessions.set(sessionId, {});
	}
	return sessions.get(sessionId);
}

/**
 * @param {import('@sveltejs/kit').Cookies} cookies
 * @param {any} data
 */
export function saveSession(cookies, data) {
	const sessionId = cookies.get('wizard_session');
	if (sessionId) {
		const current = sessions.get(sessionId) || {};
		sessions.set(sessionId, { ...current, ...data });
	}
}

/**
 * @param {import('@sveltejs/kit').Cookies} cookies
 */
export function clearSession(cookies) {
	const sessionId = cookies.get('wizard_session');
	if (sessionId) {
		sessions.delete(sessionId);
		cookies.delete('wizard_session', { path: '/' });
	}
}
