'use client';

import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import Image from "next/image";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      role: "system",
      content: "✈️ Welcome! How can I help you with your flight booking?",
    },
  ]);
  const [input, setInput] = useState("");
  const chatEndRef = useRef(null);
  const [accessToken, setAccessToken] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    setAccessToken(token);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);

    const userInput = input;
    setInput("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/chat", userInput, {
        headers: {
          "Content-Type": "text/plain",
          Authorization: `Bearer ${accessToken}`,
        },
      });

      const botResponse = response?.data?.response || "No response received.";
      const botMsg = { role: "bot", content: botResponse };
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error("API error:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: "❌ Sorry, could not connect to the server.",
        },
      ]);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-sky-100 to-white">
      <Navbar />

      <div className="flex justify-center px-4 py-6 flex-1">
        <div className="relative w-full max-w-3xl h-[80vh] bg-white shadow-2xl rounded-2xl overflow-hidden flex flex-col border border-blue-200">

          {/* Header */}
          <div className="bg-blue-600 text-white py-4 px-6 text-lg font-semibold z-10">
            AI Flight Assistant Chat
          </div>

          {/* Chat Body with Background Image */}
          <div className="flex-1 overflow-y-auto relative z-0">
            {/* Background Image */}
            <div className="absolute inset-0 z-0">
              <Image
                src="/1.jpg"
                alt="Background"
                fill
                className="object-cover opacity-40"
              />
              <div className="absolute inset-0 bg-white opacity-10" /> {/* optional overlay */}
            </div>

            {/* Messages */}
            <div className="relative z-10 p-6 space-y-4">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${
                    msg.role === "user"
                      ? "justify-end"
                      : msg.role === "bot"
                      ? "justify-start"
                      : "justify-center"
                  }`}
                >
                  <div
                    className={`px-4 py-3 rounded-xl max-w-[80%] whitespace-pre-wrap animate-fade-in ${
                      msg.role === "user"
                        ? "bg-blue-600 text-white"
                        : msg.role === "bot"
                        ? "bg-white bg-opacity-90 text-blue-800"
                        : "bg-green-100 text-green-800 text-center"
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))}
              <div ref={chatEndRef} />
            </div>
          </div>

          {/* Input */}
          <div className="p-4 border-t bg-white flex gap-2 z-10">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
              className="flex-1 px-4 py-2 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
            <button
              onClick={sendMessage}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-xl transition"
            >
              Send
            </button>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
