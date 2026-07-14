async function sendMessage() {
    let input = document.getElementById("user-input");
    let chatBox = document.getElementById("chat-box");
    let message = input.value;
    if(message.trim()===""){
        return;
    }
    chatBox.innerHTML += `
        <div class="user-message">
            <b>You:</b> ${message}
        </div>
    `;
    const response = await fetch("/chat", {
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            message:message
        })
    });
    const data = await response.json();
    chatBox.innerHTML += `
        <div class="bot-message">
            <b>Bot:</b> ${data.response}
        </div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;
    input.value = "";
}