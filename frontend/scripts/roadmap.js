const API_BASE = 'http://localhost:5000/api';

let currentRole = null;
let conversationActive = false;
let messageCount = 0;

// Get role from URL
const urlParams = new URLSearchParams(window.location.search);
currentRole = urlParams.get('role');

// Role name mapping
const roleNames = {
    'ai_data_scientist': 'AI & Data Scientist',
    'full_stack': 'Full Stack Developer',
    'machine_learning': 'Machine Learning Engineer',
    'game_developer': 'Game Developer',
    'software_architect': 'Software Architect'
};

document.addEventListener('DOMContentLoaded', async () => {
    if (!currentRole) {
        window.location.href = 'index.html';
        return;
    }

    // Set role title
    document.getElementById('roleTitle').textContent = roleNames[currentRole];

    // Load preset roadmap
    await loadPresetRoadmap();

    // Setup event listeners
    document.getElementById('startConversationBtn').addEventListener('click', startConversation);
    document.getElementById('sendButton').addEventListener('click', sendMessage);
    document.getElementById('chatInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    document.getElementById('doneButton').addEventListener('click', finishConversation);
    document.getElementById('downloadButton')?.addEventListener('click', downloadRoadmap);
});

async function loadPresetRoadmap() {
    try {
        const response = await fetch(`${API_BASE}/roadmap/preset/${currentRole}`);
        const data = await response.json();
        
        displayRoadmap(data.roadmap, 'roadmapTree');
    } catch (error) {
        console.error('Error loading preset roadmap:', error);
        document.getElementById('roadmapTree').textContent = 'Error loading roadmap. Please try again.';
    }
}

function displayRoadmap(roadmapText, containerId) {
    const container = document.getElementById(containerId);
    
    if (!roadmapText || typeof roadmapText !== 'string') {
        console.error('Invalid roadmap data:', roadmapText);
        container.innerHTML = '<div class="error-message">Error: No roadmap data available</div>';
        return;
    }
    
    container.innerHTML = '';
    
    const lines = roadmapText.split('\n');
    const formattedLines = lines.map(line => {
        const trimmed = line.trim();
        if (!trimmed) return '<br>';
        
        // Style different parts
        if (line.startsWith('├──') || line.startsWith('└──')) {
            return `<div class="tree-item">${escapeHtml(line)}</div>`;
        } else if (line.match(/^\d+\./)) {
            return `<div class="tree-section">${escapeHtml(line)}</div>`;
        } else if (line.match(/^[A-Z]/)) {
            return `<div class="tree-root">${escapeHtml(line)}</div>`;
        }
        return `<div>${escapeHtml(line)}</div>`;
    });
    
    container.innerHTML = formattedLines.join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function startConversation() {
    // Hide roadmap section
    document.getElementById('roadmapSection').classList.add('hidden');
    
    // Show conversation section
    const conversationSection = document.getElementById('conversationSection');
    conversationSection.classList.remove('hidden');
    
    conversationActive = true;
    
    // Start conversation with backend
    try {
        const response = await fetch(`${API_BASE}/conversation/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role: currentRole })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (!data.message) {
            throw new Error('No message received from server');
        }
        
        addMessage('bot', data.message);
    } catch (error) {
        console.error('Error starting conversation:', error);
        addMessage('bot', `❌ Error: ${error.message}. Please check the server console and try again.`);
        conversationActive = false;
    }
}

function addMessage(type, content) {
    const messagesContainer = document.getElementById('messagesContainer');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="message-avatar">${type === 'bot' ? '🤖' : '👤'}</div>
            <span>${type === 'bot' ? 'Assistant' : 'You'}</span>
        </div>
        <div class="message-content">${escapeHtml(content)}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message || !conversationActive) return;
    
    // Add user message
    addMessage('user', message);
    input.value = '';
    
    // Disable input while waiting
    const sendButton = document.getElementById('sendButton');
    sendButton.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/conversation/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                role: currentRole,
                message: message 
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (!data.message) {
            throw new Error('No response received from server');
        }
        
        addMessage('bot', data.message);
        
        messageCount++;
    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('bot', `❌ Error: ${error.message}. Please check the server console.`);
    } finally {
        sendButton.disabled = false;
    }
}

async function finishConversation() {
    conversationActive = false;
    
    // Hide conversation section
    document.getElementById('conversationSection').classList.add('hidden');
    
    // Show personalized section
    const personalizedSection = document.getElementById('personalizedSection');
    personalizedSection.classList.remove('hidden');
    
    // Generate personalized roadmap
    try {
        const response = await fetch(`${API_BASE}/roadmap/personalize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role: currentRole })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (!data.roadmap) {
            throw new Error('No roadmap data received from server');
        }
        
        // Hide loading, show roadmap
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('personalizedRoadmapContainer').classList.remove('hidden');
        document.getElementById('finalActions').classList.remove('hidden');
        
        displayRoadmap(data.roadmap, 'personalizedRoadmapTree');
    } catch (error) {
        console.error('Error generating personalized roadmap:', error);
        const loadingState = document.getElementById('loadingState');
        loadingState.innerHTML = `
            <div style="text-align: center; color: #ef4444;">
                <p style="font-size: 1.25rem; margin-bottom: 1rem;">⚠️ Error</p>
                <p>${error.message}</p>
                <button onclick="window.location.reload()" style="margin-top: 1rem; padding: 0.75rem 1.5rem; background: #6366f1; color: white; border: none; border-radius: 12px; cursor: pointer;">
                    Try Again
                </button>
            </div>
        `;
    }
}

async function downloadRoadmap() {
    try {
        const response = await fetch(`${API_BASE}/roadmap/download/${currentRole}`);
        const blob = await response.blob();
        
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${currentRole}_roadmap.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error downloading roadmap:', error);
    }
}
