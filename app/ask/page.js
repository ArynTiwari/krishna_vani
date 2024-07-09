export default async function handler(req, res) {
  if (req.method === "POST") {
    const { question } = req.body;

    const response = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();
    res?.status(200).json({ answer: data.answer });
  } else {
    res?.status(405).json({ message: "Only POST requests allowed" });
  }
}
