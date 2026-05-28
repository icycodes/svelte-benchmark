<script>
	import { enhance } from '$app/forms';
	import { greetings } from '$lib/i18n.js';

	let { data } = $props();
</script>

<h1>{greetings[data.locale]}</h1>

<div data-testid="current-locale">{data.locale}</div>

<form method="POST" use:enhance>
	<button type="submit" name="locale" value="en" data-testid="locale-btn-en">English</button>
	<button type="submit" name="locale" value="de" data-testid="locale-btn-de">Deutsch</button>
	<button type="submit" name="locale" value="fr" data-testid="locale-btn-fr">Français</button>
</form>
