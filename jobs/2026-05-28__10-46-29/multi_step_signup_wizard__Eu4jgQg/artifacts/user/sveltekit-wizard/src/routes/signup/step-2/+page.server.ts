import { redirect, fail } from '@sveltejs/kit';
import { getSession, saveSession } from '$lib/server/session';

export function load({ cookies }) {
	const session = getSession(cookies);
	if (!session || !session.email) {
		redirect(303, '/signup/step-1');
	}
	return {};
}

export const actions = {
	default: async ({ request, cookies }) => {
		const data = await request.formData();
		const password = data.get('password');
		const confirmPassword = data.get('confirmPassword');

		if (!password || typeof password !== 'string' || password.length < 8) {
			return fail(400, { error: 'Password must be at least 8 characters long' });
		}
		if (password !== confirmPassword) {
			return fail(400, { error: 'Passwords do not match' });
		}

		const session = getSession(cookies);
		if (!session) {
			redirect(303, '/signup/step-1');
		}
		
		session.passwordLength = password.length;
		session.password = password; // we keep it in session for now, but remove on final review
		saveSession(cookies, session);

		redirect(303, '/signup/step-3');
	}
};
