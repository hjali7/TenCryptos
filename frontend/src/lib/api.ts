export async function fetchCryptos() {
    const res = await fetch("http://127.0.0.1:8000/cryptos", {
      next: { revalidate: 0 },
    });
  
    if (!res.ok) {
      throw new Error("Failed to fetch cryptos");
    }
  
    return res.json();
  }
  