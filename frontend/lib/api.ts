const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchCompanies() {
  const res = await fetch(`${BASE_URL}/companies`);
  return res.json();
}

export async function fetchCompany(id: string) {
  const res = await fetch(`${BASE_URL}/companies/${id}`);
  return res.json();
}

export async function fetchTrends() {
  const res = await fetch(`${BASE_URL}/trends`);
  return res.json();
}

export async function askQuestion(question: string) {
  const res = await fetch(`${BASE_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });
  return res.json();
}