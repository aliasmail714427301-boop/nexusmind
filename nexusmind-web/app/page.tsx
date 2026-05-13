"use client";

import { useState } from "react";

export default function Home() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "👋 مرحباً! أنا NexusMind AI",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      role: "user",
      content: input,
    };

    setMessages((prev: any) => [...prev, userMessage]);

    const currentInput = input;

    setInput("");
    setLoading(true);

    try {
      const response = await fetch(
        "https://nexusmind-production-62a4.up.railway.app/repos",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            repo_name: currentInput,
          }),
        }
      );

      const data = await response.json();

      const botMessage = {
        role: "assistant",
        content: JSON.stringify(data, null, 2),
      };

      setMessages((prev: any) => [...prev, botMessage]);
    } catch (error: any) {
      console.log(error);

      setMessages((prev: any) => [
        ...prev,
        {
          role: "assistant",
          content:
            "❌ " + (error?.message || "خطأ غير معروف"),
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <main className="bg-black text-white min-h-screen flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-800">
        <h1 className="text-2xl font-bold">
          NexusMind AI 🚀
        </h1>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg: any, index) => (
          <div
            key={index}
            className={`max-w-[85%] p-4 rounded-3xl whitespace-pre-wrap ${
              msg.role === "user"
                ? "bg-blue-600 ml-auto"
                : "bg-zinc-900"
            }`}
          >
            {msg.content}
          </div>
        ))}

        {loading && (
          <div className="bg-zinc-900 p-4 rounded-3xl w-fit">
            ⏳ جاري التحليل...
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-800 flex gap-2">
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
