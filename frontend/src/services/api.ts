import { goto } from "$app/navigation";

export async function authorizeUser(
  initData: string,
  initDataUnsafe: Record<string, any>
) {
  const res = await fetch("/api/user/auth", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      initData: initData,
      initDataUnsafe: initDataUnsafe,
    }),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data?.detail || "Auth failed");
  }

  return await res.json();
}

export async function getUser(token: string) {
  const res = await fetch("/api/user/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    localStorage.removeItem("token");
    goto("/auth");
    return;
  }

  return await res.json();
}

export async function sendMailing(title: string, text: string) {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      localStorage.removeItem("token");
      goto("/auth");
      return;
    }

    const response = await fetch("/api/mailing/bulk", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title, text }),
    });

    const result = await response.json();
    return result.status === "ok"
      ? "Message sent"
      : result.detail || "Mailing error";
  } catch (err) {
    return "Server error";
  }
}
