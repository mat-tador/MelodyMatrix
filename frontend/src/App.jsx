import React from "react";
import MusicChatbot from "./components/MusicChatbot";

function App() {
  return (
    <div style={{ minHeight: "100vh", background: "#f7f4ef" }}>
      
      {/* Your App Content */}
      <h1 style={{ textAlign: "center", paddingTop: "40px" }}>
        🎵 Melody Matrix
      </h1>

      <p style={{ textAlign: "center" }}>
        Your AI-powered music assistant
      </p>

      {/* Chatbot always available */}
      <MusicChatbot />
    </div>
  );
}

export default App;