import { randomUUID } from 'crypto';

const COOKIE_NAME = 'wizard_session';
const sessions = new Map();

export function getSession(cookies) {
  let sessionId = cookies.get(COOKIE_NAME);

  if (!sessionId) {
    sessionId = randomUUID();
    cookies.set(COOKIE_NAME, sessionId, {
      path: '/',
      httpOnly: true,
      sameSite: 'lax'
    });
  }

  let session = sessions.get(sessionId);
  if (!session) {
    session = { id: sessionId, data: {} };
    sessions.set(sessionId, session);
  }

  return session;
}

export function clearSession(cookies) {
  const sessionId = cookies.get(COOKIE_NAME);
  if (sessionId) {
    sessions.delete(sessionId);
  }

  cookies.delete(COOKIE_NAME, { path: '/' });
}
