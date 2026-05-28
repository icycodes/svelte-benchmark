import { fail, redirect } from '@sveltejs/kit';
import { mkdir, readFile, writeFile } from 'fs/promises';
import path from 'path';
import { getSession, clearSession } from '$lib/server/session';

const usersFilePath = path.resolve('data', 'users.json');

const getRedirectForMissingData = (data) => {
  if (!data.email) return '/signup/step-1';
  if (!data.password) return '/signup/step-2';
  if (!data.firstName || !data.lastName) return '/signup/step-3';
  return null;
};

export const load = ({ cookies }) => {
  const session = getSession(cookies);
  const redirectTo = getRedirectForMissingData(session.data);

  if (redirectTo) {
    redirect(303, redirectTo);
  }

  return {
    values: {
      email: session.data.email,
      firstName: session.data.firstName,
      lastName: session.data.lastName
    }
  };
};

export const actions = {
  default: async ({ cookies }) => {
    const session = getSession(cookies);
    const redirectTo = getRedirectForMissingData(session.data);

    if (redirectTo) {
      redirect(303, redirectTo);
    }

    const { email, firstName, lastName, password } = session.data;

    if (!email || !firstName || !lastName || !password) {
      return fail(400, { error: 'Missing signup data. Please restart the wizard.' });
    }

    await mkdir(path.dirname(usersFilePath), { recursive: true });

    let users = [];
    try {
      const existing = await readFile(usersFilePath, 'utf-8');
      const parsed = JSON.parse(existing);
      if (Array.isArray(parsed)) {
        users = parsed;
      }
    } catch (error) {
      if (error.code !== 'ENOENT') {
        throw error;
      }
    }

    users.push({
      email,
      firstName,
      lastName,
      passwordLength: password.length
    });

    await writeFile(usersFilePath, JSON.stringify(users, null, 2));

    clearSession(cookies);

    redirect(303, `/signup/done?email=${encodeURIComponent(email)}`);
  }
};
