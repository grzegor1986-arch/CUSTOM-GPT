export const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function checkout() {
  const res = await fetch(`${API_URL}/checkout`);
  if (!res.ok) {
    throw new Error("Checkout request failed");
  }
  return res.json();
}
