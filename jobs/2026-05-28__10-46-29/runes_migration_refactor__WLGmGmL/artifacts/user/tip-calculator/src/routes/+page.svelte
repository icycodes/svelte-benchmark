<script>
    import TipButton from '$lib/TipButton.svelte';

    let bill = $state(0);
    let people = $state(1);
    let tip = $state(5);

    const tipOptions = [5, 10, 15];

    const tipAmount = $derived(() => (Number(bill) || 0) * (Number(tip) || 0) / 100);
    const total = $derived(() => (Number(bill) || 0) + tipAmount);
    const perPerson = $derived(() => total / Math.max(1, Number(people) || 1));

    function handleSelect(value) {
        tip = value;
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
        <TipButton value={option} active={tip === option} onselect={handleSelect} />
    {/each}
</div>

<p>Tip: $<span data-testid="tip-amount">{tipAmount.toFixed(2)}</span></p>
<p>Total: $<span data-testid="total-amount">{total.toFixed(2)}</span></p>
<p>Per person: $<span data-testid="per-person">{perPerson.toFixed(2)}</span></p>
