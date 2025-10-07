<script lang="ts">
  import favicon from "$lib/assets/favicon.svg";
  import "../app.css";
  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<main class="min-h-screen flex items-center justify-center p-4">
  {@render children?.()}
</main>
