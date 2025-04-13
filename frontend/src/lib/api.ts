export async function fetchCryptos() {
  const res = await fetch("/api/cryptos", {
    next: { revalidate: 0 },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch cryptos");
  }

  return res.json();
}