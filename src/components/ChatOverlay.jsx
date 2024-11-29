import React, { useState } from "react";
import "../styles/ChatOverlay.css";

function ChatOverlay() {
  const [showHistory, setShowHistory] = useState(false);

  return (
    <div className="overlay-container">
      {/* History Panel */}
      {showHistory && (
        <div className="history-panel">
          <h3 className="history-panel-top-logo">LOGO</h3>
          <div className="history-list">
            <div className="history-item">AI: Hey! how are you doing?</div>
            <div className="history-item">
              user: Great! Can you help me out?
            </div>
            <div className="history-item">AI: Hey! how are you doing?</div>
            <div className="history-item">
              user: Great! Can you help me out?
            </div>
          </div>
        </div>
      )}

      {/* Toggle Button */}
      <button
        className="toggle-history"
        onClick={() => setShowHistory(!showHistory)}
      >
        {showHistory ? "ICON" : "ICON"}
      </button>

      {/* Chat Input */}
      <div className="chat-input">
        <input type="text" placeholder="Type a message..." />
        <button>Send</button>
      </div>
    </div>
  );
}

export default ChatOverlay;
