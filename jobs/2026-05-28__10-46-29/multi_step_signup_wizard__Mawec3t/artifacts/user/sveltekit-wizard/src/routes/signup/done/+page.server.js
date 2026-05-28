export const load = ({ url }) => {
  return {
    email: url.searchParams.get('email') ?? ''
  };
};
