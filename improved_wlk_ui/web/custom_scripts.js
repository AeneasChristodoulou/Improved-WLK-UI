// ============ Speaker Name Management ============
const speakerNamesCache = {};
let speakerRowCount = 0;

// Toggle speaker names panel
document.getElementById('speakerNamesToggle').addEventListener('click', () => {
    const container = document.getElementById('speakerNamesContainer');
    container.classList.toggle('visible');
    if (container.classList.contains('visible')) {
        loadSpeakerNames();
    }
});

// Load existing speaker names from server
async function loadSpeakerNames() {
    try {
        const response = await fetch('/api/speakers');
        const data = await response.json();
        Object.assign(speakerNamesCache, data.speakers);
        renderSpeakerNamesList();
    } catch (error) {
        console.error('Failed to load speaker names:', error);
    }
}

// Render the speaker names list
function renderSpeakerNamesList() {
    const list = document.getElementById('speakerNamesList');
    list.innerHTML = '';

    // Get all unique speaker IDs (from cache + any detected in transcript)
    const speakerIds = new Set(Object.keys(speakerNamesCache).map(Number));

    // Add default speakers 1-4 if none exist
    if (speakerIds.size === 0) {
        [1, 2, 3, 4].forEach(id => speakerIds.add(id));
    }

    Array.from(speakerIds).sort((a, b) => a - b).forEach(speakerId => {
        addSpeakerRowElement(speakerId, speakerNamesCache[speakerId] || '');
    });
}

// Add a speaker row element
function addSpeakerRowElement(speakerId, name = '') {
    const list = document.getElementById('speakerNamesList');
    const row = document.createElement('div');
    row.className = 'speaker-name-row';
    row.dataset.speakerId = speakerId;

    row.innerHTML = `
        <div class="speaker-badge-edit">${speakerId}</div>
        <input type="text" class="speaker-name-input"
               placeholder="Enter name (e.g., Alice)"
               value="${name}"
               data-speaker-id="${speakerId}">
        <button class="speaker-name-btn save" onclick="saveSpeakerName(${speakerId}, this)">Save</button>
        <button class="speaker-name-btn clear" onclick="removeSpeakerName(${speakerId}, this)">✕</button>
    `;

    // Save on Enter key
    const input = row.querySelector('input');
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            saveSpeakerName(speakerId, row.querySelector('.save'));
        }
    });

    list.appendChild(row);
}

// Add a new speaker row
function addSpeakerRow() {
    const existingIds = Array.from(document.querySelectorAll('.speaker-name-row'))
        .map(row => parseInt(row.dataset.speakerId));
    const newId = existingIds.length > 0 ? Math.max(...existingIds) + 1 : 1;
    addSpeakerRowElement(newId, '');
}

// Save speaker name to server
async function saveSpeakerName(speakerId, button) {
    const row = button.closest('.speaker-name-row');
    const input = row.querySelector('.speaker-name-input');
    const name = input.value.trim();

    if (!name) {
        alert('Please enter a name');
        return;
    }

    try {
        const response = await fetch('/api/speakers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ speaker_id: speakerId, name: name })
        });

        if (response.ok) {
            speakerNamesCache[speakerId] = name;
            button.textContent = '✓';
            setTimeout(() => { button.textContent = 'Save'; }, 1000);

            // Update any visible speaker badges in transcript
            updateTranscriptSpeakerNames();
        }
    } catch (error) {
        console.error('Failed to save speaker name:', error);
    }
}

// Remove speaker name
async function removeSpeakerName(speakerId, button) {
    try {
        await fetch(`/api/speakers/${speakerId}`, { method: 'DELETE' });
        delete speakerNamesCache[speakerId];

        const row = button.closest('.speaker-name-row');
        row.querySelector('.speaker-name-input').value = '';

        updateTranscriptSpeakerNames();
    } catch (error) {
        console.error('Failed to remove speaker name:', error);
    }
}

// Clear all speaker names
async function clearAllSpeakerNames() {
    if (!confirm('Clear all speaker names?')) return;

    try {
        await fetch('/api/speakers', { method: 'DELETE' });
        Object.keys(speakerNamesCache).forEach(key => delete speakerNamesCache[key]);
        renderSpeakerNamesList();
        updateTranscriptSpeakerNames();
    } catch (error) {
        console.error('Failed to clear speaker names:', error);
    }
}

// Update speaker badges in the transcript
function updateTranscriptSpeakerNames() {
    document.querySelectorAll('.speaker-badge').forEach(badge => {
        const speakerId = parseInt(badge.dataset.speakerId || badge.textContent);
        if (speakerNamesCache[speakerId]) {
            badge.textContent = speakerNamesCache[speakerId];
            badge.title = `Speaker ${speakerId}`;
        } else {
            badge.textContent = speakerId;
            badge.title = '';
        }
    });
}

// Initialize on page load
loadSpeakerNames();
