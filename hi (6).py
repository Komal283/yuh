import streamlit as st
import pandas as pd
import requests

# Sample user profile and skill data
user_profile = {
    "name": "Alex Johnson",
    "profession": "Data Analyst",
    "experience_years": 4,
    "career_goals": "Advance into Data Science",
    "career_interests": ["IT", "Data Science", "AI"]
}

skills_data = {
    'Skill': ['Python', 'SQL', 'Machine Learning', 'Deep Learning', 'Cloud Computing', 'Big Data', 'Communication'],
    'Current Level': [4, 4, 2, 1, 1, 1, 5],
    'Target Level': [5, 5, 4, 3, 3, 3, 5]
}

df_skills = pd.DataFrame(skills_data)

learning_resources = [
    {"title": "Deep Learning Specialization", "platform": "Coursera", "level": "Advanced", "free": False},
    {"title": "AWS Cloud Practitioner", "platform": "AWS Training", "level": "Beginner", "free": True},
    {"title": "Big Data Fundamentals", "platform": "edX", "level": "Beginner", "free": True},
    {"title": "Effective Communication", "platform": "LinkedIn Learning", "level": "All", "free": False}
]

def skill_gap_analysis_df(df):
    df['Gap'] = df['Target Level'] - df['Current Level']
    return df

def fetch_industry_news(industry):
    NEWS_API_KEY = ''  # <-- Put your NewsAPI.org key here
    url = f'https://newsapi.org/v2/everything?q={industry}&apiKey={NEWS_API_KEY}&pageSize=5&sortBy=publishedAt'
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        return [(a['title'], a['url']) for a in articles]
    except Exception:
        return []

def get_analytical_mentor_response(user_input, context):
    user_input_lower = user_input.lower()
    timeline = context.get('timeline', None)
    prep_level = context.get('prep_level', None)

    if "leadership" in user_input_lower:
        return ("To build leadership skills, focus on communication, decision-making, and managing teams. "
                "Consider courses on organizational behavior and management.")
    elif "career growth" in user_input_lower:
        plan = ("Assess current skills, identify gaps, set SMART goals, and create a learning path "
                "involving training, mentorship, and projects.")
        if context.get('industry'):
            plan += f" Tailored resources for {context['industry']} industry can help."
        return plan
    elif "interview" in user_input_lower:
        return ("Prepare for interviews by practicing behavioral and role-specific questions. "
                "Do mock interviews and seek feedback to improve.")
    else:
        return ("Please specify your career domain, current role, goals, and timeline for more tailored advice.")

# Streamlit app starts here
st.set_page_config(page_title="Universal Career & Skills Advisor", layout="wide")

menu = ["Dashboard", "Career Path", "Skills & Courses", "Insights", "Progress Tracker", "Mentorship Chatbot", "Industry News"]
choice = st.sidebar.selectbox("Navigation", menu)

def show_dashboard():
    st.header("Welcome, " + user_profile["name"])
    st.write(f"Profession: {user_profile['profession']}")
    st.write(f"Experience: {user_profile['experience_years']} years")
    st.write(f"Career Goal: {user_profile['career_goals']}")
    gap_df = skill_gap_analysis_df(df_skills.copy())
    st.subheader("Skill Gap Analysis")
    st.bar_chart(gap_df.set_index('Skill')['Gap'])

def show_career_path():
    st.header("Career Path Recommendations")
    gap_df = skill_gap_analysis_df(df_skills.copy())
    missing_skills = gap_df[gap_df["Gap"] > 0]["Skill"].tolist()
    st.write("Current Skills:", ", ".join(df_skills[df_skills["Current Level"] > 0]["Skill"].tolist()))
    st.write("Missing Skills:", ", ".join(missing_skills) if missing_skills else "None!")
    st.write("Suggested Actions:")
    st.markdown("""
    - Enroll in advanced courses tailored to your missing skills.
    - Build hands-on projects to strengthen skills.
    - Network with professionals in your domain.
    """)

def show_skills_courses():
    st.header("Learning Hub")
    platforms = sorted({item["platform"] for item in learning_resources})
    selected_platforms = st.multiselect("Filter by Platform", platforms)
    filtered = [c for c in learning_resources if c["platform"] in selected_platforms] if selected_platforms else learning_resources
    for course in filtered:
        st.write(f"**{course['title']}** ({course['level']}) - {course['platform']} - {'Free' if course['free'] else 'Paid'}")

def show_insights():
    st.header("Career Insights & Trends")
    st.write("- Top skills in demand: Python, Machine Learning, Cloud Computing")
    st.write("- Median salary for Data Scientist in US: $120k")
    st.write("- Success story: Jane went from Analyst to Lead Scientist in 3 years")

def show_progress_tracker():
    st.header("Progress Tracker")
    gap_df = skill_gap_analysis_df(df_skills.copy())
    certs_completed = ["Data Science Certificate", "Python Fundamentals"]
    acquired_skills = gap_df[gap_df["Current Level"] >= 3]["Skill"].tolist()
    st.write("Skills acquired:", ", ".join(acquired_skills))
    st.write("Certifications:", ", ".join(certs_completed))
    st.progress(len(acquired_skills) / len(gap_df))

def show_mentor_chat():
    st.header("Analytical Mentor Chatbot")
    if "context" not in st.session_state:
        st.session_state.context = {}
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask your career question here...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        text_lower = user_input.lower()
        if "timeline:" in text_lower:
            timeline_val = user_input.split("timeline:")[-1].strip()
            st.session_state.context["timeline"] = timeline_val
            response = f"Timeline noted: {timeline_val}."
        elif "prep level:" in text_lower:
            prep_val = user_input.split("prep level:")[-1].strip()
            st.session_state.context["prep_level"] = prep_val
            response = f"Preparation level recorded: {prep_val}."
        else:
            response = get_analytical_mentor_response(user_input, st.session_state.context)

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            st.markdown(response)

def show_industry_news():
    st.header("Latest Industry News")
    industry = st.text_input("Enter your industry (e.g. Data Science, Healthcare, Finance)", "Data Science")
    if industry:
        news_items = fetch_industry_news(industry)
        if news_items:
            for title, url in news_items:
                st.markdown(f"- [{title}]({url})")
        else:
            st.write("No news found or unable to fetch.")

page_map = {
    "Dashboard": show_dashboard,
    "Career Path": show_career_path,
    "Skills & Courses": show_skills_courses,
    "Insights": show_insights,
    "Progress Tracker": show_progress_tracker,
    "Mentorship Chatbot": show_mentor_chat,
    "Industry News": show_industry_news
}

page_map.get(choice, show_dashboard)()

