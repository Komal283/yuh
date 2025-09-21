import streamlit as st
import pandas as pd
from ibynp import user_profile, df_skills, learning_resources, skill_gap_analysis_df, get_mentor_response

st.set_page_config(page_title="Career & Skills Advisor", layout="wide")

# Sidebar menu
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
    
    values = [len(skills_acquired), len(gap_df) - len(skills_acquired)]
    st.progress(len(skills_acquired) / len(gap_df))

def show_mentor_chat():
    st.header("Mentorship & Career Advice Chatbot")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_input = st.text_input("Ask a career question:")

    if st.button("Send"):
        if user_input:
            response = get_mentor_response(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Mentor", response))

    for sender, text in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(f"**Mentor:** {text}")

if choice == "Dashboard":
    show_dashboard()
elif choice == "Career Path":
    show_career_path()
elif choice == "Skills & Courses":
    show_skills_courses()
elif choice == "Insights":
    show_insights()
elif choice == "Progress Tracker":
    show_progress()
elif choice == "Mentorship Chatbot":
    show_mentor_chat()
