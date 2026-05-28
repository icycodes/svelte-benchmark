<script>
	import { enhance } from '$app/forms';
	import { defaultLocale, translations } from '$lib/i18n';

	const { data } = $props();
	const currentLocale = $derived(data.locale ?? defaultLocale);
	const greeting = $derived(translations[currentLocale] ?? translations[defaultLocale]);
</script>

<main>
	<h1>{greeting}</h1>
	<p data-testid="current-locale">{currentLocale}</p>

	<form method="POST" use:enhance>
		<button type="submit" name="locale" value="en" data-testid="locale-btn-en">English</button>
		<button type="submit" name="locale" value="de" data-testid="locale-btn-de">Deutsch</button>
		<button type="submit" name="locale" value="fr" data-testid="locale-btn-fr">Français</button>
	</form>
</main>
