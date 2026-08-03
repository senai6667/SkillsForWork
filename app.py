from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from jobs_data import JOBS

app = Flask(__name__)
CORS(app) #允许任意端口访问

def calculate_relevance(user_skills, job_keywords):
    user_skills_lower = [s.strip().lower() for s in user_skills]
    job_keywords_lower = [s.strip().lower() for s in job_keywords]
    matches = sum(1 for s in user_skills_lower if s in job_keywords_lower)
    return matches

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/skills_for_works', methods = ['GET'])
def skills_for_works():
    return render_template('skills_for_works.html')

@app.route('/works_for_skills', methods=['GET'])
def works_for_skills():
    return render_template('works_for_skills.html')

@app.route('/api/api_skills_for_works', methods = ['POST'])

def skills_for_works():
    data = request.get_json()
    skills_str = data.get('skills', '')
    if not skills_str:
        return jsonify([])
    
    # 将skills_str换成数组，并去掉空格，中文逗号，以及句号
    skills_str = skills_str.replace('，', ",") # 将中文逗号替换成英文逗号
    skills_str = skills_str.split(",") # 数组
    skills = [] # 整理后的数组
    for s in skills_str:
        if s:
            s = s.strip().rstrip('.').lower()
            skills.append(s)
    
    results = []
    for job in JOBS:
        relevance = calculate_relevance(skills, job['jd_keywords'])
        if relevance:
            results.append({
                "title": job['title'],
                "relevance": relevance,
                "matched_keywords": [kw for kw in job['jd_keywords'] if kw.lower() in skills],
                "all_keywords": job['jd_keywords']
                })
    results.sort(key=lambda x: x['relevance'], reverse= True)
    return jsonify(results)

@app.route('/api/api_works_for_skills', methods = ['POST'])

def works_for_skills():
    data = request.get_json()
    works_str = data.get('works', '')
    if not works_str:
        return jsonify([])
    works_str = works_str.replace('，', ',')
    works_str = works_str.split(',')
    works = []
    results = []
    for w in works_str:
        w = w.strip().rstrip('.').lower()
        works.append(w)
    for w in works:
        for title in JOBS:
            if w in title['title'].lower():
                results.append({
                    "title": title,
                    "skills_number": len(title['jd_keywords']),
                    "all_skills": [kw for kw in title['jd_keywords']]
                })
    return jsonify(results)
                
        
        
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)