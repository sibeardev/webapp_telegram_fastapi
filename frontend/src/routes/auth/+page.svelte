<script lang="ts">
  import { onMount } from "svelte";
  import WebApp from "@twa-dev/sdk";
  import { authorizeUser } from "../../services/api";
  import { goto } from "$app/navigation";

  let errorMessage: string | null = null;

  onMount(async () => {
    try {
      if (typeof window === "undefined") return;
      const initData = WebApp.initData;
      const initDataUnsafe = WebApp.initDataUnsafe;

      if (!WebApp.initDataUnsafe?.user?.id) {
        throw new Error("Launch the application inside Telegram");
      }

      const access_token = await authorizeUser(initData, initDataUnsafe);
      localStorage.setItem("token", access_token);
      WebApp.ready();
      WebApp.expand();
      goto("/");
    } catch (error: any) {
      errorMessage = error.message || "Auth failed";
    }
  });
</script>
