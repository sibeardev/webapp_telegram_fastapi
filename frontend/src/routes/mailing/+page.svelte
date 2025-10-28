<script lang="ts">
  import { onMount } from "svelte";
  import WebApp from "@twa-dev/sdk";
  import { sendMailing } from "../../services/api";
  import { goto } from "$app/navigation";

  let errorMessage: string | null = null;
  let title = "";
  let text = "";

  async function handleSubmit() {
    const result = await sendMailing(title, text);
    alert(result);
    goto("/")
  }

  onMount(async () => {
    try {
      if (typeof window === "undefined") return;

      WebApp.BackButton.show();
      WebApp.BackButton.onClick(() => {
        history.back();
      });

      WebApp.SecondaryButton.hide();
      WebApp.ready();
      WebApp.expand();
    } catch (error: any) {
      errorMessage = error.message;
    }
  });
</script>

<div class="tg-secondary-bg p-6 rounded-2xl shadow-lg max-w-md w-full">
  {#if errorMessage}
    <p class="tg-destructive-text text-center">{errorMessage}</p>
  {:else}
    <h2 class="text-xl font-semibold mb-4 text-center">Create a mailing</h2>

    <form class="max-w-sm mx-auto" on:submit|preventDefault={handleSubmit}>
      <div class="mb-5">
        <input
          type="text"
          placeholder="Title"
          bind:value={title}
          class="bg-zinc-50 border border-zinc-300 text-zinc-900 tg-field text-sm rounded-lg block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white"
          required
        />
      </div>

      <div class="mb-5">
        <textarea
          placeholder="Text"
          bind:value={text}
          rows="5"
          class="bg-zinc-50 border border-zinc-300 text-zinc-900 tg-field text-sm rounded-lg block w-full p-2.5 dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white"
          required
        ></textarea>
      </div>
      <button
        type="submit"
        class="tg-button-bg tg-button-text focus:ring-4 focus:outline-none font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
        >Submit</button
      >
    </form>
  {/if}
</div>
