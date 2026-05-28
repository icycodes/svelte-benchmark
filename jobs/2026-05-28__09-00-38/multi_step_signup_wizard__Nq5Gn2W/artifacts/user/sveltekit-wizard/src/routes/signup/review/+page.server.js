import { getSession, clearSession } from '$lib/server/session';
import { fail, redirect } from '@sveltejs/kit';
import fs from 'node:fs/promises';
import path from 'node:path';

export function load({ cookies }) {
	const session = getSession(cookies);
	if (!session.email) throw redirect(303, '/signup/step-1');
	if (!session.password) throw redirect(303, '/signup/step-2');
	if (!session.firstName || !session.lastName) throw redirect(303, '/signup/step-3');

	return {
		email: session.email,
		firstName: session.firstName,
		lastName: session.lastName
	};
}

export const actions = {
	default: async ({ cookies }) => {
		const session = getSession(cookies);
		
		if (!session.email || !session.password || !session.firstName || !session.lastName) {
			return fail(400, { message: 'Missing data' });
		}

		const userRecord = {
			email: session.email,
			firstName: session.firstName,
			lastName: session.lastName,
			passwordLength: session.password.length
		};

		const dataDir = path.resolve('data');
		const filePath = path.join(dataDir, 'users.json');

		try {
			await fs.mkdir(dataDir, { recursive: true });
			let users = [];
			try {
				const content = await fs.readFile(filePath, 'utf-8');
				users = JSON.parse(content);
			} catch (e) {
				// File doesn't exist or is invalid, start with empty array
			}
			users.push(userRecord);
			await fs.writeFile(filePath, JSON.stringify(users, null, 2));
		} catch (err) {
			console.error('Failed to save user:', err);
			return fail(500, { message: 'Failed to save user data' });
		}

		const email = session.email;
		clearSession(cookies);
		throw redirect(303, `/signup/done?email=${encodeURIComponent(email)}`);
	}
};
