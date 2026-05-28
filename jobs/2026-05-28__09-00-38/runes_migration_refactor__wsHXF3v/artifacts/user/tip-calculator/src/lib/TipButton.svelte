<script>
    let { value = 0, active = false, onselect } = $props();

    function handleClick() {
        if (onselect) {
            onselect(value);
        }
    }
</script>

<button
    type="button"
    class:selected={active}
    data-testid={'tip-' + value}
    onclick={handleClick}
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
