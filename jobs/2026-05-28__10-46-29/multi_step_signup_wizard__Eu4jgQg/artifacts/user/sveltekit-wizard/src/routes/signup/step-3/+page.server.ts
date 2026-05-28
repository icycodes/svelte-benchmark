import { redirect, fail } from '@sveltejs/kit';
import { getSession, saveSession } from '$lib/server/session';

export function load({ cookies }) {
	const session = getSession(cookies);
	if (!session || !session.email) {
		redirect(303, '/signup/step-1');
	}
	if (!session.password) {
		redirect(303, '/signup/step-2');
	}
	return { firstName: session.firstName || '', lastName: session.lastName || '' };
}

export const actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();
		const firstName = data.get('firstName');
		const lastName = data.get('lastName');

		if (!firstName || typeof firstName !== 'string' || firstName.trim() === '') {
			return fail(400, { firstName, lastName, error: 'First name is required' });
		}
		if (!lastName || typeof lastName !== 'string' || lastName.trim() === '') {
			return fail(400, { firstName, lastName, error: 'Last name is required' });
		}

		const session = getSession(cookies);
		if (!session) {
			redirect(303, '/signup/step-1');
		}
		
		session.firstName = firstName.trim();
		session.lastName = lastName.trim();
		saveSession(cookies, session);

		redirect(303, '/signup/review');
	}
};
