import streamlit as st
import pandas as pd
from ibynp import user_profile, df_skills, learning_resources, skill_gap_analysis_df, get_analytical_mentor_response

st.set_page_config(page_title="Career & Skills Advisor", layout="wide")

menu = ["Dashboard", "Career Path", "Skills & Courses", "Insights", "Progress Tracker", "Mentorship Chatbot"]
choice = st.sidebar.selectbox("Navigation", menu)

def show_dashboard():
    st.header("Dashboard Overview")
    st.subheader(f"Welcome, {user_profile['name']}")
    st.write(f"Profession: {user_profile['profession']}")
    st.write(f"Experience: {user_profile['experience_years']} years")
    st.write(f"Career Goals: {user_profile['career_goals']}")
    gap_df = skill_gap_analysis_df(df_skills.copy())
    st.write("### Skill Gap Analysis")
    st.bar_chart(gap_df.set_index('Skill')['Gap'])

def show_career_path():
    st.header("Career Pathway Recommendations")
    gap_df = skill_gap_analysis_df(df_skills.copy())
    missing_skills = gap_df[gap_df["Gap"] > 0]["Skill"].tolist()
    st.write("Your Target Role: Data Scientist")
    st.write("Current Skills:", ", ".join(df_skills[df_skills["Current Level"] > 0]["Skill"].tolist()))
    if missing_skills:
        st.write("Missing Skills:", ", ".join(missing_skills))
    else:
        st.write("No missing skills!")
    st.write("Suggested Actions:")
    st.markdown("""
    - Enroll in “Deep Learning Specialization” (Coursera)
    - Join AWS Cloud Practitioner Course
    - Attend Local AI Meetup
    """)

def show_skills_courses():
    st.header("Skills & Courses Learning Hub")
    platforms = sorted({item['platform'] for item in learning_resources})
    selected_platforms = st.multiselect("Filter by Platform", platforms)
    filtered_courses = [c for c in learning_resources if c["platform"] in selected_platforms] if selected_platforms else learning_resources
    for course in filtered_courses:
        st.write(f"**{course['title']}** ({course['level']}) - {course['platform']} - {'Free' if course['free'] else 'Paid'}")

def show_insights():
    st.header("Career Insights & Trends")
    st.write("- Top skills in demand: Python, Machine Learning, Cloud Computing")
    st.write("- Median salary for Data Scientist in US: $120k")
    st.write("- Success story: Jane Doe advanced from Data Analyst to Lead Scientist in 3 years")

def show_progress():
    st.header("Progress Tracker")
    gap_df = skill_gap_analysis_df(df_skills.copy())
    certs_completed = ["Data Science Certificate", "Python Fundamentals"]
    skills_acquired = gap_df[gap_df["Current Level"] >= 3]["Skill"].tolist()
    st.write("Skills acquired:", ", ".join(skills_acquired))
    st.write("Certifications completed:", ", ".join(certs_completed))
    st.progress(len(skills_acquired) / len(gap_df))

def show_mentor_chat():
    st.header("Analytical Mentor Chatbot")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "context" not in st.session_state:
        st.session_state.context = {}

    # Render existing messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Ask your career or exam question here...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Simple context extraction: timeline and prep level
        input_lower = user_input.lower()
        if "timeline:" in input_lower:
            timeline = user_input.split("timeline:")[-1].strip()
            st.session_state.context["timeline"] = timeline
            response = f"Got it. Your timeline is set to: {timeline}."
        elif "prep level:" in input_lower:
            prep_level = user_input.split("prep level:")[-1].strip()
            st.session_state.context["prep_level"] = prep_level
            response = f"Got it. Your preparation level is: {prep_level}."
        else:
            response = get_analytical_mentor_response(user_input, st.session_state.context)

        st.session_state.chat_history.append({"role": "assistant", "content": response})

        # Display new messages
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            st.markdown(response)

page_funcs = {
    "Dashboard": show_dashboard,
    "Career Path": show_career_path,
    "Skills & Courses": show_skills_courses,
    "Insights": show_insights,
    "Progress Tracker": show_progress,
    "Mentorship Chatbot": show_mentor_chat
}

page_funcs[choice]()

