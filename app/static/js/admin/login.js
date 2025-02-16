async function login() {
    const password = document.getElementById('password').value;
    try {
        const response = await fetch('/api/admin/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',  // 允许发送和接收cookie
            body: JSON.stringify({ password })
        });
        
        const data = await response.json();
        if (data.success) {
            window.location.href = data.jump;
        } else {
            alert('登录失败：' + data.error);
        }
    } catch (error) {
        alert('登录失败：' + error);
    }
}