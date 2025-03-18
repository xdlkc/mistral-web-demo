/**
 * Mistral AI 聊天应用的主JavaScript文件
 */

document.addEventListener('DOMContentLoaded', function() {
    // 初始化激活的聊天类型按钮
    const textChatButton = document.getElementById('toggleTextChat');
    if (textChatButton) {
        textChatButton.classList.add('active');
    }
    
    // 适配移动设备的侧边栏切换
    if (window.innerWidth < 768) {
        const sidebarToggle = document.createElement('button');
        sidebarToggle.className = 'btn btn-sm btn-light position-fixed';
        sidebarToggle.style.top = '10px';
        sidebarToggle.style.left = '10px';
        sidebarToggle.style.zIndex = '1001';
        sidebarToggle.innerHTML = '<i class="bi bi-list"></i>';
        
        document.body.appendChild(sidebarToggle);
        
        const sidebar = document.querySelector('.sidebar');
        
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
        
        document.addEventListener('click', function(e) {
            if (!sidebar.contains(e.target) && e.target !== sidebarToggle) {
                sidebar.classList.remove('show');
            }
        });
    }
    
    // 延迟加载缺省头像和图片
    const images = document.querySelectorAll('img[data-src]');
    images.forEach(img => {
        img.src = img.getAttribute('data-src');
    });
});