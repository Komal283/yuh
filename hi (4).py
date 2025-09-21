
import streamlit as st
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

def skill_gap_analysis_df(df):
    df['Gap'] = df['Target Level'] - df['Current Level']
    return df

def fetch_industry_news(industry):
    NEWS_API_KEY = ''  # Replace elif "interview" in user_input_lower:
        return ("Prepare for interviews by practicing behavioral and technical questions, understanding role demands, "
                "and doing mock interviews with feedback.")
    else:
        return ("Please specify your career domain, current role, goals, and timeline so I can provide tailored guidance.")

response = get_analytical_mentor_response("I want to grow in leadership", {"industry": "Healthcare"})
print(response)
 with your NewsAPI key
    url = f'https://newsapi.org/v2/everything?q={industry}&apiKey={NEWS_API_KEY}&pageSize=5&sortBy=publishedAt'
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return [(a['title'], a['url']) for a in articles]
    else:
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

st.set_page_config(page_title="Universal Career Advisor", layout="wide")

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
    missing_skills = gap_df[gap_df['Gap'] > 0]['Skill'].tolist()
    st.write("Current Skills:", ", ".join(df_skills[df_skills['Current Level'] > 0]['Skill'].tolist()))
    st.write("Missing Skills:", ", ".join(missing_skills) if missing_skills else "None!")
    st.write("Suggested Activities:")
    st.markdown("- Take relevant advanced courses\n- Participate in projects\n- Network with professionals")

def show_skills_courses():
    st.header("Learning Hub")
    platforms = sorted({lr["platform"] for lr in learning_resources})
    selected_platforms = st.multiselect("Filter by Platform", platforms)
    courses = [lr for lr in learning_resources if lr["platform"] in selected_platforms] if selected_platforms else learning_resources
    for c in courses:
        st.write(f"**{c['title']}** ({c['level']}) - {c['platform']} - {'Free' if c['free'] else 'Paid'}")

def show_insights():
    st.header("Career Insights & Trends")
    st.write("- Top skills in demand: Python, Machine Learning, Cloud Computing")
    st.write("- Median salary for Data Scientist in US: $120k")
    st.write("- Success story: Jane Doe advanced from Analyst to Lead Scientist in 3 years")

def show_progress_tracker():
    st.header("Progress Tracker")
    gap_df = skill_gap_analysis_df(df_skills.copy())
    certs = ["Data Science Certificate", "Python Fundamentals"]
    acquired_skills = gap_df[gap_df["Current Level"] >= 3]["Skill"].tolist()
    st.write("Skills acquired:", ", ".join(acquired_skills))
    st.write("Certifications:", ", ".join(certs))
    st.progress(len(acquired_skills) / len(gap_df))

def show_mentor_chat():
    st.header("Analytical Mentor Chatbot")

    if "context" not in st.session_state:
        st.session_state.context = {}
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    user_text = st.chat_input("Ask your career-related question...")

    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})

        # Extract timeline or prep level context from simple keywords in input
        low_text = user_text.lower()
        if "timeline:" in low_text:
            timeline_val = user_text.split("timeline:")[-1].strip()
            st.session_state.context["timeline"] = timeline_val
            bot_resp = f"Thanks, timeline set to: {timeline_val}."
        elif "prep level:" in low_text:
            prep_val = user_text.split("prep level:")[-1].strip()
            st.session_state.context["prep_level"] = prep_val
            bot_resp = f"Preparation level recorded as: {prep_val}."
        else:
            bot_resp = get_analytical_mentor_response(user_text, st.session_state.context)

        st.session_state.messages.append({"role": "assistant", "content": bot_resp})
        with st.chat_message("user"):
            st.markdown(user_text)
        with st.chat_message("assistant"):
            st.markdown(bot_resp)

def show_industry_news():
    st.header("Latest Industry News")
    industry = st.text_input("Enter your industry (e.g. Data Science, Healthcare, Finance)", "Data Science")
    if industry:
        news = fetch_industry_news(industry)
        if news:
            for title, url in news:
                st.markdown(f"- [{title}]({url})")
        else:
            st.write("No news found or API error.")

page_functions = {
    "Dashboard": show_dashboard,
    "Career Path": show_career_path,
    "Skills & Courses": show_skills_courses,
    "Insights": show_insights,
    "Progress Tracker": show_progress_tracker,
    "Mentorship Chatbot": show_mentor_chat,
    "Industry News": show_industry_news
}

page_functions.get(choice, show_dashboard)()

