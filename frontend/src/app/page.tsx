import { Crypto } from "@/../types/crypto"
import { fetchCryptos } from "@/lib/api"

export default async function Home() {
  const data: Crypto[] = await fetchCryptos()

  return (
    <main className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">💰 Top 10 Cryptos</h1>
      <ul className="space-y-3">
        {data.map((crypto) => (
          <li
            key={crypto.symbol}
            className="bg-gray-900 rounded-lg p-4 flex justify-between items-center shadow-md"
          >
            <div>
              <p className="text-lg font-semibold">{crypto.name}</p>
              <p className="text-sm text-gray-400 uppercase">{crypto.symbol}</p>
            </div>
            <div className="text-right">
              <p>${crypto.price_usd.toFixed(2)}</p>
            </div>
          </li>
        ))}
      </ul>
    </main>
  )
}