import { redirect, fail } from "@sveltejs/kit";
import { g as getSession, c as clearSession } from "../../../../chunks/session.js";
import { readFile, mkdir, writeFile } from "fs/promises";
import { join } from "path";
const DATA_DIR = "data";
const USERS_FILE = join(DATA_DIR, "users.json");
function load({ cookies }) {
  const { data } = getSession(cookies);
  if (!data.email) {
    redirect(303, "/signup/step-1");
  }
  if (!data.password) {
    redirect(303, "/signup/step-2");
  }
  if (!data.firstName || !data.lastName) {
    redirect(303, "/signup/step-3");
  }
  return {
    email: data.email,
    firstName: data.firstName,
    lastName: data.lastName
  };
}
const actions = {
  default: async ({ cookies }) => {
    const { data } = getSession(cookies);
    if (!data.email) {
      redirect(303, "/signup/step-1");
    }
    if (!data.password) {
      redirect(303, "/signup/step-2");
    }
    if (!data.firstName || !data.lastName) {
      redirect(303, "/signup/step-3");
    }
    const { email, password, firstName, lastName } = data;
    if (!email || !password || !firstName || !lastName) {
      return fail(400, { message: "Incomplete signup data. Please start again." });
    }
    let users = [];
    try {
      const raw = await readFile(USERS_FILE, "utf-8");
      users = JSON.parse(raw);
    } catch {
    }
    const newUser = {
      email,
      firstName,
      lastName,
      passwordLength: password.length
    };
    users.push(newUser);
    await mkdir(DATA_DIR, { recursive: true });
    await writeFile(USERS_FILE, JSON.stringify(users, null, 2), "utf-8");
    clearSession(cookies);
    redirect(303, `/signup/done?email=${encodeURIComponent(email)}`);
  }
};
export {
  actions,
  load
};
