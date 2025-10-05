import WebApp from "@twa-dev/sdk";


export async function authorizeUser() {
    if (!WebApp.initDataUnsafe?.user?.id) {
        throw new Error("Launch the application inside Telegram");
    }
    const res = await fetch("/api/user/auth", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            initData: WebApp.initData,
            initDataUnsafe: WebApp.initDataUnsafe,
        }),
    });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(`Authorization failed: ${text}`);
    }

    return await res.json();
}
