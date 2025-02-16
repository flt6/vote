document.addEventListener('DOMContentLoaded', function() {
    fetchVoteData();
});

async function fetchVoteData() {
    const response = await fetch('/api/vote/options');
    const data = await response.json();
    renderVoteData(data);
}

function renderVoteData(data) {
    document.getElementById('voteTitle').textContent = data.title;
    const optionsList = document.getElementById('optionsList');
    
    optionsList.innerHTML = data.options.map(option => `
        <div class="option-item" onclick="selectOption('${option.text}')">
            ${option.text}
            ${data.showCount ? `<span class="vote-count">${option.count}人</span>` : ''}
        </div>
    `).join('');

    localStorage.setItem('voteTitle', data.title);
}

function selectOption(option) {
    localStorage.setItem('selectedOption', option);
    window.location.href = '/vote/confirm';
}

function confirmVote() {
    const option = localStorage.getItem('selectedOption');
    fetch('/api/vote/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ option })
    }).then(() => {
        window.location.href = '/vote';
    });
}