import streamlit as st

# --- Comprehensive career map by field ---
career_map = {
    "ai": ["AI Engineer", "ML Researcher", "MLOps Engineer"],
    "data": ["Data Scientist", "Data Analyst", "ML Engineer"],
    "embedded": ["Embedded Systems Engineer", "Firmware Engineer", "IoT Developer"],
    "web": ["Full-stack Developer", "Frontend Engineer", "Backend Engineer"],
    "robotics": ["Robotics Engineer", "Control Systems Engineer"],
    "security": ["Security Engineer", "Cloud Security Analyst"],
    
    "government": [
        "Sub Inspector", "Civil Services Officer", "Government Clerk",
        "Customs Officer", "Defence Personnel", "Police Officer"
    ],
    "management": [
        "Business Analyst", "Project Manager", "HR Specialist",
        "Marketing Manager", "Operations Manager", "Consultant",
        "Entrepreneur"
    ],
    "education": [
        "School Teacher", "College Professor", "Education Consultant",
        "Corporate Trainer", "Career Counselor"
    ],
    "finance": [
        "Financial Analyst", "Accountant", "Banker", "Investment Analyst",
        "Auditor", "Tax Consultant"
    ],
    "healthcare": [
        "Doctor", "Nurse", "Pharmacist", "Medical Lab Technician",
        "Physiotherapist", "Healthcare Administrator"
    ],
    "arts": [
        "Graphic Designer", "Animator", "Fashion Designer",
        "Photographer", "Interior Designer", "Musician"
    ],
    "law": [
        "Lawyer", "Legal Advisor", "Paralegal",
        "Judge", "Corporate Lawyer"
    ],
    "media": [
        "Journalist", "Content Writer", "Public Relations Specialist",
        "Social Media Manager", "Video Editor"
    ],
    "science": [
        "Research Scientist", "Lab Technician", "Environmental Scientist",
        "Biologist", "Chemist", "Physicist"
    ],
    "trade": [
        "Electrician", "Plumber", "Carpenter",
        "Mechanic", "Welder", "HVAC Technician"
    ],
    "hospitality": [
        "Hotel Manager", "Travel Agent", "Chef",
        "Tour Guide", "Event Planner"
    ],
    "misc": ["Entrepreneur", "Freelancer", "Volunteer", "Social Worker", "Coach"],
}

def parse_keywords(text):
    t = text.lower()
    keys = []
    if any(word in t for word in ["ai", "machine", "learning"]): keys.append("ai")
    if any(word in t for word in ["data", "analytics", "statistics"]): keys.append("data")
    if any(word in t for word in ["embedded", "firmware", "iot"]): keys.append("embedded")
    if any(word in t for word in ["web", "frontend", "react", "node"]): keys.append("web")
    if any(word in t for word in ["robot", "control", "mechatron"]): keys.append("robotics")
    if any(word in t for word in ["security", "crypt", "privacy"]): keys.append("security")

    if any(word in t for word in ["gov", "government", "exam", "civil", "police", "sub inspector", "defense", "army"]): keys.append("government")
    if any(word in t for word in ["manage", "business", "hr", "project", "marketing", "operations", "consultant", "entrepreneur"]): keys.append("management")
    if any(word in t for word in ["teach", "education", "tutor", "trainer", "counselor"]): keys.append("education")
    if any(word in t for word in ["finance", "account", "bank", "financial", "investment", "auditor", "tax"]): keys.append("finance")
    if any(word in t for word in ["doctor", "nurse", "pharma", "medical", "healthcare", "physio"]): keys.append("healthcare")
    if any(word in t for word in ["design", "artist", "graphic", "animator", "fashion", "photographer", "interior", "music"]): keys.append("arts")
    if any(word in t for word in ["lawyer", "legal", "paralegal", "judge"]): keys.append("law")
    if any(word in t for word in ["journalist", "content", "pr", "social media", "video"]): keys.append("media")
    if any(word in t for word in ["research", "science", "lab", "environmental", "biology", "chemistry", "physics"]): keys.append("science")
    if any(word in t for word in ["electrician", "plumber", "carpenter", "mechanic", "welder", "hvac"]): keys.append("trade")
    if any(word in t for word in ["hotel", "travel", "chef", "tour", "event"]): keys.append("hospitality")
    if any(word in t for word in ["freelance", "volunteer", "social worker", "coach"]): keys.append("misc")

    return list(set(keys))

