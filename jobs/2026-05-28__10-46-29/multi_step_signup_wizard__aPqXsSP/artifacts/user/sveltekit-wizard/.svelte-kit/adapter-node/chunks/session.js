import { randomUUID } from "crypto";
const store = /* @__PURE__ */ new Map();
const COOKIE_NAME = "wizard_sid";
const COOKIE_MAX_AGE = 60 * 60 * 24;
function getSession(cookies) {
  let id = cookies.get(COOKIE_NAME);
  if (!id || !store.has(id)) {
    id = randomUUID();
    store.set(id, {});
    cookies.set(COOKIE_NAME, id, {
      path: "/",
      httpOnly: true,
      sameSite: "lax",
      maxAge: COOKIE_MAX_AGE
    });
  }
  return { id, data: (
    /** @type {SessionData} */
    store.get(id)
  ) };
}
function saveSession(cookies, updates) {
  const { id, data } = getSession(cookies);
  Object.assign(data, updates);
  store.set(id, data);
}
function clearSession(cookies) {
  const { id } = getSession(cookies);
  store.set(id, {});
}
export {
  clearSession as c,
  getSession as g,
  saveSession as s
};
