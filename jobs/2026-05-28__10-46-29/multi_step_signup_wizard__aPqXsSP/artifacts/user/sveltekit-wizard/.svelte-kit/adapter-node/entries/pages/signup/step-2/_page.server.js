import { redirect, fail } from "@sveltejs/kit";
import { g as getSession, s as saveSession } from "../../../../chunks/session.js";
function load({ cookies }) {
  const { data } = getSession(cookies);
  if (!data.email) {
    redirect(303, "/signup/step-1");
  }
  return {};
}
const actions = {
  default: async ({ request, cookies }) => {
    const { data } = getSession(cookies);
    if (!data.email) {
      redirect(303, "/signup/step-1");
    }
    const formData = await request.formData();
    const password = String(formData.get("password") ?? "");
    const confirmPassword = String(formData.get("confirmPassword") ?? "");
    if (!password) {
      return fail(400, { field: "password", message: "Password is required." });
    }
    if (password.length < 8) {
      return fail(400, { field: "password", message: "Password must be at least 8 characters." });
    }
    if (confirmPassword !== password) {
      return fail(400, { field: "confirmPassword", message: "Passwords do not match." });
    }
    saveSession(cookies, { password });
    redirect(303, "/signup/step-3");
  }
};
export {
  actions,
  load
};
