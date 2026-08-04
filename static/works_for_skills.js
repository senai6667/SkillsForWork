const API_URL = "http://127.0.0.1:5000/api/api_works_for_skills"

const works_input = document.getElementById('works')
const search = document.querySelector('.search')
const results = document.querySelector('.results')
const recommand_btn = document.getElementById('recommand')

recommand_btn.addEventListener('click', async () =>{
    const works = works_input.value.trim();
    if (!works) {
        results.innerHTML = '<div class="no_input">请输入你的岗位，例如：前端，后端，数据分析</div>';
        return;
    }

    search.classList.remove('hidden');
    results.innerHTML = '';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({works: works})
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
        results.innerHTML = '<div class="content">没有找到匹配的技能，请尝试输入更多的岗位，如：后端，前端，数据分析</div>';
        return;
    }

    const html = jobs.map(job => {
        const all_skills_html = `<p class="works_keywords">岗位相关技能：${job.all_skills.map(s => `<span>${s}</span>`).join((''))}</p>`;

        return `
            <div class="content">
                <h3>${job.title}</h3>
                <p class="match_level">需要的技能数${job.skills_number}</p>
                ${all_skills_html}
            </div>
        `;
    }).join('');

    results.innerHTML = html;
}