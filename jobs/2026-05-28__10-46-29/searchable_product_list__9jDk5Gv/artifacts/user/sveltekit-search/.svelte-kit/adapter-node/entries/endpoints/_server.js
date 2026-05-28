import { redirect } from "@sveltejs/kit";
function GET() {
  throw redirect(302, "/products");
}
export {
  GET
};
