const form = document.getElementById("askForm");
const msg = document.getElementById("msg");
let dots = 0;

//scroll down function:
function msgScrollToBottom() {
    msg.scrollTop = msg.scrollHeight;
}



form.addEventListener("submit", async function (e) {
    e.preventDefault();
    
    
    const formData = new FormData(form);

    //adding msg elemnts to the li
    const userMsg = document.createElement("li");
    userMsg.textContent = formData.get("question");
    msg.appendChild(userMsg);

    form.reset();
    msgScrollToBottom();
    //

    //loading animation:
    const loadMsg = document.createElement("li");
    loadMsg.textContent = "Thinking";
    msg.appendChild(loadMsg);
    
    dots = 0;
    const loadingInterval = setInterval(() => {
    dots++;

    if (dots > 3) {
        dots = 0;
    }

    loadMsg.textContent = "Thinking" + ".".repeat(dots);
    }, 500);
    //

    const res = await fetch("/ask", {method:"POST", body:formData});

    const data = await res.json();

    //deleting animation:
    clearInterval(loadingInterval);
    loadMsg.remove();
    //

    if (res.ok) {
        const aiMsg = document.createElement("li");
        aiMsg.textContent = data.answer;
        msg.appendChild(aiMsg);

        msgScrollToBottom()

    }
    else {
        console.error(`Failed to receive: ${data.detail}`);
    }

});