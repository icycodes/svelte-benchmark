import { s as saveSession, g as getSession } from "../../../../chunks/session.js";
import { fail, redirect } from "@sveltejs/kit";
function load({ cookies }) {
  const session = getSession(cookies);
  return {
    email: session.email ?? ""
  };
}
const actions = {
  default: async ({ request, cookies }) => {
    const formData = await request.formData();
    const email = formData.get("email");
    if (!email || typeof email !== "string" || !email.includes("@")) {
      return fail(400, {
        email,
        message: "Invalid email address"
      });
    }
    saveSession(cookies, { email });
    throw redirect(303, "/signup/step-2");
  }
};
export {
  actions,
  load
};
