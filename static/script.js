const subredditInput = document.getElementById('subreddit-input');
const chatContainer = document.getElementById('chat-container');
const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

let currentSubreddit = "";
let lastLoadedSubreddit = "";

// changed - converts LLM markdown-style text to readable HTML
function formatResponse(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // **bold** → <strong>
        .replace(/\*(.*?)\*/g, '<em>$1</em>')               // *italic* → <em>
        .replace(/\n/g, '<br>');                             // newlines → <br>
}

document.getElementById('load-subreddit').addEventListener('click', () => {
    const subreddit = subredditInput.value.trim();
    if (subreddit) {
        currentSubreddit = subreddit;
        chatContainer.classList.remove('disabled');

        if (subreddit !== lastLoadedSubreddit) {
            chatWindow.innerHTML += `<div class="bot-message">Searching for subreddit: r/${subreddit}</div>`;
            lastLoadedSubreddit = subreddit;
        }
    }
});

sendBtn.addEventListener('click', async () => {
    const message = userInput.value.trim();
    if (!message) return;

    chatWindow.innerHTML += `<div class="user-message">${message}</div>`;
    userInput.value = "";

    sendBtn.disabled = true;
    userInput.disabled = true;

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: message, subreddit: currentSubreddit }),
        });

        const data = await response.json();
        if (!response.ok) {  // changed - checks if status is 4xx/5xx
            chatWindow.innerHTML += `<div class="bot-message error">${data.error}</div>`;  // changed - shows e.g. "Subreddit r/xyz does not exist"
        } else {
            chatWindow.innerHTML += `<div class="bot-message">${formatResponse(data.answer)}</div>`;
        }
        chatWindow.scrollTop = chatWindow.scrollHeight;
    } catch (err) {
        chatWindow.innerHTML += `<div class="bot-message error">Something went wrong. Please try again.</div>`;
    } finally {
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
});