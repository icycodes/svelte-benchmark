import { redirect, fail } from "@sveltejs/kit";
import { g as getSession, s as saveSession } from "../../../../chunks/session.js";
function load({ cookies }) {
  const { data } = getSession(cookies);
  if (!data.email) {
    redirect(303, "/signup/step-1");
  }
  if (!data.password) {
    redirect(303, "/signup/step-2");
  }
  return {
    firstName: data.firstName ?? "",
    lastName: data.lastName ?? ""
  };
}
const actions = {
  default: async ({ request, cookies }) => {
    const { data } = getSession(cookies);
    if (!data.email) {
      redirect(303, "/signup/step-1");
    }
    if (!data.password) {
      redirect(303, "/signup/step-2");
    }
    const formData = await request.formData();
    const firstName = String(formData.get("firstName") ?? "").trim();
    const lastName = String(formData.get("lastName") ?? "").trim();
    if (!firstName) {
      return fail(400, {
        field: "firstName",
        message: "First name is required.",
        firstNameValue: firstName,
        lastNameValue: lastName
      });
    }
    if (!lastName) {
      return fail(400, {
        field: "lastName",
        message: "Last name is required.",
        firstNameValue: firstName,
        lastNameValue: lastName
      });
    }
    saveSession(cookies, { firstName, lastName });
    redirect(303, "/signup/review");
  }
};
export {
  actions,
  load
};
