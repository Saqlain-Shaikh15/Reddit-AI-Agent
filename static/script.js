const subredditInput = document.getElementById('subreddit-input');
const subredditStatus = document.getElementById('subreddit-status');
const chatContainer = document.getElementById('chat-container');
const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

let currentSubreddit = "";
let lastLoadedSubreddit = "";
let subreddit = false;

function formatResponse(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // **bold** → <strong>
        .replace(/\*(.*?)\*/g, '<em>$1</em>')               // *italic* → <em>
        .replace(/\n/g, '<br>');                             // newlines → <br>
}

function clearEmptyState() {
    const emptyState = chatWindow.querySelector('.empty-state');
    if (emptyState) emptyState.remove();
}

function appendMessage(role, html) {
    clearEmptyState();
    const el = document.createElement('div');
    el.className = role;
    el.innerHTML = html;
    chatWindow.appendChild(el);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return el;
}

async function loadSubreddit() {
    const subreddit = subredditInput.value.trim().replace(/^r\//i, '');
    if (!subreddit) return;

    const response = await fetch('/check-subreddit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({subreddit})
    });

    const data = await response.json();

    if(!data.exists){
        subredditStatus.textContent = `r/${subreddit} does not exist`;
        subredditStatus.classList.remove('active');
        return;
    }

    currentSubreddit = subreddit;
    chatContainer.classList.remove('disabled');
    userInput.disabled = false;
    sendBtn.disabled = false;

    subredditStatus.textContent = `Connected to r/${subreddit}`;
    subredditStatus.classList.add('active');

    if (subreddit !== lastLoadedSubreddit) {
        appendMessage('bot-message', `Searching for subreddit: r/${subreddit}`);
        lastLoadedSubreddit = subreddit;
    }

    userInput.focus();
}

document.getElementById('load-subreddit').addEventListener('click', loadSubreddit);

subredditInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        loadSubreddit();
    }
});

document.getElementById('subreddit-form').addEventListener('submit', (e) => {
    e.preventDefault();
    loadSubreddit();
});

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage('user-message', message);
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
        if (!response.ok) {
            appendMessage('bot-message error', data.error);
        } else {
            appendMessage('bot-message', formatResponse(data.answer));
        }
    } catch (err) {
        appendMessage('bot-message error', 'Something went wrong. Please try again.');
    } finally {
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
});