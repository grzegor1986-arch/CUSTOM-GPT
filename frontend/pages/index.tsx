import { checkout } from "../lib/api";

export default function Home() {
  const handleCheckout = async () => {
    const data = await checkout();
    window.location.href = data.url;
  };

  return (
    <main style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>AI SaaS</h1>
      <p>Production-ready minimal checkout flow.</p>
      <button onClick={handleCheckout}>Buy Now</button>
    </main>
  );
}
