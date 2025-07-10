import { useState } from "react";
import ChatContainer from "./components/ChatContainer";
import ChatHeader from "./components/ChatHeader";
import ChatMessages from "./components/ChatMessages";
import ChatInput from "./components/ChatInput";
import "./App.css";

function App() {
  const [isSending, setIsSending] = useState(false);
  const [messages, setMessages] = useState([
    {
      from: "system",
      value:
        "You are A VASTLY intelligent ARTIFICIAL INTELLIGENCE with DOMAIN-EXPERT KNOWLEDGE from a variety of fields.\nUSE your knowledge to be helpful and truthfully answer questions about the world.",
    },
    {
      from: "user",
      value: "How to define consciousness?",
    },
    {
      from: "gpt",
      value:
        "Consciousness is a complex and multifaceted phenomenon that has been studied across various disciplines, including psychology, neuroscience, philosophy, and cognitive science.",
    },
  ]);
  return (
    <ChatContainer>
      <ChatHeader />
      <ChatMessages messages={messages} />
      <ChatInput
        messages={messages}
        setMessages={setMessages}
        isSending={isSending}
        setIsSending={setIsSending}
      />
    </ChatContainer>
  );
}

export default App;
