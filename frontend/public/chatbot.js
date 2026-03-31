(function () {
  const BACKEND_URL = "http://localhost:5001/api/chat";

  function createMessage(text, className) {
    const div = document.createElement("div");
    div.className = className;
    div.textContent = text;
    return div;
  }

  function scrollToBottom(container) {
    container.scrollTop = container.scrollHeight;
  }

  function getValue(selectors) {
    for (const selector of selectors) {
      const el = document.querySelector(selector);
      if (el) {
        if (el.type === "checkbox") return el.checked;
        return el.value;
      }
    }
    return null;
  }

  function getDashboardState() {
    return {
      genre: getValue(["#genre", "select[name='genre']", ".genre-select"]),
      scale: getValue(["#scale", "select[name='scale']", ".scale-select"]),
      bpm: getValue(["#bpm", "input[name='bpm']", ".bpm-input"]),
      note_limit: getValue(["#noteLimit", "#note-limit", "input[name='note_limit']"]),
      markov_order: getValue(["#markovOrder", "#markov-order", "input[name='markov_order']"]),
      instruments: {
        melody: getValue(["#melody", "input[name='melody']"]),
        bass: getValue(["#bass", "input[name='bass']"]),
        drums: getValue(["#drums", "input[name='drums']"]),
        chords: getValue(["#chords", "input[name='chords']"])
      }
    };
  }

  function downloadJsonFile(obj, filename = "melody_matrix_config.json") {
    const blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function initChatbot() {
    const chatToggle = document.getElementById("chat-toggle");
    const chatWindow = document.getElementById("chat-window");
    const chatClose = document.getElementById("chat-close");
    const chatSend = document.getElementById("chat-send");
    const chatInput = document.getElementById("chat-input");
    const chatMessages = document.getElementById("chat-messages");
    const suggestionButtons = document.querySelectorAll(".chat-suggestion-btn");

    if (!chatToggle || !chatWindow || !chatClose || !chatSend || !chatInput || !chatMessages) {
      return;
    }

    function addUserMessage(text) {
      chatMessages.appendChild(createMessage(text, "user-message"));
      scrollToBottom(chatMessages);
    }

    function addBotMessage(text) {
      chatMessages.appendChild(createMessage(text, "bot-message"));
      scrollToBottom(chatMessages);
    }

    function addTypingMessage() {
      const typing = createMessage("Thinking...", "typing-message");
      typing.id = "chat-typing";
      chatMessages.appendChild(typing);
      scrollToBottom(chatMessages);
    }

    function removeTypingMessage() {
      const typing = document.getElementById("chat-typing");
      if (typing) typing.remove();
    }

    async function sendChatMessage(textFromButton) {
      const text = (textFromButton || chatInput.value).trim();
      if (!text) return;

      addUserMessage(text);
      chatInput.value = "";
      addTypingMessage();

      try {
        const response = await fetch(BACKEND_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            message: text,
            dashboard_state: getDashboardState()
          })
        });

        const data = await response.json();
        removeTypingMessage();
        addBotMessage(data.reply || "No reply received.");

        if (data.config_json) {
          addBotMessage("A config JSON preset was generated and will download now.");
          downloadJsonFile(data.config_json);
        }
      } catch (error) {
        removeTypingMessage();
        addBotMessage("Could not reach the chatbot backend.");
      }
    }

    chatToggle.addEventListener("click", () => {
      chatWindow.classList.toggle("hidden");
      if (!chatWindow.classList.contains("hidden")) {
        scrollToBottom(chatMessages);
      }
    });

    chatClose.addEventListener("click", () => {
      chatWindow.classList.add("hidden");
    });

    chatSend.addEventListener("click", () => {
      sendChatMessage();
    });

    chatInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        sendChatMessage();
      }
    });

    suggestionButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const text = btn.getAttribute("data-question") || "";
        sendChatMessage(text);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initChatbot);
  } else {
    initChatbot();
  }
})();