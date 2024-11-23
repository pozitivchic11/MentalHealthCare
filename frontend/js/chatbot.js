const form = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const messageInput = document.getElementById("message-input");
    const modelSelect = document.getElementById("model");
    const userMessage = messageInput.value.trim();
    const selectedModel = modelSelect.value;

    if (userMessage && selectedModel) {
        const userBubble = document.createElement("div");
        userBubble.className = "chat-bubble user";
        userBubble.textContent = userMessage;
        chatBox.appendChild(userBubble);

        chatBox.scrollTop = chatBox.scrollHeight;

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const reader = response.body.getReader();
                let { value, done } = await reader.read();
                let result = "";
                while (!done) {
                    result += new TextDecoder().decode(value);
                    ({ value, done } = await reader.read());
                }

                const botBubble = document.createElement("div");
                botBubble.className = "chat-bubble bot";
                botBubble.textContent = result;
                chatBox.appendChild(botBubble);
            } else {
                throw new Error("Error fetching response");
            }
        } catch (error) {
            const botBubble = document.createElement("div");
            botBubble.className = "chat-bubble bot";
            botBubble.textContent = "Error: Could not fetch bot response.";
            chatBox.appendChild(botBubble);
        }

        messageInput.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});

function logout() {
    fetch('/logout', {
        method: 'POST',
        credentials: 'same-origin'
    }).then(response => {
        if (response.ok) {
            // Перенаправляє на сторінку входу
            window.location.href = '/';
        } else {
            alert('Logout failed. Please try again.');
        }
    }).catch(error => {
        console.error('Error during logout:', error);
        alert('An error occurred. Please try again.');
    });
}
