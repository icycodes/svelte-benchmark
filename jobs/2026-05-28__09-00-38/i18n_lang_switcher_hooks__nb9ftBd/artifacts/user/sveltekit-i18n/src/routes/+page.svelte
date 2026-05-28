<script>
	import { enhance } from '$app/forms';
	import { translations } from '$lib/i18n';

	let { data } = $props();
	let currentLocale = $derived(data.locale);
	let greeting = $derived(translations[currentLocale].greeting);
</script>

<h1>{greeting}</h1>

<p>
	Current locale: <span data-testid="current-locale">{currentLocale}</span>
</p>

<form method="POST" use:enhance>
	<button type="submit" name="locale" value="en" data-testid="locale-btn-en">English</button>
	<button type="submit" name="locale" value="de" data-testid="locale-btn-de">Deutsch</button>
	<button type="submit" name="locale" value="fr" data-testid="locale-btn-fr">Français</button>
</form>
