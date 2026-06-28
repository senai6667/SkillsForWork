import requests
from bs4 import BeautifulSoup
import json
import time

# 目标网站
URL = "https://realpython.github.io/fake-jobs/"

# 伪装成浏览器
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15"
}

def get_job_cards():
    print(f"正在请求{URL}响应...")
    response = requests.get(URL, headers=HEADERS)
    if (response.status_code != 200):
        print(f"请求失败，状态码: {response}")
        return []
    
    #用beautifulSoup解析html网站
    soup = BeautifulSoup(response.text, "lxml")
    
    cards = soup.find_all("div", class_ = "card")
    print(f"共找到{len(cards)}个职位卡片")
    
    return cards

def extract_job_info(card):
    # 从单个岗位中提取岗位名称、公司、简介、关键词
    # 职位标题
    title_elem = card.find("h2", class_ = "title")
    title = title_elem.text.strip() if title_elem else " 未知岗位"
    
    # 公司名称
    company_elem = card.find("h3", class_ = "company")
    company = company_elem.text.strip() if company_elem else "未知公司"
    
    # 职位简介/描述（里面可能包含近技能要求）
    description_elem = card.find("div", class_ = "description")
    description = description_elem.text.strip() if description_elem else ""
    
    # 从描述中提取关键词
    keywords = extract_keywords_from_description(description)
    
    return {
        "title": title,
        "company": company,
        "description": description[:200] + "..." if len(description)>200 else description,
        "keywords": keywords
    }
    
def extract_keywords_from_description(text):
    # 小写化，便于匹配
    
    text_lower = text.lower()
    skill_words = ["python", "java", "javascript", "html", "data analyse", "c++"]
    found = []
    for skill in skill_words:
        if skill in text_lower:
            found.append(skill)
    return list(set(found))

def save_jobs_to_json(jobs, filename = "jobs_from_web.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"已保存{len(jobs)}条岗位数据到{filename}")

def main():
    cards = get_job_cards()
    
    if not cards:
        return
    
    all_jobs = []
    for idx, card in enumerate(cards, 1):
        job_info = extract_job_info(card)
        
        all_jobs.append(job_info)
        print(f"（{idx}）已提取：{job_info['title']}@{job_info['company']}")
        
        time.sleep(0.5)
        save_jobs_to_json(all_jobs)
        
        # 打印前三个展示
        print("\n===前三个岗位展示===")
        for job in all_jobs[:3]:
            print(f"职位：{job['title']}")
            print(f"关键词: {job['company']}")
            print("-" * 40)
        

# 调用函数
if __name__ == "__main__":
    main()