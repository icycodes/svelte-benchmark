import { fail, redirect } from "@sveltejs/kit";
import { s as saveSession, g as getSession } from "../../../../chunks/session.js";
function load({ cookies }) {
  const { data } = getSession(cookies);
  return { email: data.email ?? "" };
}
const actions = {
  default: async ({ request, cookies }) => {
    const formData = await request.formData();
    const email = String(formData.get("email") ?? "").trim();
    if (!email) {
      return fail(400, { field: "email", message: "Email is required.", value: email });
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return fail(400, { field: "email", message: "Please enter a valid email address.", value: email });
    }
    saveSession(cookies, { email });
    redirect(303, "/signup/step-2");
  }
};
export {
  actions,
  load
};
