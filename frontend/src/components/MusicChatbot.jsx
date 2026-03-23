import React, { useState } from "react";
import "./MusicChatbot.css";

function MusicChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! I'm your music assistant." }
  ]);
  const [input, setInput] = useState("");

  const toggleChat = () => setIsOpen(!isOpen);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const currentInput = input;
    const userMessage = { sender: "user", text: currentInput };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const response = await fetch("http://localhost:5001/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: currentInput })
      });

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: data.reply || "No reply received." }
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Backend connection failed." }
      ]);
    }
  };

  return (
    <div>
      <button className="chat-button" onClick={toggleChat}>
        💬
      </button>

      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">Music Assistant</div>

          <div className="chat-body">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
          </div>

          <div className="chat-footer">
            <input
              type="text"
              placeholder="Ask about music..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") sendMessage();
              }}
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default MusicChatbot;