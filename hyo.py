# Place all imports at the top
import streamlit as st
import pandas as pd
import requests
from openai import OpenAI
import os
import toml
import openai

import openai

def get_openai_api_key():
    # Check Streamlit secrets first
    api_key = st.secrets.get("OPENAI_API_KEY")
    if api_key:
        return api_key
    # Fallback to local secrets.toml
    if os.path.exists("secrets.toml"):
        config = toml.load("secrets.toml")
        return config.get("OPENAI_API_KEY")
    return None

api_key = get_openai_api_key()
if not api_key:
    st.error("OpenAI API key is missing! Please set it in Streamlit secrets or secrets.toml")
    st.stop()

openai.api_key = api_key
# Centralized model config
MODEL_NAME = "gpt-4o"  # Keep consistent with actual usage

def get_openai_client():
    api_key = get_openai_api_key()
    if not api_key:
        st.error("OpenAI API key is missing! Please set it in Streamlit secrets or secrets.toml")
        st.stop()
    return OpenAI(api_key=api_key)

# ... rest of your code ...

def get_ai_mentor_response(user_input):
    profile = st.session_state.user_profile or {}
    context = st.session_state.context or {}

    prompt_messages = [
        {"role": "system", "content": "You are a helpful career mentor AI assistant."},
        {"role": "user", "content": f"User Profile: {profile}, Context: {context}, Question: {user_input}"}
    ]

    client = get_openai_client()  # Ensures centralized, robust client initialization

    response = client.chat.completions.create(
        model=MODEL_NAME,  # Use centralized config
        messages=prompt_messages,
        max_tokens=400,
        temperature=0.7,
    )

    return response.choices[0].message.content

# Initialize session state variables
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

if "personal_skills" not in st.session_state:
    st.session_state.personal_skills = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "context" not in st.session_state:
    st.session_state.context = {}

skills_by_profession = {
    "Data Analyst": ['Python', 'SQL', 'Data Visualization', 'Statistics'],
    "Software Engineer": ['Python', 'Algorithms', 'Data Structures', 'System Design'],
    "Project Manager": ['Leadership', 'Project Planning', 'Risk Management', 'Agile'],
    "Student": ['Time Management', 'Research', 'Presentation Skills'],
}

skills_by_industry = {
    "IT": ['Cloud Computing', 'Machine Learning', 'Python'],
    "Healthcare": ['Medical Terminology', 'Patient Care', 'Data Compliance'],
    "Finance": ['Financial Modeling', 'Risk Analysis', 'Excel'],
    "Education": ['Curriculum Planning', 'Teaching Skills', 'Assessment Design'],
    "Engineering": ['CAD', 'Mathematics', 'Project Management'],
    "Others": []
}

def get_skills_for_user(profile):
    prof_skills = skills_by_profession.get(profile['profession'], [])
    industry_skills = []
    for ind in profile.get('career_interests', []):
        industry_skills.extend(skills_by_industry.get(ind, []))
    return list(set(prof_skills + industry_skills))

def skill_gap_analysis_df(skills_dict):
    data = []
    for skill, levels in skills_dict.items():
        current = levels.get('current', 0)
        target = levels.get('target', 0)
        data.append({'Skill': skill, 'Current Level': current, 'Target Level': target, 'Gap': target - current})
    return pd.DataFrame(data)

def fetch_industry_news(industry):
    NEWS_API_KEY = st.secrets.get("NEWS_API_KEY") or os.getenv("NEWS_API_KEY") or "YOUR_NEWSAPI_KEY"
    url = f'https://newsapi.org/v2/everything?q={industry}&pageSize=5&sortBy=publishedAt&apiKey={NEWS_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        return [(a['title'], a['url']) for a in articles]
    except:
        return []

