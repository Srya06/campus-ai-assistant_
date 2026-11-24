"""
Campus Knowledge Base for Campus AI Assistant
Contains structured data for Academic Timetables, Course Prerequisites,
Exam Notices, and Administrative FAQs.
"""

CAMPUS_DATA = {
    "institution": {
        "name": "Apex Institute of Technology & Engineering",
        "academic_year": "2025-2026",
        "current_semester": "Spring (Even) Semester",
        "working_hours": "09:00 AM - 05:00 PM (Monday to Friday)"
    },
    "timetables": {
        "CSE": {
            "Sem 4": {
                "Monday": [
                    {"time": "09:00 - 10:00 AM", "subject": "Design & Analysis of Algorithms (CS401)", "faculty": "Dr. Sharma", "room": "LH-101"},
                    {"time": "10:00 - 11:00 AM", "subject": "Operating Systems (CS402)", "faculty": "Prof. Rao", "room": "LH-101"},
                    {"time": "11:15 - 01:15 PM", "subject": "Algorithms Lab (CS401P)", "faculty": "Dr. Sharma & TA", "room": "Lab 3, CS Block"},
                    {"time": "02:00 - 03:00 PM", "subject": "Discrete Mathematics (MA401)", "faculty": "Dr. Meena", "room": "LH-101"},
                    {"time": "03:00 - 04:00 PM", "subject": "Computer Organization & Architecture (CS403)", "faculty": "Prof. Verma", "room": "LH-101"}
                ],
                "Tuesday": [
                    {"time": "09:00 - 10:00 AM", "subject": "Database Management Systems (CS404)", "faculty": "Dr. Anita Nair", "room": "LH-101"},
                    {"time": "10:00 - 11:00 AM", "subject": "Design & Analysis of Algorithms (CS401)", "faculty": "Dr. Sharma", "room": "LH-101"},
                    {"time": "11:15 - 12:15 PM", "subject": "Operating Systems (CS402)", "faculty": "Prof. Rao", "room": "LH-101"},
                    {"time": "01:00 - 03:00 PM", "subject": "DBMS Lab (CS404P)", "faculty": "Dr. Anita Nair", "room": "Database Lab, 2nd Floor"},
                    {"time": "03:15 - 04:15 PM", "subject": "Universal Human Values (HS401)", "faculty": "Prof. Kapoor", "room": "Auditorium"}
                ],
                "Wednesday": [
                    {"time": "09:00 - 10:00 AM", "subject": "Computer Organization & Architecture (CS403)", "faculty": "Prof. Verma", "room": "LH-101"},
                    {"time": "10:00 - 11:00 AM", "subject": "Database Management Systems (CS404)", "faculty": "Dr. Anita Nair", "room": "LH-101"},
                    {"time": "11:15 - 01:15 PM", "subject": "OS & Shell Scripting Lab (CS402P)", "faculty": "Prof. Rao", "room": "Systems Lab"},
                    {"time": "02:00 - 03:00 PM", "subject": "Discrete Mathematics (MA401)", "faculty": "Dr. Meena", "room": "LH-101"},
                    {"time": "03:00 - 04:00 PM", "subject": "Library / Seminar Hour", "faculty": "Faculty Advisor", "room": "Central Library"}
                ],
                "Thursday": [
                    {"time": "09:00 - 10:00 AM", "subject": "Operating Systems (CS402)", "faculty": "Prof. Rao", "room": "LH-101"},
                    {"time": "10:00 - 11:00 AM", "subject": "Design & Analysis of Algorithms (CS401)", "faculty": "Dr. Sharma", "room": "LH-101"},
                    {"time": "11:15 - 12:15 PM", "subject": "Database Management Systems (CS404)", "faculty": "Dr. Anita Nair", "room": "LH-101"},
                    {"time": "01:00 - 03:00 PM", "subject": "Web Development Workshop (CS405P)", "faculty": "Prof. Ghosh", "room": "Web Tech Lab"},
                    {"time": "03:15 - 04:30 PM", "subject": "Sports / Club Activities", "faculty": "Student Council", "room": "Sports Arena"}
                ],
                "Friday": [
                    {"time": "09:00 - 10:00 AM", "subject": "Discrete Mathematics (MA401)", "faculty": "Dr. Meena", "room": "LH-101"},
                    {"time": "10:00 - 11:00 AM", "subject": "Computer Organization & Architecture (CS403)", "faculty": "Prof. Verma", "room": "LH-101"},
                    {"time": "11:15 - 12:15 PM", "subject": "Design & Analysis of Algorithms (CS401)", "faculty": "Dr. Sharma", "room": "LH-101"},
                    {"time": "01:00 - 03:00 PM", "subject": "Mini-Project Evaluation", "faculty": "Project Committee", "room": "Project Lab 1"},
                    {"time": "03:15 - 04:15 PM", "subject": "Remedial / Doubt Clearing Session", "faculty": "Course Instructors", "room": "LH-101"}
                ]
            },
            "Sem 6": {
                "Monday": [
                    {"time": "09:00 - 10:00 AM", "subject": "Machine Learning (CS601)", "faculty": "Dr. K. Patel", "room": "LH-203"},
                    {"time": "10:00 - 11:00 AM", "subject": "Compiler Design (CS602)", "faculty": "Dr. V. Joshi", "room": "LH-203"},
                    {"time": "11:15 - 01:15 PM", "subject": "Machine Learning Lab (CS601P)", "faculty": "Dr. K. Patel", "room": "AI/ML Lab, 3rd Floor"},
                    {"time": "02:00 - 03:00 PM", "subject": "Computer Networks (CS603)", "faculty": "Prof. S. Sen", "room": "LH-203"}
                ],
                "Tuesday": [
                    {"time": "09:00 - 10:00 AM", "subject": "Computer Networks (CS603)", "faculty": "Prof. S. Sen", "room": "LH-203"},
                    {"time": "10:00 - 11:00 AM", "subject": "Cloud Computing Elective (CS604E)", "faculty": "Prof. Gupta", "room": "LH-203"},
                    {"time": "11:15 - 01:15 PM", "subject": "Networking & Socket Lab (CS603P)", "faculty": "Prof. S. Sen", "room": "Networks Lab"},
                    {"time": "02:00 - 03:00 PM", "subject": "Compiler Design (CS602)", "faculty": "Dr. V. Joshi", "room": "LH-203"}
                ],
                "Wednesday": [
                    {"time": "09:00 - 10:00 AM", "subject": "Machine Learning (CS601)", "faculty": "Dr. K. Patel", "room": "LH-203"},
                    {"time": "10:00 - 11:00 AM", "subject": "Compiler Design (CS602)", "faculty": "Dr. V. Joshi", "room": "LH-203"},
                    {"time": "11:15 - 12:15 PM", "subject": "Cloud Computing Elective (CS604E)", "faculty": "Prof. Gupta", "room": "LH-203"},
                    {"time": "01:00 - 04:00 PM", "subject": "Major Project Phase-I", "faculty": "Guide Allocation", "room": "Innovation Center"}
                ],
                "Thursday": [
                    {"time": "09:00 - 10:00 AM", "subject": "Computer Networks (CS603)", "faculty": "Prof. S. Sen", "room": "LH-203"},
                    {"time": "10:00 - 11:00 AM", "subject": "Machine Learning (CS601)", "faculty": "Dr. K. Patel", "room": "LH-203"},
                    {"time": "11:15 - 01:15 PM", "subject": "Compiler Design Tools Lab (CS602P)", "faculty": "Dr. V. Joshi", "room": "Lab 4"},
                    {"time": "02:00 - 03:00 PM", "subject": "Open Elective (Management/Economics)", "faculty": "Visiting Faculty", "room": "Management Block LH-2"}
                ],
                "Friday": [
                    {"time": "09:00 - 11:00 AM", "subject": "Cybersecurity & Cryptography (CS605E)", "faculty": "Prof. T. Reddy", "room": "LH-203"},
                    {"time": "11:15 - 12:15 PM", "subject": "Industry Seminar / Tech Talk", "faculty": "T&P Cell", "room": "Main Auditorium"},
                    {"time": "01:00 - 04:00 PM", "subject": "Competitive Programming & Placement Prep", "faculty": "Coding Club", "room": "Lab 1"}
                ]
            }
        },
        "ECE": {
            "Sem 4": {
                "Monday": [
                    {"time": "09:00 - 10:00 AM", "subject": "Analog Circuits (EC401)", "faculty": "Dr. R. Mishra", "room": "EC-LH-1"},
                    {"time": "10:00 - 11:00 AM", "subject": "Signals & Systems (EC402)", "faculty": "Prof. D. Roy", "room": "EC-LH-1"},
                    {"time": "11:15 - 01:15 PM", "subject": "Analog Circuits Lab (EC401P)", "faculty": "Dr. R. Mishra", "room": "Analog Electronics Lab"}
                ]
            }
        }
    },
    "courses": [
        {
            "code": "CS201",
            "title": "Data Structures & Algorithms in C/C++",
            "credits": 4,
            "department": "CSE",
            "semester": 3,
            "prerequisites": ["CS101 (Intro to Programming / C Programming)"],
            "corequisites": ["CS201P (Data Structures Lab)"],
            "description": "Fundamental data structures (Arrays, Linked Lists, Stacks, Queues, Trees, Graphs, Hash Tables) and basic complexity analysis.",
            "recommended_books": ["Data Structures using C by Tanenbaum", "Introduction to Algorithms (CLRS)"]
        },
        {
            "code": "CS401",
            "title": "Design & Analysis of Algorithms",
            "credits": 4,
            "department": "CSE",
            "semester": 4,
            "prerequisites": ["CS201 (Data Structures)", "MA201 (Discrete Mathematics)"],
            "corequisites": ["CS401P (Algorithms Lab)"],
            "description": "Asymptotic notation, Divide & Conquer, Greedy method, Dynamic Programming, Backtracking, Branch & Bound, NP-Completeness.",
            "recommended_books": ["Introduction to Algorithms by Cormen, Leiserson, Rivest, Stein (CLRS)"]
        },
        {
            "code": "CS402",
            "title": "Operating Systems",
            "credits": 4,
            "department": "CSE",
            "semester": 4,
            "prerequisites": ["CS201 (Data Structures)", "CS302 (Computer Organization)"],
            "corequisites": ["CS402P (OS Lab with Linux/Bash)"],
            "description": "Process management, CPU scheduling, threads, concurrency, deadlocks, memory management (paging/segmentation), virtual memory, file systems.",
            "recommended_books": ["Operating System Concepts by Silberschatz, Galvin & Gagne"]
        },
        {
            "code": "CS404",
            "title": "Database Management Systems",
            "credits": 4,
            "department": "CSE",
            "semester": 4,
            "prerequisites": ["CS201 (Data Structures)"],
            "corequisites": ["CS404P (SQL & Relational DB Lab)"],
            "description": "Entity-Relationship model, Relational Algebra, SQL queries, Normalization (1NF to BCNF), Transaction processing, Concurrency control, ACID properties.",
            "recommended_books": ["Database System Concepts by Korth, Silberschatz & Sudarshan"]
        },
        {
            "code": "CS601",
            "title": "Machine Learning",
            "credits": 4,
            "department": "CSE",
            "semester": 6,
            "prerequisites": [
                "MA301 (Linear Algebra & Probability Statistics)",
                "CS401 (Design & Analysis of Algorithms)",
                "Proficiency in Python Programming"
            ],
            "corequisites": ["CS601P (ML Lab with Scikit-Learn & PyTorch)"],
            "description": "Supervised learning (Linear/Logistic Regression, SVMs, Decision Trees, Random Forests), Unsupervised learning (K-Means, PCA), Neural Networks basics, model evaluation.",
            "recommended_books": ["Pattern Recognition and Machine Learning by Christopher Bishop", "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow"]
        },
        {
            "code": "CS602",
            "title": "Compiler Design",
            "credits": 4,
            "department": "CSE",
            "semester": 6,
            "prerequisites": ["CS301 (Theory of Computation / Automata)", "CS201 (Data Structures)"],
            "corequisites": ["CS602P (Lex & Yacc Compiler Lab)"],
            "description": "Phases of a compiler, Lexical Analysis, Syntax Analysis (LL/LR parsers), Syntax-Directed Translation, Intermediate Code Generation, Code Optimization.",
            "recommended_books": ["Compilers: Principles, Techniques, and Tools (Dragon Book) by Aho, Lam, Sethi, Ullman"]
        },
        {
            "code": "CS603",
            "title": "Computer Networks",
            "credits": 4,
            "department": "CSE",
            "semester": 6,
            "prerequisites": ["CS402 (Operating Systems)"],
            "corequisites": ["CS603P (Network Simulation & Wireshark Lab)"],
            "description": "OSI and TCP/IP protocol suites, Physical layer, Data link protocols, Network routing (Dijkstra, Bellman-Ford), Transport layer (TCP/UDP flow and congestion control), Application protocols (HTTP, DNS).",
            "recommended_books": ["Computer Networking: A Top-Down Approach by Kurose & Ross"]
        },
        {
            "code": "CS604E",
            "title": "Cloud Computing & DevOps (Professional Elective)",
            "credits": 3,
            "department": "CSE",
            "semester": 6,
            "prerequisites": ["CS402 (Operating Systems)", "CS603 (Computer Networks)"],
            "corequisites": [],
            "description": "Virtualization, Docker containers, Kubernetes orchestration, AWS/GCP cloud architectures, CI/CD pipelines, Serverless computing.",
            "recommended_books": ["Cloud Computing: Concepts, Technology & Architecture by Thomas Erl"]
        }
    ],
    "exam_notices": [
        {
            "id": "EXAM-2026-01",
            "title": "Mid-Semester Examination Schedule - Even Sem 2026",
            "date_issued": "2026-03-10",
            "applicable_to": "B.Tech Sem 4 & Sem 6 (All Branches)",
            "exam_window": "April 06, 2026 to April 15, 2026",
            "sessions": {
                "Morning": "10:00 AM - 12:00 PM",
                "Afternoon": "02:00 PM - 04:00 PM"
            },
            "schedule_highlights": [
                {"date": "April 06, 2026", "subject": "Design & Analysis of Algorithms (CS401) / Machine Learning (CS601)", "time": "10:00 AM - 12:00 PM"},
                {"date": "April 08, 2026", "subject": "Operating Systems (CS402) / Compiler Design (CS602)", "time": "10:00 AM - 12:00 PM"},
                {"date": "April 10, 2026", "subject": "Database Management Systems (CS404) / Computer Networks (CS603)", "time": "10:00 AM - 12:00 PM"},
                {"date": "April 13, 2026", "subject": "Discrete Mathematics (MA401) / Cloud Computing (CS604E)", "time": "10:00 AM - 12:00 PM"}
            ],
            "guidelines": [
                "Students must carry their Physical College ID Card & Hall Ticket. Digital softcopies on phones are strictly prohibited.",
                "Reporting time: 20 minutes prior to exam commencement. Entry closed after 15 minutes of exam start.",
                "Non-programmable scientific calculators (Fx-991MS / Fx-82MS) are permitted only for Mathematics & Electronics papers.",
                "Smartwatches, mobile phones, and notes inside the hall lead to immediate debarment under Examination Malpractice Rules."
            ]
        },
        {
            "id": "EXAM-2026-02",
            "title": "Practical Lab Examinations & Viva Voce Notification",
            "date_issued": "2026-03-14",
            "applicable_to": "All Lab Courses (Sem 4 & 6)",
            "exam_window": "May 02, 2026 to May 08, 2026",
            "guidelines": [
                "Completed and verified lab records signed by faculty-in-charge are mandatory for appearing in the lab viva.",
                "Internal weightage: 60 marks (Continuous evaluation + Record book), External viva & coding task: 40 marks."
            ]
        },
        {
            "id": "EXAM-2026-03",
            "title": "Supplementary / Backlog Exam Registration Deadline",
            "date_issued": "2026-03-01",
            "deadline": "March 28, 2026 (5:00 PM)",
            "fee": "INR 500 per subject",
            "portal": "https://erp.campus.edu/backlog-reg"
        }
    ],
    "administrative_queries": [
        {
            "category": "Fee Payment & Installments",
            "details": "Even semester tuition fee deadline without late fee is January 20th. With late fee of Rs. 100/day up to February 10th. Installment requests must be submitted to the Finance Office (Room A-104) with an application endorsed by the student's guardian and HOD.",
            "contact": "Finance Desk: finance@campus.edu | Ext: 104"
        },
        {
            "category": "Scholarships & Financial Aid",
            "details": "Applications for Merit-cum-Means (MCM), National Scholarship Portal (NSP), and State Post-Matric Scholarships are handled at Student Welfare Section (Admin Block, 1st Floor). Required documents: Income Certificate (< 2.5 LPA for fee waiver), Marksheets of previous 2 semesters (min 7.5 CGPA), Caste certificate (if applicable), and Aadhaar-seeded Bank passbook.",
            "contact": "Scholarship Incharge: scholarships@campus.edu | Admin Block Room 108"
        },
        {
            "category": "Library Timings & Policies",
            "details": "Central Library is open from 08:30 AM to 09:00 PM on weekdays, and 10:00 AM to 05:00 PM on weekends. During exam season, study halls remain open 24/7. B.Tech students can borrow up to 4 books for a 14-day duration. Overdue fine is Rs. 5 per day per book. Digital repository and IEEE Xplore access can be accessed on campus LAN or via OpenAthens credentials.",
            "contact": "Chief Librarian: library@campus.edu | Ext: 301"
        },
        {
            "category": "Hostel & Mess Regulations",
            "details": "Hostel in-time for all students is strictly 09:30 PM. Night-out or weekend leave pass must be requested 24 hours in advance via the Campus ERP app with parent SMS/email consent verification. Mess menu changes are decided on the 1st of every month by the Student Mess Committee.",
            "contact": "Chief Warden Office: hostel@campus.edu | Warden Office Block B"
        },
        {
            "category": "Bonafide Certificate & Transcripts",
            "details": "Bonafide certificates for passport, bank loan, bus pass, or visa can be requested directly through the Student ERP portal under 'Services -> Certificates'. Digital signed PDF is delivered within 24 working hours. Official sealed transcripts require 5 working days and a fee of Rs. 200 per set at Academic Section (Counter 3).",
            "contact": "Academic Section: academic.records@campus.edu | Counter 3, Main Building"
        },
        {
            "category": "Attendance & Medical Leave Policy",
            "details": "A minimum of 75% attendance is mandatory in each registered theory and laboratory course to be eligible for End-Semester Examinations. Relaxation up to 10% (i.e., minimum 65%) is granted on medical grounds or official institute duty, provided an approved Medical Certificate and Leave Application is submitted to the HOD within 3 working days of resumption of classes.",
            "contact": "Dean Academic Affairs: dean.academics@campus.edu"
        },
        {
            "category": "Grievance, Anti-Ragging & Student Counseling",
            "details": "Zero-tolerance anti-ragging campus. Anti-Ragging Toll-Free Helpline: 1800-180-5522. Campus Internal Complaint Committee (ICC) & Women's Cell: Room Admin-202. Confidential student mental health counselor is available Mon-Fri 02:00 PM - 05:00 PM in Health Center Room 4.",
            "contact": "Counseling Cell: counseling@campus.edu | Anti-ragging: 9876543210"
        }
    ]
}

