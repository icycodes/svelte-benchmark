import crypto from "node:crypto";
const sessions = /* @__PURE__ */ new Map();
function getSession(cookies) {
  let sessionId = cookies.get("wizard_session");
  if (!sessionId || !sessions.has(sessionId)) {
    sessionId = crypto.randomUUID();
    cookies.set("wizard_session", sessionId, {
      path: "/",
      httpOnly: true,
      sameSite: "strict",
      maxAge: 60 * 60 * 24
      // 1 day
    });
    sessions.set(sessionId, {});
  }
  return sessions.get(sessionId);
}
function saveSession(cookies, data) {
  const sessionId = cookies.get("wizard_session");
  if (sessionId) {
    const current = sessions.get(sessionId) || {};
    sessions.set(sessionId, { ...current, ...data });
  }
}
function clearSession(cookies) {
  const sessionId = cookies.get("wizard_session");
  if (sessionId) {
    sessions.delete(sessionId);
    cookies.delete("wizard_session", { path: "/" });
  }
}
export {
  clearSession as c,
  getSession as g,
  saveSession as s
};
