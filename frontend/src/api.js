// import { useAuthStore } from "store/auth";
import { create } from "zustand";

export const useAuthStore = create(set => ({
  token: null,
  setToken: (token) => set({ token }),
  logout: () => set({ token: null }),
}));

export async function login(email, password) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const res = await fetch("http://localhost:8000/auth/token", {
        method: "POST",
        body: formData,
    });
    return await res.json();
}

export async function apiFetch(url, options = {}) {
  const token = useAuthStore.getState().token;

  const headers = {
    "Content-Type": "application/json",
    // ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`http://localhost:8000${url}`, {
    ...options,
    headers,
    credentials: "include", // ВАЖНО: отправлять cookie
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "API error");
  }

  return response.json();
}

export function getResumes() {
  return apiFetch("/resumes");
}

export function createResume(data) {
  return apiFetch("/resumes", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function getResume(id) {
  return apiFetch(`/resumes/${id}`);
}

export function improveResume(id) {
  return apiFetch(`/resumes/${id}/improve`, {
    // method: "POST",
  });
}