def suggest_careers(profile):
    text = f"{profile['degree']} {profile['interests']} {profile['strengths']} {profile['goals']}"
    keys = parse_keywords(text)
    suggestions = set()
    for k in keys:
        for job in career_map.get(k, []):
            suggestions.add(job)
    if not suggestions:
        suggestions = {
            "Software Engineer",
            "Data Analyst",
            "Sub Inspector",
            "Business Analyst",
            "Teacher",
            "Financial Analyst",
        }
    return list(suggestions)[:7]

def resume_feedback(text):
    tips = []
    if not text or len(text) < 100:
        tips.append("Resume looks short — add clear headline & 3–5 bullets per role/project.")
    if "skills" not in text.lower():
        tips.append("Add a 'Technical Skills' or relevant skills section listing languages, frameworks, or tools.")
    if "project" not in text.lower() and "intern" not in text.lower():
        tips.append("Include at least 1 concrete project or internship with measurable impact.")
    if not any(x in text for x in ["%", "A", "B", "C"]):
        tips.append("Quantify achievements (e.g., 'reduced latency by 30%').")
    if not tips:
        tips.append("Resume looks solid. Keep bullets concise and results-focused.")
    return tips

def mentor_response(user_msg):
    msg = user_msg.lower()
    tech_keywords = ["ml engineer", "machine learning engineer", "data scientist", "ai engineer", "software developer"]
    government_keywords = ["sub inspector", "civil services", "government jobs", "police", "govt exam", "defense", "army"]
    management_keywords = ["business analyst", "project manager", "hr specialist", "marketing manager", "operations manager"]
    education_keywords = ["teacher", "education consultant", "tutor", "trainer", "counselor"]
    finance_keywords = ["financial analyst", "accountant", "banker", "investment analyst", "auditor", "tax consultant"]
    healthcare_keywords = ["doctor", "nurse", "pharmacist", "medical", "healthcare", "physiotherapist"]
    arts_keywords = ["graphic designer", "animator", "fashion designer", "photographer", "interior designer", "musician"]
    law_keywords = ["lawyer", "legal advisor", "paralegal", "judge"]
    media_keywords = ["journalist", "content writer", "public relations", "social media", "video editor"]
    science_keywords = ["research scientist", "lab technician", "environmental scientist", "biologist", "chemist", "physicist"]
    trade_keywords = ["electrician", "plumber", "carpenter", "mechanic", "welder", "hvac technician"]
    hospitality_keywords = ["hotel manager", "travel agent", "chef", "tour guide", "event planner"]
    
    if any(kw in msg for kw in tech_keywords):
        return ("To pursue a tech career like ML Engineer or Data Scientist, focus on programming (Python), "
                "build data skills & hands-on projects, and target certifications.")
    elif any(kw in msg for kw in government_keywords):
        return ("For government roles like Sub Inspector, Civil Services, or Defence, structured exam preparation, "
                "practice previous papers, and current affairs knowledge are essential.")
    elif any(kw in msg for kw in management_keywords):
        return ("Management careers require communication, leadership, and business knowledge. "
                "Certifications like PMP or courses in business analytics can help.")
    elif any(kw in msg for kw in education_keywords):
        return ("Teaching and education roles need domain expertise and communication skills. "
                "Consider education certifications or degrees.")
    elif any(kw in msg for kw in finance_keywords):
        return ("Finance roles demand financial modeling, accounting skills, and tools proficiency. "
                "Certifications like CFA or CPA enhance job prospects.")
    elif any(kw in msg for kw in healthcare_keywords):
        return ("Healthcare careers require specialized education, training, and licenses. "
                "Hands-on experience and certification are critical.")
    elif any(kw in msg for kw in arts_keywords):
        return ("Arts careers thrive on creativity, portfolio building, and networking. "
                "Consider related certifications or degrees.")
    elif any(kw in msg for kw in law_keywords):
        return ("Legal careers require law degrees and professional certification. Building experience through internships helps.")
    elif any(kw in msg for kw in media_keywords):
        return ("Media careers benefit from writing skills, digital marketing knowledge, and portfolio showcasing.")
    elif any(kw in msg for kw in science_keywords):
        return ("Science careers involve research skills, lab experience, and higher education or certifications.")
    elif any(kw in msg for kw in trade_keywords):
        return ("Trade careers require vocational training and apprenticeships for hands-on skills.")
    elif any(kw in msg for kw in hospitality_keywords):
        return ("Hospitality careers need customer service skills, certifications, and practical experience.")
    elif "career" in msg or "support" in msg:
        return ("Please specify your desired job role and timeline for tailored guidance.")
    else:
        return f"I received your note: '{user_msg}'. Tip: be specific about timelines and measurable outcomes."

