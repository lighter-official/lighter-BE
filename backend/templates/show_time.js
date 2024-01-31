window.addEventListener("DOMContentLoaded", () => {
  const messages = document.createElement("ul");
  document.body.appendChild(messages);

  const websocket = new WebSocket("ws://localhost:8000/ws/glooing/timer");
  websocket.onmessage = ({ data }) => {
    const message = document.createElement("li");
    const content = document.createTextNode(data);
    message.appendChild(content);
    messages.appendChild(message);
  };
});