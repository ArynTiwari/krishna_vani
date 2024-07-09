"use client";
import Image from "next/image";
import { useState } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [count, setCount] = useState(0);
  const handleAsk = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setAnswer(data.answer);
    } catch (error) {
      console.error("Error:", error);
    }
  };
  console.log("This is the question", question);
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center py-12 px-6 lg:px-8">
      <h1 className="text-3xl font-extrabold text-gray-900 mb-8">
        Ask a Question
      </h1>
      <form
        onSubmit={handleAsk}
        className="w-full max-w-md bg-white p-8 rounded-lg shadow-md"
      >
        <div className="mb-4">
          <input
            className="w-full px-4 py-2 border border-gray-300 rounded-md text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Type your question here..."
          />
        </div>
        <div className="flex justify-center">
          <button
            type="submit"
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            Ask
          </button>
        </div>
      </form>
      {answer && (
        <div className="mt-8 bg-white p-6 rounded-lg shadow-md w-full max-w-md">
          <p className="text-lg font-medium text-gray-900">Answer:</p>
          <p className="text-gray-700 mt-2">{answer}</p>
        </div>
      )}
    </div>
  );
}
