// const API_HOST = "http://localhost";
const API_HOST = "http://resume.tripleap.ru";

export async function apiFetch(url, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  const response = await fetch(`${API_HOST}/api${url}`, {
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

export async function login(email, password) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  return apiFetch("/auth/token", {
    method: "POST",
    body: formData,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  })
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
  });
}
