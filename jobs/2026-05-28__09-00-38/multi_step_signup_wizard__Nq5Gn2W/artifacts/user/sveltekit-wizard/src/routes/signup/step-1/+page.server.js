import { getSession, saveSession } from '$lib/server/session';
import { fail, redirect } from '@sveltejs/kit';

export function load({ cookies }) {
	const session = getSession(cookies);
	return {
		email: session.email ?? ''
	};
}

export const actions = {
	default: async ({ request, cookies }) => {
		const formData = await request.formData();
		const email = formData.get('email');

		if (!email || typeof email !== 'string' || !email.includes('@')) {
			return fail(400, {
				email,
				message: 'Invalid email address'
			});
		}

		saveSession(cookies, { email });
		throw redirect(303, '/signup/step-2');
	}
};
