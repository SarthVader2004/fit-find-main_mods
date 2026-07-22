import React, { useState } from "react";
import axios from "axios";
import MessageBubble from "./MessageBubble";
import Loader from "./Loader";

const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      type: "bot",
      text: "👋 Hi! I'm FitFind — ask me about outfits, colors, or occasions.",
    },
  ]);
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const q = userInput.trim();
    if (!q) return;

    // Show user message immediately
    setMessages((prev) => [...prev, { type: "user", text: q }]);
    setUserInput("");
    setLoading(true);

    try {
      // Call backend
      const res = await axios.post("/api/chat", { query: q });
      const data = res.data || {};
      console.log("🧩 Backend response:", data);

      let replyText = "";

      // 🧠 CASE 1: Combined (FitFind + Groq)
      if (data.intent === "combined") {
        replyText =
          `🧠 FitFind Insight:\n${data.fitfind_response || ""}\n\n` +
          (data.fitfind_explanation
            ? data.fitfind_explanation.join("\n") + "\n\n"
            : "") +
          `🪄 Groq Stylist:\n${data.groq_response || ""}`;
      }
      // 🧠 CASE 2: FitFind only
      else if (data.intent === "fitfind") {
        replyText =
          `🧠 FitFind Insight:\n${data.response || ""}\n\n` +
          (data.explanation ? data.explanation.join("\n") : "");
      }
      // 🪄 CASE 3: Groq fallback only
      else if (data.intent === "fallback") {
        replyText = `🪄 Groq Stylist:\n${data.response || ""}`;
      }
      // ⚠️ Default fallback
      else {
        replyText =
          data.response ||
          data.fitfind_response ||
          data.groq_response ||
          "⚠️ No response from FitFind.";
      }

      // Push bot message
      setMessages((prev) => [...prev, { type: "bot", text: replyText }]);
    } catch (error) {
      console.error("⚠️ Backend error:", error);
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: "⚠️ Backend error. Is the API running?" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-window">
        {messages.map((m, i) => (
          <MessageBubble key={i} msg={m} />
        ))}
        {loading && <Loader />}
      </div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="e.g., pastel saree for wedding"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          onKeyDown={(e) => (e.key === "Enter" ? sendMessage() : null)}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
