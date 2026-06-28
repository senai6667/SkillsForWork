from flask import Flask, request, jsonify
from flask_cors import CORS
from jobs_data import JOBS

app = Flask(__name__)
CORS(app) # 允许前端任意端口访问

def calculate_relevance(user_skills, job_keywords):
    """
    计算相关性：用户技能列表与岗位关键词列表的交集数量
    """
    user_skills_lower = [s.strip().lower() for s in user_skills]
    job_keywords_lower = [kw.strip().lower() for kw in job_keywords]
    matches = sum(1 for skill in user_skills_lower if skill in job_keywords_lower)
    return matches

@app.route('/api/recommend', methods = ['POST'])

def recommend():
    data = request.get_json()
    skills_str = data.get("skills", '')
    if not skills_str:
        return jsonify([])
    user_skills = [s.strip() for s in skills_str.replace("，", ",").split(",") if s.strip()]
    
    results = []
    
    for job in JOBS:
        relevance = calculate_relevance(user_skills, job['jd_keywords'])
        results.append(
            {
                "title": job["title"],
                "relevance": relevance,
                "matched_keywords":[kw for kw in job['jd_keywords'] if kw.lower() in [s.lower() for s in user_skills]],
                "all_keywords": job['jd_keywords']
            }
        )
    
    # 按照相关性从高到低排序
    results.sort(key=lambda x: x['relevance'], reverse = True)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug = True, port = 5000)