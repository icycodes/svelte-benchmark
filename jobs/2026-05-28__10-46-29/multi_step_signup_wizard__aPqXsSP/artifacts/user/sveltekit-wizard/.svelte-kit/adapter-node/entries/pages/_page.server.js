import { redirect } from "@sveltejs/kit";
function load() {
  redirect(303, "/signup/step-1");
}
export {
  load
};
