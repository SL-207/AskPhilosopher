import { useState } from "react";
import styles from "./chatinput.module.css";
import { sendMessage } from "../services/chatService";

function ChatInput({ messages, setMessages, isSending, setIsSending }) {
  const [inputText, setInputText] = useState("");
  
  const handleSubmit = (e) => {
    if (!e.shiftKey && e.key === "Enter") {
      e.preventDefault();
      if (inputText.trim() !== "" && !isSending) {
        const userMessage = {
          from: "user",
          value: inputText,
        };
        const newMessages = [...messages, userMessage];
        setIsSending(true);
        setMessages(newMessages);
        setInputText("");
        sendMessage(newMessages)
          .then((data) => {
            setMessages([...newMessages, data.response]);
          })
          .catch((error) => {
            console.error(error);
          }).finally(() => {
            setIsSending(false);
          });
      }
    }
  };
  return (
    <div className={styles.inputArea}>
      <textarea
        className={styles.inputBox}
        placeholder="Ask a question..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        onKeyDown={handleSubmit}
      />
      <div className={styles.inputHint}>
        Press Enter to send, Shift+Enter for new line
      </div>
    </div>
  );
}

export default ChatInput;
