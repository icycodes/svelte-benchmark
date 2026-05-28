import { redirect, fail } from '@sveltejs/kit';
import { getSession, clearSession } from '$lib/server/session';
import fs from 'fs/promises';
import path from 'path';

export function load({ cookies }) {
	const session = getSession(cookies);
	if (!session || !session.email) {
		redirect(303, '/signup/step-1');
	}
	if (!session.password) {
		redirect(303, '/signup/step-2');
	}
	if (!session.firstName || !session.lastName) {
		redirect(303, '/signup/step-3');
	}
	
	return {
		email: session.email,
		firstName: session.firstName,
		lastName: session.lastName,
		passwordLength: session.passwordLength
	};
}

export const actions = {
	default: async ({ cookies }) => {
		const session = getSession(cookies);
		if (!session || !session.email || !session.password || !session.firstName || !session.lastName) {
			return fail(400, { error: 'Missing required fields' });
		}

		const userRecord = {
			email: session.email,
			firstName: session.firstName,
			lastName: session.lastName,
			passwordLength: session.passwordLength
		};

		const dataDir = path.resolve('data');
		const usersFile = path.join(dataDir, 'users.json');

		try {
			await fs.mkdir(dataDir, { recursive: true });
			let users = [];
			try {
				const fileContent = await fs.readFile(usersFile, 'utf-8');
				users = JSON.parse(fileContent);
			} catch (e) {
				// File doesn't exist or invalid JSON
			}
			users.push(userRecord);
			await fs.writeFile(usersFile, JSON.stringify(users, null, 2));
		} catch (e) {
			console.error('Error saving user:', e);
			return fail(500, { error: 'Internal server error' });
		}

		clearSession(cookies);
		redirect(303, `/signup/done?email=${encodeURIComponent(userRecord.email)}`);
	}
};
