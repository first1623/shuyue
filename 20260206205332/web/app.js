// 全局状态管理
const state = {
    records: [],
    currentPreview: null,
    todayCount: 0
};

// 导航切换
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
        // 移除所有active类
        document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
        document.querySelectorAll('.section').forEach(sec => sec.classList.remove('active'));

        // 添加active类到当前项
        this.classList.add('active');
        const sectionId = this.getAttribute('data-section');
        document.getElementById(sectionId).classList.add('active');
    });
});

// 显示/隐藏加载动画
function showLoading(text = '正在处理...') {
    document.getElementById('loading').classList.add('active');
    document.getElementById('loading-text').textContent = text;
}

function hideLoading() {
    document.getElementById('loading').classList.remove('active');
}

// 快速发布
async function quickPublish() {
    const theme = document.getElementById('quick-theme').value.trim();
    const needImage = document.getElementById('quick-image').value === 'yes';

    if (!theme) {
        alert('请输入文章主题');
        return;
    }

    showLoading('正在生成并发布文章...');

    try {
        const result = await publishToBackend({
            action: 'quick_publish',
            theme: theme,
            need_image: needImage
        });

        hideLoading();

        if (result.success) {
            state.todayCount++;
            updateTodayCount();
            alert(`发布成功！\n文章ID: ${result.media_id || '草稿已保存'}`);
            document.getElementById('quick-theme').value = '';
        } else {
            alert(`发布失败：${result.message}`);
        }

        // 刷新记录
        refreshRecords();

    } catch (error) {
        hideLoading();
        alert(`操作失败：${error.message}`);
    }
}

// 生成预览
async function generatePreview() {
    const theme = document.getElementById('preview-theme').value.trim();
    const needImage = document.getElementById('preview-image').value === 'yes';

    if (!theme) {
        alert('请输入文章主题');
        return;
    }

    showLoading('正在生成内容...');

    try {
        const result = await publishToBackend({
            action: 'generate_preview',
            theme: theme,
            need_image: needImage
        });

        hideLoading();

        if (result.success) {
            state.currentPreview = result.article;
            displayPreview(result.article);
        } else {
            alert(`生成失败：${result.message}`);
        }

    } catch (error) {
        hideLoading();
        alert(`操作失败：${error.message}`);
    }
}

// 显示预览
function displayPreview(article) {
    const previewContent = document.getElementById('preview-content');
    previewContent.style.display = 'block';

    document.getElementById('preview-title').textContent = article.title;
    document.getElementById('preview-author').textContent = `作者：${article.author}`;
    document.getElementById('preview-date').textContent = new Date().toLocaleString('zh-CN');
    document.getElementById('preview-body').innerHTML = article.content;
}

// 发布预览
async function publishPreview() {
    if (!state.currentPreview) {
        alert('请先生成内容');
        return;
    }

    if (!confirm('确认发布此文章到公众号？')) {
        return;
    }

    showLoading('正在发布文章...');

    try {
        const result = await publishToBackend({
            action: 'publish_preview',
            article: state.currentPreview
        });

        hideLoading();

        if (result.success) {
            state.todayCount++;
            updateTodayCount();
            alert(`发布成功！\n文章ID: ${result.media_id || '草稿已保存'}`);
            document.getElementById('preview-content').style.display = 'none';
            document.getElementById('preview-theme').value = '';
        } else {
            alert(`发布失败：${result.message}`);
        }

        refreshRecords();

    } catch (error) {
        hideLoading();
        alert(`操作失败：${error.message}`);
    }
}

// 重新生成预览
function regeneratePreview() {
    document.getElementById('preview-content').style.display = 'none';
    document.getElementById('preview-theme').value = '';
}

// 批量发布
async function batchPublish() {
    const themesText = document.getElementById('batch-themes').value.trim();

    if (!themesText) {
        alert('请输入至少一个主题');
        return;
    }

    const themes = themesText.split(/[,，\n]/)
        .map(t => t.trim())
        .filter(t => t);

    if (!confirm(`将批量处理 ${themes.length} 个主题，确认继续？`)) {
        return;
    }

    const progressDiv = document.getElementById('batch-progress');
    progressDiv.style.display = 'block';

    const results = [];

    for (let i = 0; i < themes.length; i++) {
        const theme = themes[i];

        document.getElementById('batch-status').textContent = `正在处理 ${i + 1}/${themes.length}`;
        document.getElementById('batch-current').textContent = theme;

        // 更新进度条
        const progress = ((i + 1) / themes.length * 100).toFixed(0);
        document.getElementById('progress-bar').style.width = `${progress}%`;

        showLoading(`正在处理第 ${i + 1}/${themes.length} 个主题...`);

        try {
            const result = await publishToBackend({
                action: 'quick_publish',
                theme: theme,
                need_image: false
            });

            results.push({
                theme: theme,
                success: result.success,
                message: result.message
            });

            if (result.success) {
                state.todayCount++;
            }

        } catch (error) {
            results.push({
                theme: theme,
                success: false,
                message: error.message
            });
        }

        hideLoading();
    }

    updateTodayCount();

    // 显示结果
    const resultsDiv = document.getElementById('batch-results');
    resultsDiv.innerHTML = `
        <h4 style="margin-bottom:10px;">批量处理结果</h4>
        <p style="margin-bottom:10px;">
            成功：<strong>${results.filter(r => r.success).length}</strong> |
            失败：<strong>${results.filter(r => !r.success).length}</strong>
        </p>
    `;

    results.forEach((result, index) => {
        const statusClass = result.success ? 'success' : 'failed';
        const statusText = result.success ? '成功' : '失败';
        resultsDiv.innerHTML += `
            <div style="margin-top:10px; padding:10px; background:${result.success ? '#d4edda' : '#f8d7da'}; border-radius:5px;">
                <strong>${result.theme}</strong>
                <span class="status ${statusClass}">${statusText}</span>
                <div style="margin-top:5px; font-size:12px;">${result.message}</div>
            </div>
        `;
    });

    document.getElementById('batch-status').textContent = '处理完成！';

    refreshRecords();

    setTimeout(() => {
        if (confirm('批量处理已完成，是否关闭进度面板？')) {
            progressDiv.style.display = 'none';
        }
    }, 1000);
}

