import os
import streamlit as st
import ollama

st.title("🎓 Smart College FAQ Chatbot")

# ---------- Branch ----------
branch = st.selectbox("Select Branch", ["AIML", "CSE"])

# ---------- Year ----------
year = st.selectbox("Select Year", ["year1", "year2", "year3", "year4"])

# ---------- Cycle / Semester ----------
path = None

if year == "year1":
    cycle = st.selectbox("Select Cycle", ["physics_cycle", "chemistry_cycle"])
    path = f"syllabus/{branch}/{year}/{cycle}"

else:
    if year == "year2":
        sem = st.selectbox("Select Semester", ["sem3", "sem4"])
    elif year == "year3":
        sem = st.selectbox("Select Semester", ["sem5", "sem6"])
    else:
        sem = st.selectbox("Select Semester", ["sem7", "sem8"])

    path = f"syllabus/{branch}/{year}/{sem}"


# ---------- Load Courses ----------
syllabus = None

if os.path.exists(path):
    files = os.listdir(path)
    courses = [f.replace(".txt", "") for f in files]

    course = st.selectbox("Select Course", courses)

    file_path = f"{path}/{course}.txt"

    try:
        with open(file_path, "r") as f:
            syllabus = f.read()
    except:
        st.error("Error loading syllabus file")


# ---------- Chat ----------
if syllabus:
    st.subheader("💬 Ask Questions")

    question = st.text_input("Enter your question", key="q1")

    if question:
        # Limit syllabus size to avoid slow response
        short_syllabus = syllabus[:2000]

        prompt = f"""
Answer ONLY using this syllabus.
If answer is not present, say: Not mentioned in syllabus.

SYLLABUS:
{short_syllabus}

QUESTION:
{question}
"""

        with st.spinner("Thinking... 🤖"):
            try:
                response = ollama.chat(
                    model="phi3",
                    messages=[{"role": "user", "content": prompt}]
                )

                st.success(response['message']['content'])

            except Exception as e:
                st.error("⚠️ Model not responding. Check Ollama is running.")