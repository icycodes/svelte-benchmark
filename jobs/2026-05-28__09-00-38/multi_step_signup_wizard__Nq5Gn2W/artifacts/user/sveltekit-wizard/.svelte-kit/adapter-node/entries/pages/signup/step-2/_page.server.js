import { s as saveSession, g as getSession } from "../../../../chunks/session.js";
import { fail, redirect } from "@sveltejs/kit";
function load({ cookies }) {
  const session = getSession(cookies);
  if (!session.email) {
    throw redirect(303, "/signup/step-1");
  }
  return {};
}
const actions = {
  default: async ({ request, cookies }) => {
    const formData = await request.formData();
    const password = formData.get("password");
    const confirmPassword = formData.get("confirmPassword");
    if (!password || typeof password !== "string" || password.length < 8) {
      return fail(400, {
        message: "Password must be at least 8 characters long"
      });
    }
    if (password !== confirmPassword) {
      return fail(400, {
        message: "Passwords do not match"
      });
    }
    saveSession(cookies, { password });
    throw redirect(303, "/signup/step-3");
  }
};
export {
  actions,
  load
};