def get_campus_system_prompt() -> str:
    """Returns a rich, grounded system prompt injecting all campus data for Gemini."""
    import json
    campus_context = json.dumps(CAMPUS_DATA, indent=2)
    return f"""You are the official Campus AI Assistant for Apex Institute of Technology & Engineering.
You are a student-centric conversational assistant designed to navigate:
1. Academic timetables (schedules, labs, room allocations, faculty)
2. Exam notices & circulars (midterms, finals, hall-ticket rules, calculator guidelines)
3. Course prerequisites & curriculum (credits, prerequisite dependencies, syllabus, recommended books)
4. Administrative queries (fees, scholarships, library timings, hostel rules, bonafide certificates, attendance rules)
5. Drafting academic communications (leave letters, permission letters, formal emails to professors/deans, etc.)

GROUND TRUTH CAMPUS KNOWLEDGE BASE:
```json
{campus_context}
```

INSTRUCTIONS & PERSONALITY:
- Be encouraging, accurate, student-friendly, and concise.
- When answering timetable, exam, or course queries, refer directly to the verified ground truth data above.
- If a student asks for prerequisites, clearly state which prior courses must be passed, recommended prerequisites, and why.
- If a student asks about administrative matters (scholarships, fees, library, bonafide certificates), provide exact office locations, deadlines, contacts, and required documents.
- Use markdown formatting with bullet points, bold tags, and tables where appropriate to make information effortless to read on a mobile or laptop screen.
- If a student asks you to draft an email or letter, write a polished, professional draft ready to send, including Subject line, salutation, body, and student placeholder fields.
"""

