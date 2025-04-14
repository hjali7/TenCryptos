"use client";

import { useEffect, useState } from "react";

type Crypto = {
  symbol: string;
  name: string;
  price_usd: number;
};

export default function Home() {
  const [cryptos, setCryptos] = useState<Crypto[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://localhost:8000/cryptos/db");

        if (!res.ok) {
          throw new Error("Failed to fetch cryptos");
        }

        const data = await res.json();
        setCryptos(data);
      } catch (err: any) {
        console.error("⛔ Error fetching:", err.message);
        setError(err.message);
      }
    };

    fetchData();
  }, []);

  return (
    <main className="p-4">
      <h1 className="text-2xl font-bold mb-4">Top 10 Cryptocurrencies</h1>

      {error && <p className="text-red-500">Error: {error}</p>}

      <ul>
        {cryptos.map((crypto) => (
          <li key={crypto.symbol} className="mb-2">
            <strong>{crypto.name}</strong> ({crypto.symbol.toUpperCase()}): ${crypto.price_usd}
          </li>
        ))}
      </ul>
    </main>
  );
}
