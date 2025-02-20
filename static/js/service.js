async function connect(method, url, params) {
    try {
        showLoader()
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(params),
        });
        hideLoader()
        return await response.json();
    } catch (error) {
        hideLoader()
        showMessage('error', 'เกิดข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์')
    }
}
