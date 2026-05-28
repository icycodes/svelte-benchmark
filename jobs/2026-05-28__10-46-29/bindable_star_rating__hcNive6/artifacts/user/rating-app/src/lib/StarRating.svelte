<script>
  let { value = $bindable(0), max = 5 } = $props();

  const stars = Array.from({ length: max }, (_, index) => index + 1);
</script>

<div class="stars" role="radiogroup" aria-label="Star rating">
  {#each stars as rating}
    <button
      type="button"
      class="star"
      class:filled={rating <= value}
      data-filled={rating <= value}
      aria-checked={rating === value}
      aria-label={`Set rating to ${rating}`}
      on:click={() => (value = rating)}
    >
      ★
    </button>
  {/each}
</div>

<style>
  .stars {
    display: inline-flex;
    gap: 0.25rem;
  }

  .star {
    border: none;
    background: transparent;
    font-size: 2rem;
    color: #9ca3af;
    cursor: pointer;
    padding: 0;
  }

  .star.filled {
    color: #f59e0b;
  }
</style>
