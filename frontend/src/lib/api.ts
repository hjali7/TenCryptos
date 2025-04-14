export async function fetchCryptos() {
  const res = await fetch("http://localhost:8000/cryptos/db");

  if (!res.ok) {
    throw new Error("Failed to fetch cryptos");
  }

  return res.json();
}