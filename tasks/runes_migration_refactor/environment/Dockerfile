FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep \
        ffmpeg libxcb-shm0 libx11-xcb1 libx11-6 libxcb1 libxext6 libxrandr2 libxcomposite1 \
        libxcursor1 libxdamage1 libxfixes3 libxi6 libgtk-3-0t64 libpangocairo-1.0-0 \
        libpango-1.0-0 libatk1.0-0t64 libcairo-gobject2 libcairo2 libgdk-pixbuf-2.0-0 \
        libxrender1 libasound2t64 libfreetype6 libfontconfig1 libdbus-1-3 libnss3 libnspr4 \
        libatk-bridge2.0-0t64 libdrm2 libxkbcommon0 libatspi2.0-0t64 libcups2t64 \
        libxshmfence1 libgbm1 && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g agent-browser && \
    agent-browser install && \
    pip3 install --break-system-packages pytest-json-ctrf pytest-xprocess pochi-verifier && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

# Scaffold a minimal SvelteKit (Svelte 5) project at /home/user/tip-calculator.
RUN cd /home/user && \
    npx --yes sv create tip-calculator \
        --template minimal \
        --no-types \
        --no-add-ons \
        --install npm \
        --no-dir-check

# Replace the default route with a Svelte 4 style Tip Calculator that the
# executor will migrate to Svelte 5 runes.
RUN mkdir -p /home/user/tip-calculator/src/lib /home/user/tip-calculator/src/routes

RUN cat >/home/user/tip-calculator/src/lib/TipButton.svelte <<'EOF'
<script>
    import { createEventDispatcher } from 'svelte';

    export let value = 0;
    export let active = false;

    const dispatch = createEventDispatcher();

    function handleClick() {
        dispatch('select', value);
    }
</script>

<button
    type="button"
    class:selected={active}
    data-testid={'tip-' + value}
    on:click={handleClick}
>
    {value}%
</button>

<style>
    button {
        padding: 0.5rem 1rem;
        margin-right: 0.5rem;
        border: 1px solid #888;
        background: #fff;
        cursor: pointer;
        border-radius: 4px;
    }
    button.selected {
        background: #1e88e5;
        color: #fff;
        border-color: #1565c0;
    }
</style>
EOF

RUN cat >/home/user/tip-calculator/src/routes/+page.svelte <<'EOF'
<script>
    import TipButton from '$lib/TipButton.svelte';

    export let bill = 0;
    export let people = 1;
    export let tip = 5;

    const tipOptions = [5, 10, 15];

    $: tipAmount = (Number(bill) || 0) * (Number(tip) || 0) / 100;
    $: total = (Number(bill) || 0) + tipAmount;
    $: perPerson = total / Math.max(1, Number(people) || 1);

    function handleSelect(event) {
        tip = event.detail;
    }
</script>

<h1>Tip Calculator</h1>

<label>
    Bill:
    <input
        type="number"
        min="0"
        step="0.01"
        data-testid="bill-input"
        bind:value={bill}
    />
</label>

<label>
    People:
    <input
        type="number"
        min="1"
        step="1"
        data-testid="people-input"
        bind:value={people}
    />
</label>

<div>
    {#each tipOptions as option}
        <TipButton value={option} active={tip === option} on:select={handleSelect} />
    {/each}
</div>

<p>Tip: $<span data-testid="tip-amount">{tipAmount.toFixed(2)}</span></p>
<p>Total: $<span data-testid="total-amount">{total.toFixed(2)}</span></p>
<p>Per person: $<span data-testid="per-person">{perPerson.toFixed(2)}</span></p>
EOF

# Make sure dependencies installed by `sv create` are present (idempotent).
RUN cd /home/user/tip-calculator && npm install

LABEL Author="generate-harbor-tasks"
LABEL Description="SvelteKit (Svelte 5) tip calculator pre-populated with Svelte 4 idioms for a runes migration task; browser verification dependencies included."

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]

# Container contents:
#   - always required apt packages: curl wget ca-certificates git python3 python3-pip python3-pytest bash ripgrep
#   - always required pip3 packages: pytest-json-ctrf
#   - Node.js v24 for running the SvelteKit dev server
#   - browser verification dependencies: pochi-verifier, agent-browser, ffmpeg, and more
#   - pytest-xprocess: used by the final-state test to run the dev server in the background
#   - /home/user/tip-calculator: minimal SvelteKit (Svelte 5) project scaffolded with `sv create`
#   - /home/user/tip-calculator/src/routes/+page.svelte: Tip Calculator page using Svelte 4 idioms
#   - /home/user/tip-calculator/src/lib/TipButton.svelte: reusable button component using Svelte 4 idioms
