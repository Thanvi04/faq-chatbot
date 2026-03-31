import os
import ollama


# ---------- Helper Function ----------
def get_choice(options, user_input):
    user_input = user_input.strip()

    if user_input in options:
        return options[user_input]

    for value in options.values():
        if user_input.lower() == value.lower():
            return value

    return None


print("\n🎓 Welcome to Smart College FAQ Chatbot\n")


# ---------- Branch ----------
branches = {
    "1": "AIML",
    "2": "CSE"
}

print("Select Branch:")
for k, v in branches.items():
    print(f"{k}. {v}")

branch = None
while not branch:
    user_input = input("Enter branch (number or name): ")
    branch = get_choice(branches, user_input)


# ---------- Year ----------
years = {
    "1": "year1",
    "2": "year2",
    "3": "year3",
    "4": "year4"
}

print("\nSelect Year:")
for k in years:
    print(f"{k}. Year {k}")

year = None
while not year:
    user_input = input("Enter year: ")
    year = get_choice(years, user_input)


# ---------- Cycle / Semester ----------
if year == "year1":

    cycles = {
        "1": "physics_cycle",
        "2": "chemistry_cycle"
    }

    print("\nSelect Cycle:")
    print("1. Physics Cycle")
    print("2. Chemistry Cycle")

    cycle = None
    while not cycle:
        user_input = input("Enter cycle: ")
        cycle = get_choice(cycles, user_input)

    path = f"syllabus/{branch}/{year}/{cycle}"

else:

    if year == "year2":
        semesters = {"1": "sem3", "2": "sem4"}
        print("\nSelect Semester:\n1. Sem 3\n2. Sem 4")

    elif year == "year3":
        semesters = {"1": "sem5", "2": "sem6"}
        print("\nSelect Semester:\n1. Sem 5\n2. Sem 6")

    else:
        semesters = {"1": "sem7", "2": "sem8"}
        print("\nSelect Semester:\n1. Sem 7\n2. Sem 8")

    semester = None
    while not semester:
        user_input = input("Enter semester: ")
        semester = get_choice(semesters, user_input)

    path = f"syllabus/{branch}/{year}/{semester}"


# ---------- Show Courses ----------
print("\n📂 Loading courses from:", path)

try:
    files = os.listdir(path)
except:
    print("❌ Folder not found. Check your structure.")
    exit()

courses = {}

print("\n📚 Available Courses:")
for i, file in enumerate(files, start=1):
    name = file.replace(".txt", "")
    courses[str(i)] = name
    print(f"{i}. {name}")


# ---------- Select Course ----------
course = None
while not course:
    user_input = input("\nSelect course (number or name): ")
    course = get_choice(courses, user_input)


# ---------- Load Syllabus ----------
file_path = f"{path}/{course}.txt"

try:
    with open(file_path, "r") as f:
        syllabus = f.read()
except:
    print("❌ Error loading file.")
    exit()

print("\n📖 Syllabus Loaded Successfully!\n")


# ---------- Chat Loop (Ollama LLM) ----------
print("💬 Ask questions about this course (type 'exit' to stop)\n")

while True:
    question = input("Ask: ")

    if question.lower() == "exit":
        print("\n👋 Exiting chatbot. Thank you!")
        break

    # Limit syllabus to avoid slow response
    short_syllabus = syllabus[:2000]

    prompt = f"""
Answer ONLY using this syllabus.
If answer is not present, say: Not mentioned in syllabus.

SYLLABUS:
{short_syllabus}

QUESTION:
{question}
"""

    try:
        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": prompt}]
        )

        print("\n🤖 Chatbot:", response['message']['content'])

    except Exception as e:
        print("\n⚠️ Error: Make sure Ollama is running.")