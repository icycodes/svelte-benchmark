import { redirect } from '@sveltejs/kit';

export const load = () => {
  redirect(303, '/signup/step-1');
};
