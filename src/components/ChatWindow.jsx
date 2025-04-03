import React, { useState, useEffect, useRef } from "react";
import "./ChatWindow.css";
import { postChatMessage, getOverview } from "../api/api"; // Import getOverview
import { marked } from "marked";

function ChatWindow() {

  const defaultMessage = [{
    role: "assistant",
    content: "Hi, how can I help you today?"
  }];

  const [messages,setMessages] = useState(defaultMessage)
  const [input, setInput] = useState("");

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
      scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const fetchOverview = async () => {
      const overviewMessage = await getOverview("secret_id", ""); // Call getOverview
      setMessages(prevMessages => [...prevMessages, overviewMessage]); // Add the overview message
    };

    fetchOverview(); // Trigger the API call on component load
    scrollToBottom();
  }, []);

  const handleSend = async (input) => {
    if (input.trim() !== "") {
      // Set user message
      setMessages(prevMessages => [...prevMessages, { role: "user", content: input }]);
      setInput("");

      // Call API & set assistant message
      const newMessage = await postChatMessage("secret_id", input);
      console.log("newMessage", newMessage);
      setMessages(prevMessages => [...prevMessages, newMessage]);
    }
  };

  return (
    <>
      <div className="messages-container">
          {messages.map((message, index) => (
              <div key={index} className={`${message.role}-message-container`}>
                  {message.content && (
                      <div className={`message ${message.role}-message`}>
                          <div dangerouslySetInnerHTML={{__html: marked(message.content).replace(/<p>|<\/p>/g, "")}}></div>
                      </div>
                  )}
              </div>
          ))}
          <div ref={messagesEndRef} />
      </div>
      <div className="input-area">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a message..."
              onKeyPress={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  handleSend(input);
                  e.preventDefault();
                }
              }}
              rows="3"
            />
            <button className="send-button" onClick={handleSend}>
              Send
            </button>
          </div>
        </>
);
}

export default ChatWindow;
