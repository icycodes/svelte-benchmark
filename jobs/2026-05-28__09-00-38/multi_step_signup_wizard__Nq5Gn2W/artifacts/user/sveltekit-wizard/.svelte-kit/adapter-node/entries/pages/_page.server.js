import { redirect } from "@sveltejs/kit";
function load() {
  throw redirect(303, "/signup/step-1");
}
export {
  load
};
