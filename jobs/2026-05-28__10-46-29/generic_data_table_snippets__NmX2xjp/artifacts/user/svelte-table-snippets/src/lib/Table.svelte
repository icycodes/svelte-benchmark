<script lang="ts">
  type TableProps<T> = {
    data: T[];
    header: () => unknown;
    row: (item: T) => unknown;
  };

  const { data, header, row } = $props<TableProps<unknown>>();
</script>

<table>
  <thead>
    <tr>
      {@render header()}
    </tr>
  </thead>
  <tbody>
    {#each data as item}
      <tr>
        {@render row(item)}
      </tr>
    {/each}
  </tbody>
</table>
