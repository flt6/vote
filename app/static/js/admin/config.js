let currentTab = 'chain';

document.addEventListener('DOMContentLoaded', async function() {
    document.getElementById('nameList').addEventListener("input", async function (e){
        if (e.inputType=="insertLineBreak")
            renderPreview(parseList(e.target.value),"preview-name");
    });
    document.getElementById('optionList').addEventListener("input", async function (e){
        if (e.inputType=="insertLineBreak")
            renderPreview(parseList(e.target.value),"preview-option");
    });
});

function switchTab(tab) {
    currentTab = tab;
    if (tab === "chain"){
        document.getElementById('tab-chain').classList.add("active")
        document.getElementById('tab-vote').classList.remove("active")
    }else{
        document.getElementById('tab-chain').classList.remove("active")
        document.getElementById('tab-vote').classList.add("active")

    }
    document.getElementById('chainConfig').style.display = tab === 'chain' ? 'block' : 'none';
    document.getElementById('voteConfig').style.display = tab === 'vote' ? 'block' : 'none';
}

function parseList(text) {
    return text.split(/[\n,]/)
        .map(item => item.trim())
        .filter(item => item.length > 0);
}

function renderPreview(names,id) {
    const grid = document.getElementById(id);
    grid.innerHTML = names.map(name => `
        <div class="name-item" onclick="selectName('${name}')">
            ${name}
        </div>
    `).join('');
}

async function saveChainConfig() {
    const names = parseList(document.getElementById('nameList').value);
    try {
        const response = await fetch('/api/admin/config/chain', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ names })
        });
        
        const data = await response.json();
        if (data.success) {
            alert('保存成功');
            window.location.href = '/admin/dashboard';
        } else {
            alert('保存失败：' + data.error);
        }
    } catch (error) {
        alert('保存失败：' + error);
    }
}

async function saveVoteConfig() {
    const title = document.getElementById('voteTitle').value;
    const options = parseList(document.getElementById('optionList').value);
    const showCount = document.getElementById('showCount').checked;
    
    try {
        const response = await fetch('/api/admin/config/vote', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ title, options, show_count: showCount })
        });
        
        const data = await response.json();
        if (data.success) {
            alert('保存成功');
            window.location.href = '/admin/dashboard';
        } else {
            alert('保存失败：' + data.error);
        }
    } catch (error) {
        alert('保存失败：' + error);
    }
}