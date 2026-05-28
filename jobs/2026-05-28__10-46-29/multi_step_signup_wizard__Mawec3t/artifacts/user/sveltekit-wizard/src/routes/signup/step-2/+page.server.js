import { fail, redirect } from '@sveltejs/kit';
import { getSession } from '$lib/server/session';

export const load = ({ cookies }) => {
  const session = getSession(cookies);

  if (!session.data.email) {
    redirect(303, '/signup/step-1');
  }

  return {};
};

export const actions = {
  default: async ({ request, cookies }) => {
    const session = getSession(cookies);

    if (!session.data.email) {
      redirect(303, '/signup/step-1');
    }

    const formData = await request.formData();
    const password = String(formData.get('password') ?? '');
    const confirmPassword = String(formData.get('confirmPassword') ?? '');

    if (!password) {
      return fail(400, { error: 'Password is required.' });
    }

    if (password.length < 8) {
      return fail(400, { error: 'Password must be at least 8 characters long.' });
    }

    if (password !== confirmPassword) {
      return fail(400, { error: 'Passwords do not match.' });
    }

    session.data.password = password;

    redirect(303, '/signup/step-3');
  }
};
