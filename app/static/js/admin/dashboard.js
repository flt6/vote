let currentTab = 'chain';

async function loadData() {
    const response = await fetch('/api/get_mode', {
        method: 'GET'
    });
    currentTab = await response.text();
    if (currentTab === 'chain') {
        document.getElementById('chainStats').style.display = "block";
        document.getElementById('voteStats').style.display = "none";
        await loadChainStats();
    } else {
        document.getElementById('chainStats').style.display = "none";
        document.getElementById('voteStats').style.display = "block";
        await loadVoteStats();
    }
}


async function loadChainStats() {
    try {
        const response = await fetch('/api/chain/stats');
        const data = await response.json();
        
        document.getElementById('chainCount').textContent = data.chained_count;
        document.getElementById('unchainCount').textContent = data.unchained_count;
        
        renderNameGrid('chainedGrid', data.chained, true);
        renderNameGrid('unchainedGrid', data.unchained, false);
    } catch (error) {
        alert('加载数据失败：' + error);
    }
}

async function loadVoteStats() {
    try {
        const response = await fetch('/api/vote/stats');
        const stats = await response.json();
        renderVoteTable(stats);
    } catch (error) {
        alert('加载数据失败：' + error);
    }
}

function renderNameGrid(elementId, names, showCancel) {
    const grid = document.getElementById(elementId);
    grid.innerHTML = names.map(item => {
        const name = typeof item === 'string' ? item : item.name;
        const time = typeof item === 'string' ? '' : item.time;
        
        return `
            <div class="name-item" onclick="${showCancel ? `toggleOperations('${name}')` : `confirmChain('${name}')`}" data-name="${name}">
                <div class="name-text">${name}</div>
                ${showCancel ? `
                    <div class="operations" id="operations-${name}" style="display: none">
                        ${time ? `<div class="chain-time">接龙时间：<br>${time}</div>` : ''}
                        <button class="cancel-btn" onclick="event.stopPropagation(); cancelChain('${name}')">
                            <i class="fas fa-times"></i> 取消接龙
                        </button>
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
}

// 添加新函数用于切换操作栏的显示/隐藏
function toggleOperations(name) {
    const operationsDiv = document.getElementById(`operations-${name}`);
    const allOperations = document.querySelectorAll('.operations');
    
    // 先隐藏所有其他的操作栏
    allOperations.forEach(op => {
        if (op.id !== `operations-${name}`) {
            op.style.display = 'none';
        }
    });
    
    // 切换当前点击项的操作栏
    operationsDiv.style.display = operationsDiv.style.display === 'none' ? 'block' : 'none';
}


async function confirmChain(name) { 
    try {
        const response = await fetch('/api/chain/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name })
        });
        
        const data = await response.json();
        if (data.success) {
            await loadChainStats()
            showToast("提交成功！");
        } else {
            showToast('提交失败：' + data.error, 'error');
        }
    } catch (error) {
        showToast('网络错误，请重试', 'error');
    }
}

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 1500);
}

function renderVoteTable(stats) {
    const tbody = document.querySelector('#voteTable tbody');
    tbody.innerHTML = stats.map(item => `
        <tr>
            <td>${item.option}</td>
            <td>${item.count}</td>
            <td>${item.percentage}%</td>
        </tr>
    `).join('');
}

async function cancelChain(name) {
    try {
        const response = await fetch('/api/chain/cancel', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ name })
        });
        
        const data = await response.json();
        if (data.success) {
            loadChainStats();
        } else {
            alert('取消失败：' + data.error);
        }
    } catch (error) {
        alert('取消失败：' + error);
    }
}

async function resetSystem() {
    if (!confirm('确定要重置系统吗？此操作不可恢复！')) {
        return;
    }
    
    try {
        const response = await fetch('/api/admin/reset', {
            method: 'POST'
        });
        
        const data = await response.json();
        if (data.success) {
            alert('重置成功');
            window.location.href = '/admin/config';
        } else {
            alert('重置失败：' + data.error);
        }
    } catch (error) {
        alert('重置失败：' + error);
    }
}

document.addEventListener('DOMContentLoaded', loadData);