// 刷新记录
async function refreshRecords() {
    showLoading('正在加载记录...');

    try {
        const result = await fetchRecords();
        hideLoading();

        state.records = result.records || [];
        displayRecords();

    } catch (error) {
        hideLoading();
        alert(`加载记录失败：${error.message}`);
    }
}

// 显示记录
function displayRecords() {
    const recordsList = document.getElementById('records-list');

    if (state.records.length === 0) {
        recordsList.innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                </svg>
                <p>暂无发布记录</p>
            </div>
        `;
        return;
    }

    let html = '';
    state.records.slice(0, 20).forEach((record, index) => {
        const statusClass = record.status === 'success' ? 'success' : 'failed';
        const statusText = record.status === 'success' ? '成功' : '失败';

        html += `
            <div class="record-item ${record.status === 'failed' ? 'failed' : ''}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong>${record.title || record.theme}</strong>
                    <span class="status ${statusClass}">${statusText}</span>
                </div>
                <div style="margin-top:10px; font-size:13px; color:#6c757d;">
                    <div>时间：${record.timestamp}</div>
                    <div>主题：${record.theme}</div>
                    ${record.media_id ? `<div>文章ID：${record.media_id}</div>` : ''}
                </div>
                <div style="margin-top:10px; font-size:13px; color:#495057;">
                    ${record.message || ''}
                </div>
            </div>
        `;
    });

    recordsList.innerHTML = html;
}

// 清空记录
function clearRecords() {
    if (!confirm('确认清空所有发布记录？此操作不可恢复！')) {
        return;
    }

    state.records = [];
    displayRecords();
    alert('记录已清空');
}

// 测试配置
async function testConfig() {
    showLoading('正在测试连接...');

    try {
        const result = await publishToBackend({
            action: 'test_config'
        });

        hideLoading();

        if (result.success) {
            alert('配置测试成功！\n\n' +
                `AI服务：${result.ai_status}\n` +
                `微信API：${result.wechat_status}`);
        } else {
            alert(`配置测试失败：${result.message}`);
        }

    } catch (error) {
        hideLoading();
        alert(`测试失败：${error.message}`);
    }
}

// 保存配置
function saveConfig() {
    const config = {
        ai_provider: document.getElementById('ai-provider').value,
        api_key: document.getElementById('api-key').value,
        wechat_appid: document.getElementById('wechat-appid').value,
        wechat_secret: document.getElementById('wechat-secret').value,
        image_engine: document.getElementById('image-engine').value
    };

    localStorage.setItem('wechat_config', JSON.stringify(config));
    alert('配置已保存！');
}

// 加载配置
function loadConfig() {
    const saved = localStorage.getItem('wechat_config');
    if (saved) {
        const config = JSON.parse(saved);
        if (config.ai_provider) document.getElementById('ai-provider').value = config.ai_provider;
        if (config.api_key) document.getElementById('api-key').value = config.api_key;
        if (config.wechat_appid) document.getElementById('wechat-appid').value = config.wechat_appid;
        if (config.wechat_secret) document.getElementById('wechat-secret').value = config.wechat_secret;
        if (config.image_engine) document.getElementById('image-engine').value = config.image_engine;
    }
}

// 更新今日发布数
function updateTodayCount() {
    document.getElementById('today-count').textContent = state.todayCount;
}

// 调用后端API
async function publishToBackend(data) {
    const apiMap = {
        'quick_publish': '/api/quick_publish',
        'generate_preview': '/api/generate_preview',
        'publish_preview': '/api/publish_preview',
        'batch_publish': '/api/batch_publish',
        'test_config': '/api/test_config'
    };

    const url = apiMap[data.action];
    if (!url) {
        throw new Error('未知的操作类型: ' + data.action);
    }

    console.log('发送请求到:', url, '数据:', data);

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        console.log('响应状态:', response.status, response.statusText);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('响应错误:', errorText);
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }

        const result = await response.json();
        console.log('响应数据:', result);

        // 如果是异步任务，轮询获取结果
        if (result.success && result.task_id) {
            return await pollTaskResult(result.task_id);
        }

        return result;

    } catch (error) {
        console.error('API 调用失败:', error);
        throw error;
    }
}

// 轮询任务结果
async function pollTaskResult(taskId, maxAttempts = 60, interval = 2000) {
    console.log('开始轮询任务:', taskId);

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
        try {
            const response = await fetch(`/api/task/${taskId}`);
            const data = await response.json();

            console.log(`轮询第 ${attempt + 1} 次:`, data);

            if (!data.success) {
                throw new Error(data.message || '查询任务失败');
            }

            if (data.status === 'completed') {
                return data.result;
            }

            if (data.status === 'failed') {
                throw new Error(data.result?.message || '任务执行失败');
            }

            // 任务还在处理中，等待后继续轮询
            await new Promise(resolve => setTimeout(resolve, interval));

        } catch (error) {
            console.error('轮询失败:', error);
            throw error;
        }
    }

    throw new Error('任务超时，请稍后刷新页面查看结果');
}

// 获取记录
async function fetchRecords() {
    const response = await fetch('/api/records');
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    loadConfig();
    refreshRecords();
    updateTodayCount();
});