# Streamlit UI
st.set_page_config(page_title="Generative AI Career & Skills Advisor", layout="wide")
st.title("🎓 Generative AI Career & Skills Advisor (Python Streamlit Prototype)")
st.write("Fill in your details to get personalized career suggestions, skill roadmap, resume feedback, and interview tips.")

# Sidebar form for user profile
st.sidebar.header("Student Profile")
profile = {
    "name": st.sidebar.text_input("Name"),
    "degree": st.sidebar.text_input("Degree / Major"),
    "year": st.sidebar.text_input("Year / Experience"),
    "interests": st.sidebar.text_area("Interests (comma separated)"),
    "strengths": st.sidebar.text_area("Strengths"),
    "goals": st.sidebar.text_area("Goals"),
}

resume_text = st.sidebar.text_area("Paste Resume / CV (optional)")

if st.sidebar.button("Generate Roadmap"):
    careers = suggest_careers(profile)
    resume_tips = resume_feedback(resume_text)

    st.subheader(f"👋 Hi {profile['name'] or 'Student'}, here are your suggestions:")

    st.write("### 🚀 Suggested Careers")
    st.write(careers)

    st.write("### 📚 Personalized Roadmap")
    for c in careers:
        with st.expander(c):
            st.write("*Courses:* Example courses related to " + c)
            st.write("*Projects:* Example projects for portfolio")
            st.write("*Certifications:* Relevant certifications")

    st.write("### 📝 Resume Feedback")
    for tip in resume_tips:
        st.markdown(f"- {tip}")

    st.write("### 💡 Interview Prep Tips")
    st.markdown("- Prepare 4–6 STAR stories (Situation, Task, Action, Result)")
    st.markdown("- Be ready to explain 1–2 projects end-to-end")
    st.markdown("- Mock interviews for behavioral + technical rounds")

    st.write("### 🛠 Project Ideas")
    st.markdown("- Build a chatbot")
    st.markdown("- IoT sensor dashboard")
    st.markdown("- AI-powered recommendation system")

# Mentor chat section
st.subheader("💬 24/7 Mentor Chat (Prototype)")
if "chat" not in st.session_state:
    st.session_state.chat = []

user_msg = st.text_input("Ask mentor a question:")
if st.button("Send"):
    if user_msg:
        st.session_state.chat.append(("user", user_msg))
        response = mentor_response(user_msg)
        st.session_state.chat.append(("mentor", response))

for role, msg in st.session_state.chat:
    if role == "user":
        st.write(f"*You:* {msg}")
    else:
        st.write(f"*Mentor:* {msg}")