def get_ai_mentor_response(user_input):
    profile = st.session_state.user_profile or {}
    context = st.session_state.context or {}

    prompt_messages = [
        {"role": "system", "content": "You are a helpful career mentor AI assistant."},
        {"role": "user", "content": f"User Profile: {profile}, Context: {context}, Question: {user_input}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=prompt_messages,
        max_tokens=400,
        temperature=0.7,
    )

    return response.choices[0].message.content

def user_profile_form():
    st.header("Create Your Career Profile")
    name = st.text_input("Full Name")
    profession = st.selectbox("Current Profession or Role", list(skills_by_profession.keys()))
    experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
    career_goal = st.text_area("Career Goals")
    industries = st.multiselect("Select Your Industries of Interest", list(skills_by_industry.keys()))

    if st.button("Save Profile"):
        if not name or not career_goal:
            st.error("Please fill all required fields.")
        else:
            st.session_state.user_profile = {
                "name": name,
                "profession": profession,
                "experience_years": experience,
                "career_goals": career_goal,
                "career_interests": industries
            }
            st.success("Profile saved! Use the sidebar to navigate.")

def skill_rating_form():
    st.subheader("Personalize Your Skills & Set Proficiency Levels")
    profile = st.session_state.user_profile
    personal_skills = st.session_state.personal_skills

    skills = get_skills_for_user(profile)
    for skill in skills:
        col1, col2 = st.columns([2, 3])
        with col1:
            st.write(skill)
        with col2:
            curr_level = st.slider(f"Current level for {skill}", 0, 5,
                                   value=personal_skills.get(skill, {}).get('current', 0),
                                   key=f"current_{skill}")
            target_level = st.slider(f"Target level for {skill}", curr_level, 5,
                                     value=personal_skills.get(skill, {}).get('target', curr_level),
                                     key=f"target_{skill}")
        personal_skills[skill] = {'current': curr_level, 'target': target_level}
    st.session_state.personal_skills = personal_skills

def show_dashboard():
    profile = st.session_state.user_profile
    st.header(f"Welcome, {profile['name']}!")
    st.write(f"Profession: {profile['profession']}")
    st.write(f"Experience: {profile['experience_years']} years")
    st.write(f"Career Goals: {profile['career_goals']}")

    if not st.session_state.personal_skills:
        st.info("Please personalize your skills first in 'Skills & Courses'.")
        return

    gap_df = skill_gap_analysis_df(st.session_state.personal_skills)
    st.subheader("Skill Gap Analysis")
    st.dataframe(gap_df)
    st.bar_chart(gap_df.set_index('Skill')['Gap'])

def show_skills_courses():
    skill_rating_form()
    st.subheader("Recommended Courses")

    learning_resources = [
        {"title": "Deep Learning Specialization", "platform": "Coursera", "level": "Advanced", "free": False},
        {"title": "AWS Cloud Practitioner", "platform": "AWS Training", "level": "Beginner", "free": True},
        {"title": "Big Data Fundamentals", "platform": "edX", "level": "Beginner", "free": True},
        {"title": "Effective Communication Skills", "platform": "LinkedIn Learning", "level": "All", "free": False}
    ]

    platforms = sorted({course['platform'] for course in learning_resources})
    selected_platforms = st.multiselect("Filter by Platform", platforms)
    filtered_courses = [c for c in learning_resources if c['platform'] in selected_platforms] if selected_platforms else learning_resources
    for course in filtered_courses:
        st.write(f"**{course['title']}** ({course['level']}) - {course['platform']} - {'Free' if course['free'] else 'Paid'}")

def show_mentor_chat():
    st.header("AI Mentor Chatbot")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    user_input = st.chat_input("Ask your career question here...")
    if user_input:
     import re

def parse_special_commands(user_input):
    """
    Parse special commands from user input and update context if needed.
    Supported commands:
      - timeline: <value>
      - prep level: <value>
    """
    command_patterns = {
        "timeline": r"timeline:\s*(.*)",
        "prep_level": r"prep level:\s*(.*)"
    }
    for key, pattern in command_patterns.items():
        match = re.search(pattern, user_input, flags=re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            if not value:
                return f"{key.replace('_', ' ').capitalize()} value missing. Please provide a value."
            st.session_state.context[key] = value
            return f"{key.replace('_', ' ').capitalize()} recorded: {value}."
    return None

def show_mentor_chat():
    st.header("AI Mentor Chatbot")
    # chat_history initialization should be at app startup, not here

    for msg in st.session_state.chat_history:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    user_input = st.chat_input("Ask your career question here...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Parse for special commands
        response = parse_special_commands(user_input)
        if response is None:
            try:
                response = get_ai_mentor_response(user_input)
            except Exception as e:
                response = f"Sorry, there was an error: {e}"

        st.session_state.chat_history.append({"role": "assistant", "content": response})

def show_industry_news():
    st.header("Latest Industry News")
    industry = st.text_input("Enter your industry (e.g., Data Science, Healthcare, Finance)", "Data Science")
    if industry:
        news_items = fetch_industry_news(industry)
        if news_items:
            for title, url in news_items:
                st.markdown(f"- [{title}]({url})")
        else:
            st.info("No news found or unable to fetch.")

st.set_page_config(page_title="AI-Powered Career Advisor", layout="wide")

menu = ["Dashboard", "Skills & Courses", "Mentorship Chatbot", "Industry News"]  # Example menu list

if not st.session_state.get("user_profile"):
    user_profile_form()
    st.stop()  # Prevent further execution until profile is set

# Safely get the user name, fallback to "User" if not set
user_name = st.session_state.user_profile.get('name', 'User')
choice = st.sidebar.selectbox(f"Hello, {user_name}! Navigate:", menu)

page_funcs = {
    "Dashboard": show_dashboard,
    "Skills & Courses": show_skills_courses,
    "Mentorship Chatbot": show_mentor_chat,
    "Industry News": show_industry_news
}

page_funcs[choice]()
