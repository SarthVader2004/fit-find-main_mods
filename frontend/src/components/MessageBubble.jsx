import React from "react";

const MessageBubble = ({ msg }) => {
  const isUser = msg.type === "user";
  const isBot = msg.type === "bot";

  return (
    <div className={`message-bubble ${msg.type}`}>
      <div
        className={`bubble-content ${
          isUser ? "user-bubble" : isBot ? "bot-bubble" : ""
        }`}
      >
        {/* Preserve emojis, newlines, and formatting */}
        <pre style={{ whiteSpace: "pre-wrap", margin: 0 }}>{msg.text}</pre>

        {/* Optional explanation section */}
        {Array.isArray(msg.explanation) && msg.explanation.length > 0 && (
          <div className="explanation">
            <strong>🧠 Why:</strong>
            <ul>
              {msg.explanation.map((e, idx) => (
                <li key={idx}>{e}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
