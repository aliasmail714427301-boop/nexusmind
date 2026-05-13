"use client";

import { useState } from "react";

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "👋 مرحبًا! أنا NexusMind AI",
    },
  ]);

  const sendMessage = async () => {
    if (!input) return;

    setMessages((prev: any) => [
      ...prev,
      {
        role: "user",
        content: input,
      },
    ]);

    const repo = input;
    setInput("");

    try {
      const response = await fetch(
        "https://nexusmind-production-62a4.up.railway.app/repos",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            repo_url: `https://github.com/facebook/${repo}`,
          }),
        }
      );

      const data = await response.json();

      setMessages((prev: any) => [
        ...prev,
        {
          role: "assistant",
          content: JSON.stringify(data, null, 2),
        },
      ]);
    } catch (error) {
      setMessages((prev: any) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Failed to fetch",
        },
      ]);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white flex flex-col">
      <div className="p-4 border-b border-zinc-800">
        <h1 className="text-2xl font-bold">
          NexusMind AI 🚀
        </h1>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg: any, index: number) => (
          <div
            key={index}
            className={`max-w-[85%] rounded-3xl p-4 whitespace-pre-wrap ${
              msg.role === "user"
                ? "bg-blue-600 ml-auto"
                : "bg-zinc-900"
            }`}
          >
            {msg.content}
          </div>
        ))}
      </div>

      <div className="p-4 border-t border-zinc-800 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="اكتب Repository مثل react"
          className="flex-1 bg-zinc-900 border border-zinc-700 rounded-2xl px-4 py-3 outline-none"
        />

        <button
          onClick={sendMessage}
          className="bg-blue-600 px-6 py-3 rounded-2xl font-bold"
        >
          إرسال
        </button>
      </div>
    </main>
  );
}
