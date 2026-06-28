const API_URL = "http://127.0.0.1:5000/api/recommend";

const skillsInput = document.getElementById('skillsInput');
const recommendBtn = document.getElementById('recommendBtn');
const loadingDiv = document.getElementById('loading');
const resultsDiv = document.getElementById('results');

recommendBtn.addEventListener('click', async () => {
    const skills = skillsInput.value.trim();
    if (!skills) {
        resultsDiv.innerHTML = '<div class="job-card" style="background:#fff2f0;">⚠️ 请输入你的技能，例如：Python, Excel, 沟通能力</div>';
        return;
    }

    // 显示loading，清空旧结果
    loadingDiv.classList.remove('hidden');
    resultsDiv.innerHTML = '';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ skills: skills })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const jobs = await response.json();
        displayResults(jobs);
    } catch (error) {
        console.error('请求失败:', error);
        resultsDiv.innerHTML = `<div class="job-card" style="background:#fee2e2;">❌ 后端服务未启动？请确认后端已运行 (python backend/app.py)</div>`;
    } finally {
        loadingDiv.classList.add('hidden');
    }
});

function displayResults(jobs) {
    if (!jobs.length) {
        resultsDiv.innerHTML = '<div class="job-card">😢 没有找到匹配的岗位，试试输入更多技能（如 Python、SQL）</div>';
        return;
    }

    const html = jobs.map(job => {
        const matchedKeywordsHtml = job.matched_keywords.length 
            ? `<div class="keywords">✨ 匹配上的JD关键词：${job.matched_keywords.map(k => `<span class="matched">${k}</span>`).join('')}</div>`
            : `<div class="keywords">🔍 暂无直接匹配，可补充技能提高相关性</div>`;
        
        const allKeywordsHtml = `<div class="keywords">📌 岗位相关技能：${job.all_keywords.map(k => `<span class="keyword-tag">${k}</span>`).join('')}</div>`;

        return `
            <div class="job-card">
                <h3>
                    ${job.title}
                    <span class="relevance-badge">匹配度 ${job.relevance} 个技能</span>
                </h3>
                ${matchedKeywordsHtml}
                ${allKeywordsHtml}
            </div>
        `;
    }).join('');
    
    resultsDiv.innerHTML = html;
}