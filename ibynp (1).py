
# Cell 1: Imports and sample data
import pandas as pd
import requests

user_profile = {
    "name": "Alex Johnson",
    "profession": "Data Analyst",
    "experience_years": 4,
    "career_goals": "Advance into Data Science",
    "career_interests": ["IT", "Data Science", "AI"]
}

skills_data = {
    'Skill': ['Python', 'SQL', 'Machine Learning', 'Deep Learning', 'Cloud Computing', 'Big Data', 'Communication'],
    'Current Level': [4,4,2,1,1,1,5],
    'Target Level': [5,5,4,3,3,3,5]
}
df_skills = pd.DataFrame(skills_data)

# Cell 2: Skill gap analysis function
def skill_gap_analysis_df(df):
    df['Gap'] = df['Target Level'] - df['Current Level']
    return df

# Cell 3: Fetch live industry news for a given industry (replace YOUR_API_KEY with an actual one)
def fetch_industry_news(industry):
    NEWS_API_KEY = '7bdee1423c924023b081298e1edc98d1'
    url = f'https://newsapi.org/v2/everything?q={industry}&apiKey={NEWS_API_KEY}&pageSize=5&sortBy=publishedAt'
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return [(a['title'], a['url']) for a in articles]
    else:
        return []

# Example usage:
news_items = fetch_industry_news('Data Science')
for title, url in news_items:
    print(f"- {title}\n  {url}")

# Cell 4: Analytical mentor response logic
def get_analytical_mentor_response(user_input, context):
    user_input_lower = user_input.lower()
    timeline = context.get('timeline', None)
    prep_level = context.get('prep_level', None)

    if "leadership" in user_input_lower:
        return ("To build leadership skills, focus on communication, decision-making, and managing teams. "
                "Courses on organizational behavior and management help.")
    elif "career growth" in user_input_lower:
        plan = ("Assess current skills, identify gaps, set SMART goals, create a learning path "
                "using training, mentorship, and practical projects.")
        if context.get('industry'):
            plan += f" For {context['industry']} sector, leverage specialized resources."
        return plan
         elif "interview" in user_input_lower:
        return ("Prepare for interviews by practicing behavioral and technical questions, understanding role demands, "
                "and doing mock interviews with feedback.")
    else:
        return ("Please specify your career domain, current role, goals, and timeline so I can provide tailored guidance.")

response = get_analytical_mentor_response("I want to grow in leadership", {"industry": "Healthcare"})
print(response)
