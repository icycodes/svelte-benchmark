import { redirect, fail } from '@sveltejs/kit';
import { getSession, saveSession } from '$lib/server/session';

export function load({ cookies }) {
	const session = getSession(cookies) || {};
	return { email: session.email || '' };
}

export const actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();
		const email = data.get('email');

		if (!email || typeof email !== 'string' || !email.includes('@')) {
			return fail(400, { email, error: 'Invalid email address' });
		}

		const session = getSession(cookies) || {};
		session.email = email;
		saveSession(cookies, session);

		redirect(303, '/signup/step-2');
	}
};
