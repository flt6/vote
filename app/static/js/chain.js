let nameList = [];

document.addEventListener('DOMContentLoaded', function() {
    fetchNameList();
    initializeSearch();
});

async function fetchNameList() {
    const response = await fetch('/api/chain/names');
    nameList = await response.json();
    renderNameGrid(nameList);
}

function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', debounce(async function(e) {
        const searchText = e.target.value.trim();
        const response = await fetch(`/api/chain/search?query=${encodeURIComponent(searchText)}`);
        const filtered = await response.json();
        renderNameGrid(filtered);
    }, 300));
}

// 添加防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}


function renderNameGrid(names) {
    const grid = document.getElementById('nameGrid');
    if (nameList.length==0){
        grid.innerHTML="<b>已全部完成接龙</b>"
        return;
    }
    grid.innerHTML = names.map(name => `
        <div class="name-item" onclick="selectName('${name}')">
            ${name}
        </div>
    `).join('');
}

function selectName(name) {
    localStorage.setItem('selectedName', name);
    window.location.href = '/chain/confirm';
}