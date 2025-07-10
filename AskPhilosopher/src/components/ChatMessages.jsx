import { useEffect, useRef } from "react";
import styles from "./messages.module.css";

const msgStyle = (sender) => ({
  alignSelf: sender === "user" ? "flex-end" : "flex-start",
  background:
    sender === "user" ? "linear-gradient(to right, #764ba2, #667eea)" : "white",
  color: sender === "user" ? "white" : "black",
});

function ChatMessages({ messages }) {
  const chat = useRef(null);
  useEffect(() => {
    // Scroll to bottom
    chat.current.scrollTop = chat.current.scrollHeight;
  });
  return (
    <div className={styles.messagesContainer} ref={chat}>
      {messages.map((message, index) =>
        message.from !== "system" ? (
          <div
            className={styles.message}
            style={msgStyle(message.from)}
            key={index}
          >
            {message.value}
          </div>
        ) : (
          ""
        )
      )}
    </div>
  );
}

export default ChatMessages;
