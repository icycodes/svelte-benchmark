import { randomUUID } from 'crypto';

const sessions = new Map();

export function getSession(cookies) {
	const sessionId = cookies.get('session_id');
	if (!sessionId) {
		return null;
	}
	return sessions.get(sessionId) || null;
}

export function saveSession(cookies, data) {
	let sessionId = cookies.get('session_id');
	if (!sessionId) {
		sessionId = randomUUID();
		cookies.set('session_id', sessionId, { path: '/', httpOnly: true, sameSite: 'lax' });
	}
	sessions.set(sessionId, data);
}

export function clearSession(cookies) {
	const sessionId = cookies.get('session_id');
	if (sessionId) {
		sessions.delete(sessionId);
		cookies.delete('session_id', { path: '/' });
	}
}
