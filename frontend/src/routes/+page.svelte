<script lang="ts">
  import { onMount } from "svelte";
  import WebApp from "@twa-dev/sdk";
  import { getUser } from "../services/api";
  import { goto } from "$app/navigation";
  let user: any = null;
  let errorMessage: string | null = null;

  onMount(async () => {
    try {
      if (typeof window === "undefined") return;

      if (!WebApp.initDataUnsafe?.user?.id) {
        throw new Error("Launch the application inside Telegram");
      }

      const token = localStorage.getItem("token");
      if (!token) {
        goto("/auth");
        return;
      }
      user = await getUser(token);
      WebApp.ready();
      WebApp.expand();
    } catch (error: any) {
      errorMessage = error.message;
    }
  });
</script>

<div class="tg-secondary-bg p-6 rounded-2xl shadow-lg max-w-md w-full">
  <h1 class="tg-accent-text text-2xl font-bold mb-4 text-center">Profile</h1>
  {#if errorMessage}
    <p class="text-red-500 text-center">{errorMessage}</p>
  {:else if user}
    <div class="space-y-3 text-center">
      <div class="flex justify-center mb-4">
        {#if user.photo_url}
          <img
            class="w-24 h-24 rounded-full object-cover border-2 shadow-lg"
            src={user.photo_url}
            alt={user.username}
          />
        {:else}
          <div
            class="relative w-24 h-24 flex items-center justify-center overflow-hidden bg-gray-700 rounded-full shadow-lg"
          >
            <svg
              class="w-12 h-12 text-gray-400"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                clip-rule="evenodd"
              ></path>
            </svg>
          </div>
        {/if}
      </div>
      <p><span class="font-semibold tg-hint-text">ID:</span> {user.user_id}</p>
      <p>
        <span class="font-semibold tg-hint-text">First name:</span>
        {user.first_name}
      </p>
      {#if user.last_name}
        <p>
          <span class="font-semibold tg-hint-text">Last name:</span>
          {user.last_name}
        </p>
      {/if}
      {#if user.username}
        <p>
          <span class="font-semibold tg-hint-text">Username:</span>
          @{user.username}
        </p>
      {/if}
      <p>
        <span class="font-semibold tg-hint-text">Language:</span>
        {user.language_code}
      </p>
      {#if user.is_premium}
        <p class="text-yellow-400 font-semibold">⭐ Premium user</p>
      {/if}
    </div>
  {:else}
    <p class="tg-destructive-text text-center">User not found</p>
  {/if}
</div>