def search_offline_knowledge(query: str) -> str:
    """
    Intelligent local retrieval fallback when Gemini API key is missing or offline.
    Matches queries against the structured campus database.
    """
    q = query.lower()
    
    # 1. Timetables
    if any(k in q for k in ["timetable", "schedule", "class", "lecture", "timing", "lab", "tomorrow", "today", "monday", "tuesday", "wednesday", "thursday", "friday"]):
        for dept in ["CSE", "ECE"]:
            if dept.lower() in q or dept == "CSE":
                sem = "Sem 6" if "6" in q or "sixth" in q else "Sem 4"
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                matched_day = None
                for d in days:
                    if d.lower() in q:
                        matched_day = d
                        break
                
                tt = CAMPUS_DATA["timetables"].get(dept, {}).get(sem, {})
                if matched_day and matched_day in tt:
                    slots = tt[matched_day]
                    res = f"### 📅 {dept} {sem} - {matched_day} Timetable\n\n"
                    res += "| Time | Subject | Faculty | Room |\n|---|---|---|---|\n"
                    for s in slots:
                        res += f"| {s['time']} | **{s['subject']}** | {s['faculty']} | `{s['room']}` |\n"
                    return res
                else:
                    res = f"### 📅 {dept} {sem} Full Weekly Timetable\n\n"
                    for day, slots in tt.items():
                        res += f"#### **{day}**\n"
                        for s in slots:
                            res += f"- **{s['time']}**: {s['subject']} ({s['faculty']}) - `{s['room']}`\n"
                        res += "\n"
                    return res

    # 2. Prerequisites & Courses
    if any(k in q for k in ["prerequisite", "prereq", "course", "credit", "syllabus", "subject", "algorithm", "operating system", "machine learning", "compiler", "network"]):
        matches = []
        for c in CAMPUS_DATA["courses"]:
            if (c["code"].lower() in q) or any(word in c["title"].lower() for word in q.split() if len(word) > 3):
                matches.append(c)
        if not matches:
            matches = CAMPUS_DATA["courses"][:3]
        
        res = "### 🎓 Course Prerequisites & Curriculum Details\n\n"
        for c in matches:
            res += f"#### **{c['code']}: {c['title']}** ({c['credits']} Credits - Sem {c['semester']})\n"
            prereqs = ", ".join(c["prerequisites"]) if c["prerequisites"] else "None (Open to all)"
            res += f"- **Prerequisites Required**: `{prereqs}`\n"
            res += f"- **Description**: {c['description']}\n"
            res += f"- **Recommended Books**: {', '.join(c['recommended_books'])}\n\n"
        return res

    # 3. Exams
    if any(k in q for k in ["exam", "midterm", "test", "hall ticket", "calculator", "marks", "grading", "backlog", "supplementary"]):
        res = "### 📢 Upcoming Exam Notices & Guidelines\n\n"
        for e in CAMPUS_DATA["exam_notices"]:
            res += f"#### 📝 {e['title']}\n"
            if "exam_window" in e:
                res += f"- **Exam Window**: {e['exam_window']}\n"
            if "deadline" in e:
                res += f"- **Deadline**: {e['deadline']} (Fee: {e['fee']})\n"
            if "guidelines" in e:
                res += "- **Key Guidelines**:\n"
                for g in e["guidelines"]:
                    res += f"  - {g}\n"
            res += "\n"
        return res

    # 4. Administrative Queries (fees, scholarships, library, hostel, bonafide)
    for admin in CAMPUS_DATA["administrative_queries"]:
        cat_words = admin["category"].lower().split()
        if any(w in q for w in cat_words if len(w) > 3) or any(k in q for k in ["fee", "scholarship", "library", "hostel", "bonafide", "attendance", "ragging", "complaint"]):
            res = f"### 🏢 Administrative Information: {admin['category']}\n\n"
            res += f"{admin['details']}\n\n"
            res += f"📍 **Contact / Location**: `{admin['contact']}`"
            return res

    # Fallback general response
    return (
        "### 🎓 Campus AI Assistant\n\n"
        "I am ready to help you navigate campus life! Here is what you can ask me:\n\n"
        "- 📅 **Academic Timetables**: *'Show me CSE 4th semester timetable for Tuesday'* or *'Where is Algorithms Lab?'*\n"
        "- 📚 **Course Prerequisites**: *'What are the prerequisites for Machine Learning (CS601)?'*\n"
        "- 📝 **Exam Notices**: *'When are the Mid-Sem exams and what are the calculator rules?'*\n"
        "- 🏢 **Administrative Queries**: *'How do I apply for a scholarship or bonafide certificate?'* or *'What are the library hours?'*\n"
        "- ✍️ **Drafting Academic Letters**: *'Draft a leave letter for 2 days medical leave'* or *'Write an email requesting attendance waiver'*"
    )
