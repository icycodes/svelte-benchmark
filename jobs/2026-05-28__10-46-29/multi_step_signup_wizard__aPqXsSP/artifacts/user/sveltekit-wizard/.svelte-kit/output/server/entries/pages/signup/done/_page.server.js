function load({ url }) {
  const email = url.searchParams.get("email") ?? "";
  return { email };
}
export {
  load
};
