import { fail, redirect } from '@sveltejs/kit';
import { getSession } from '$lib/server/session';

export const load = ({ cookies }) => {
  const session = getSession(cookies);

  if (!session.data.email) {
    redirect(303, '/signup/step-1');
  }

  if (!session.data.password) {
    redirect(303, '/signup/step-2');
  }

  return {
    values: {
      firstName: session.data.firstName ?? '',
      lastName: session.data.lastName ?? ''
    }
  };
};

export const actions = {
  default: async ({ request, cookies }) => {
    const session = getSession(cookies);

    if (!session.data.email) {
      redirect(303, '/signup/step-1');
    }

    if (!session.data.password) {
      redirect(303, '/signup/step-2');
    }

    const formData = await request.formData();
    const firstName = String(formData.get('firstName') ?? '').trim();
    const lastName = String(formData.get('lastName') ?? '').trim();

    if (!firstName || !lastName) {
      return fail(400, {
        error: 'First and last name are required.',
        values: { firstName, lastName }
      });
    }

    session.data.firstName = firstName;
    session.data.lastName = lastName;

    redirect(303, '/signup/review');
  }
};
