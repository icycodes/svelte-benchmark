import { json } from "@sveltejs/kit";
const products = [
  { id: 1, name: "Apple iPhone", price: 999 },
  { id: 2, name: "Banana Phone", price: 199 },
  { id: 3, name: "Cherry Tablet", price: 499 },
  { id: 4, name: "Pear Laptop", price: 1299 },
  { id: 5, name: "Grape Watch", price: 399 },
  { id: 6, name: "Melon Speaker", price: 149 }
];
function GET() {
  return json(products);
}
export {
  GET
};
