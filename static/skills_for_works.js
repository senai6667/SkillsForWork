const API_URL = "http://127.0.0.1/5000/api/api_skills_for_works"

const skills_input = document.getElementById('skills')
const search = document.querySelector('.search')
const results = document.querySelector('.results')
const recommand_btn = document.getElementById('recommand')

recommand_btn.addEventListener('click', async () =>{
    const skills = skills_input.value.trim();
    if (!skills) {
        results.innerHTML = '<div class="no_input">请输入你的技能，例如：Python，Excel，沟通能力强</div>';
        return;
    }

    search.classList.remove('hidden');
    results.innerHTML = '';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({skills: skills})
        });

        if(!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const jobs = await response.json();
        display_results(jobs);
    } catch(error) {
        console.error('请求失败:', error);
        results.innerHTML = '<div class="no_link">后端服务器未启动？请确保后端正在运行</div>';
    } finally {
        search.classList.add('hidden');
    }
});

function display_results(jobs) {
    if (!jobs.length) {
        results.innerHTML = '<div class="content">没有找到匹配的岗位，请尝试输入更多的技能，如：Python，Java，C++</div>';
        return;
    }

    const html = jobs.map(job => {
        const matched_keywords_html = job.matched_keywords.length > 0 
        ? `<p class="match_keywords">匹配上的关键词：${job.matched_keywords.map(s => `<span>${s}</span>`).join((''))}</p>` 
        : `<p class="match_keywords">没有找到合适的岗位，可补充技能提高相关性</p>`;
        
        const all_keywords_html = `<p class="works_keywords">岗位相关技能：${job.all_keywords.map(s => `<span>${s}</span>`).join((''))}</p>`;

        return `
            <div class="content">
                <h3>${job.title}</h3>
                <p class="match_level">匹配度${job.relevance}个技能</p>
                ${matched_keywords_html}
                ${all_keywords_html}
            </div>
        `;
    }).join('');

    results.innerHTML = html;
}