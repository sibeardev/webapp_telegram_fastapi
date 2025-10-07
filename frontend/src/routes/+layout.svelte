<script lang="ts">
  import favicon from "$lib/assets/favicon.svg";
  import "../app.css";
  import { onMount } from "svelte";
  import WebApp from "@twa-dev/sdk";

  let { children } = $props();
  onMount(() => {
    WebApp.ready();
  });
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<main class="min-h-screen flex items-center justify-center p-4 tg-bg tg-text">
  {@render children?.()}
</main>
