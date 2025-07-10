const API_URL = "http://localhost:8080";

export async function sendMessage(messages) {
  const formData = new FormData();
  messages.forEach((messageObj, idx) =>
    formData.append(`msg${idx}`, JSON.stringify(messageObj))
  );
  const response = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    body: formData,
  });
  const data = await response.json();
  return data;
}
