import { getSession, saveSession } from '$lib/server/session';
import { fail, redirect } from '@sveltejs/kit';

export function load({ cookies }) {
	const session = getSession(cookies);
	if (!session.email) throw redirect(303, '/signup/step-1');
	if (!session.password) throw redirect(303, '/signup/step-2');
	
	return {
		firstName: session.firstName ?? '',
		lastName: session.lastName ?? ''
	};
}

export const actions = {
	default: async ({ request, cookies }) => {
		const formData = await request.formData();
		const firstName = formData.get('firstName');
		const lastName = formData.get('lastName');

		if (!firstName || typeof firstName !== 'string' || firstName.trim() === '') {
			return fail(400, {
				firstName,
				lastName,
				message: 'First name is required'
			});
		}

		if (!lastName || typeof lastName !== 'string' || lastName.trim() === '') {
			return fail(400, {
				firstName,
				lastName,
				message: 'Last name is required'
			});
		}

		saveSession(cookies, { firstName, lastName });
		throw redirect(303, '/signup/review');
	}
};
