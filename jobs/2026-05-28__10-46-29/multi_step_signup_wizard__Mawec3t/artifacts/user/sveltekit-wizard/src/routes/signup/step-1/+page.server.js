import { fail, redirect } from '@sveltejs/kit';
import { getSession } from '$lib/server/session';

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const load = ({ cookies }) => {
  const session = getSession(cookies);

  return {
    values: {
      email: session.data.email ?? ''
    }
  };
};

export const actions = {
  default: async ({ request, cookies }) => {
    const formData = await request.formData();
    const email = String(formData.get('email') ?? '').trim();
    const session = getSession(cookies);

    if (!email) {
      return fail(400, {
        error: 'Email is required.',
        values: { email }
      });
    }

    if (!emailRegex.test(email)) {
      return fail(400, {
        error: 'Enter a valid email address.',
        values: { email }
      });
    }

    session.data.email = email;

    redirect(303, '/signup/step-2');
  }
};
