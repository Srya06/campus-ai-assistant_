import logging
from backend.app.db.session import engine, SessionLocal, Base
from backend.app.models.entities import (
    Institution, Department, Semester, Course, CoursePrerequisite,
    Faculty, Classroom, TimetableEntry, ExamNotice, AdministrativeFAQ,
    CampusContact, Role, User, CourseNote
)
from backend.app.core.security import get_password_hash

logger = logging.getLogger("campus_seed")

def init_db():
    """Create all tables and seed realistic sample data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(Institution).first():
            logger.info("Database already initialized with campus records.")
            return

        logger.info("Seeding initial institutional campus records...")

        # 1. Roles
        admin_role = Role(name="admin", description="Full administrative campus management")
        faculty_role = Role(name="faculty", description="Academic faculty advisor")
        student_role = Role(name="student", description="Undergraduate/Graduate student")
        db.add_all([admin_role, faculty_role, student_role])
        db.flush()

        # 2. Users
        admin_user = User(
            username="admin",
            email="admin@campus.edu",
            hashed_password=get_password_hash("admin123"),
            full_name="Campus Academic Registrar",
            role_id=admin_role.id,
            roll_number="",
            department="Academic Administration",
            semester="Faculty / Admin",
            cgpa="N/A",
            resume_url="",
            skills="Institutional Governance, Accreditation, Curriculum Oversight",
            phone="Ext 101"
        )
        student_user = User(
            username="student",
            email="student@campus.edu",
            hashed_password=get_password_hash("student123"),
            full_name="Aarav Sharma",
            role_id=student_role.id,
            roll_number="22CS042",
            department="CSE",
            semester="Sem 4",
            cgpa="8.4",
            resume_url="https://drive.google.com/file/d/1_aarav_sharma_academic_resume/view",
            skills="C++, Data Structures, Linux, Algorithms, System Programming",
            phone="+91 98123 45678"
        )
        surya_user = User(
            username="surya",
            email="surya@campus.edu",
            hashed_password=get_password_hash("surya123"),
            full_name="Surya D.",
            role_id=student_role.id,
            roll_number="22AI104",
            department="CSE (AI)",
            semester="Sem 5 (CSE - AI)",
            cgpa="8.0",
            resume_url="https://drive.google.com/file/d/1_surya_academic_resume_2026/view",
            skills="Python, Machine Learning, Deep Learning, FastAPI, PostgreSQL, React, Docker",
            phone="+91 98765 43210"
        )
        db.add_all([admin_user, student_user, surya_user])

        # 3. Institution
        inst = Institution(
            name="Apex Institute of Technology & Engineering",
            code="AITE",
            academic_year="2025-2026",
            current_semester="Spring (Even) Semester"
        )
        db.add(inst)
        db.flush()

        # 4. Departments
        cse = Department(institution_id=inst.id, name="Computer Science & Engineering", code="CSE")
        ece = Department(institution_id=inst.id, name="Electronics & Communication Engineering", code="ECE")
        db.add_all([cse, ece])
        db.flush()

        # 5. Semesters
        sem4 = Semester(number=4, term="Spring")
        sem6 = Semester(number=6, term="Spring")
        db.add_all([sem4, sem6])
        db.flush()

        # 6. Faculty
        f_sharma = Faculty(department_id=cse.id, name="Dr. Sharma", designation="Associate Professor", email="sharma@campus.edu", cabin_location="CS Block 204")
        f_rao = Faculty(department_id=cse.id, name="Prof. Rao", designation="Assistant Professor", email="rao@campus.edu", cabin_location="CS Block 208")
        f_nair = Faculty(department_id=cse.id, name="Dr. Anita Nair", designation="Professor & HOD", email="anita.nair@campus.edu", cabin_location="CS Block 101")
        f_patel = Faculty(department_id=cse.id, name="Dr. K. Patel", designation="Associate Professor (AI Lab)", email="k.patel@campus.edu", cabin_location="AI Lab Cabin")
        f_joshi = Faculty(department_id=cse.id, name="Dr. V. Joshi", designation="Assistant Professor", email="v.joshi@campus.edu", cabin_location="CS Block 305")
        f_sen = Faculty(department_id=cse.id, name="Prof. S. Sen", designation="Assistant Professor", email="s.sen@campus.edu", cabin_location="Networks Lab")
        f_mishra = Faculty(department_id=ece.id, name="Dr. R. Mishra", designation="Associate Professor", email="r.mishra@campus.edu", cabin_location="ECE Block 102")
        db.add_all([f_sharma, f_rao, f_nair, f_patel, f_joshi, f_sen, f_mishra])
        db.flush()

        # 7. Classrooms & Labs
        c_lh101 = Classroom(institution_id=inst.id, room_number="LH-101", building="Academic Block A", capacity=80, is_lab=False)
        c_lh203 = Classroom(institution_id=inst.id, room_number="LH-203", building="Academic Block A", capacity=80, is_lab=False)
        c_lab3 = Classroom(institution_id=inst.id, room_number="Lab 3, CS Block", building="Computing Block", capacity=40, is_lab=True)
        c_dblab = Classroom(institution_id=inst.id, room_number="Database Lab", building="Computing Block", capacity=40, is_lab=True)
        c_ailab = Classroom(institution_id=inst.id, room_number="AI/ML Lab", building="Computing Block", capacity=40, is_lab=True)
        c_netlab = Classroom(institution_id=inst.id, room_number="Networks Lab", building="Computing Block", capacity=40, is_lab=True)
        db.add_all([c_lh101, c_lh203, c_lab3, c_dblab, c_ailab, c_netlab])
        db.flush()

        # 8. Courses
        c_cs101 = Course(department_id=cse.id, code="CS101", title="Intro to Computer Programming in C", credits=4, semester_number=1, description="Foundations of C programming, pointers, memory.")
        c_ma201 = Course(department_id=cse.id, code="MA201", title="Discrete Mathematics", credits=4, semester_number=3, description="Set theory, logic, graph theory, combinatorics.")
        c_cs201 = Course(department_id=cse.id, code="CS201", title="Data Structures & Algorithms", credits=4, semester_number=3, description="Arrays, stacks, queues, trees, graphs, sorting, searching.", prerequisites_text="CS101")
        
        c_cs401 = Course(department_id=cse.id, code="CS401", title="Design & Analysis of Algorithms", credits=4, semester_number=4, description="Divide & Conquer, Greedy, Dynamic Programming, NP-completeness.", prerequisites_text="CS201, MA201", recommended_books="Introduction to Algorithms (CLRS)")
        c_cs402 = Course(department_id=cse.id, code="CS402", title="Operating Systems", credits=4, semester_number=4, description="Process scheduling, memory management, virtual memory, concurrency, deadlocks.", prerequisites_text="CS201", recommended_books="Operating System Concepts by Silberschatz")
        c_cs403 = Course(department_id=cse.id, code="CS403", title="Computer Organization & Architecture", credits=4, semester_number=4, description="CPU architecture, pipelining, cache memory, instruction sets.")
        c_cs404 = Course(department_id=cse.id, code="CS404", title="Database Management Systems", credits=4, semester_number=4, description="ER modeling, Relational Algebra, SQL, Normalization, ACID transactions.", prerequisites_text="CS201", recommended_books="Database System Concepts by Korth")
        
        c_ma301 = Course(department_id=cse.id, code="MA301", title="Linear Algebra & Probability", credits=4, semester_number=5, description="Matrix theory, eigenvalues, probability distributions, hypothesis testing.")
        c_cs601 = Course(department_id=cse.id, code="CS601", title="Machine Learning", credits=4, semester_number=6, description="Supervised learning, regression, SVMs, decision trees, unsupervised clustering, neural nets.", prerequisites_text="MA301, CS401", recommended_books="Pattern Recognition & Machine Learning by Christopher Bishop")
        c_cs602 = Course(department_id=cse.id, code="CS602", title="Compiler Design", credits=4, semester_number=6, description="Lexical analysis, parsing (LL/LR), syntax-directed translation, code optimization.", prerequisites_text="CS201", recommended_books="Compilers: Principles, Techniques, & Tools (Dragon Book)")
        c_cs603 = Course(department_id=cse.id, code="CS603", title="Computer Networks", credits=4, semester_number=6, description="OSI model, TCP/IP, routing algorithms, transport protocols, socket programming.", prerequisites_text="CS402", recommended_books="Computer Networking: A Top-Down Approach by Kurose & Ross")
        c_cs604e = Course(department_id=cse.id, code="CS604E", title="Cloud Computing & DevOps", credits=3, semester_number=6, course_type="Professional Elective", description="Containers, Docker, Kubernetes, AWS architectures, CI/CD pipelines.", prerequisites_text="CS402, CS603")
        
        c_ec401 = Course(department_id=ece.id, code="EC401", title="Analog Electronic Circuits", credits=4, semester_number=4, description="BJT/FET amplifiers, frequency response, feedback amplifiers, op-amps.", recommended_books="Microelectronic Circuits by Sedra & Smith")
        c_ec402 = Course(department_id=ece.id, code="EC402", title="Signals & Systems", credits=4, semester_number=4, description="Continuous and discrete time signals, LTI systems, Fourier analysis, Laplace and Z-transforms.", recommended_books="Signals and Systems by Oppenheim & Willsky")
        c_ec403 = Course(department_id=ece.id, code="EC403", title="Electromagnetic Field Theory", credits=4, semester_number=4, description="Electrostatics, magnetostatics, Maxwell's equations, plane wave propagation, transmission lines.", recommended_books="Elements of Electromagnetics by Sadiku")
        c_ec404 = Course(department_id=ece.id, code="EC404", title="Microprocessors & Microcontrollers", credits=4, semester_number=4, description="8086 architecture, assembly language, memory interfacing, peripheral ICs, timers.", recommended_books="Microprocessor Architecture by Gaonkar")

        db.add_all([c_cs101, c_ma201, c_cs201, c_cs401, c_cs402, c_cs403, c_cs404, c_ma301, c_cs601, c_cs602, c_cs603, c_cs604e, c_ec401, c_ec402, c_ec403, c_ec404])
        db.flush()

        # 9. Prerequisites relationships
        p1 = CoursePrerequisite(course_id=c_cs401.id, prerequisite_course_id=c_cs201.id, is_strict=True)
        p2 = CoursePrerequisite(course_id=c_cs401.id, prerequisite_course_id=c_ma201.id, is_strict=True)
        p3 = CoursePrerequisite(course_id=c_cs601.id, prerequisite_course_id=c_cs401.id, is_strict=True)
        p4 = CoursePrerequisite(course_id=c_cs601.id, prerequisite_course_id=c_ma301.id, is_strict=True)
        p5 = CoursePrerequisite(course_id=c_cs602.id, prerequisite_course_id=c_cs201.id, is_strict=True)
        p6 = CoursePrerequisite(course_id=c_cs603.id, prerequisite_course_id=c_cs402.id, is_strict=True)
        p7 = CoursePrerequisite(course_id=c_ec402.id, prerequisite_course_id=c_ec401.id, is_strict=False)
        p8 = CoursePrerequisite(course_id=c_ec404.id, prerequisite_course_id=c_cs101.id, is_strict=True)
        db.add_all([p1, p2, p3, p4, p5, p6, p7, p8])

        # 10. Timetable Entries (CSE Sem 4)
        tt_data = [
            ("Monday", "09:00 - 10:00 AM", c_cs401.id, f_sharma.name, "LH-101", False),
            ("Monday", "10:00 - 11:00 AM", c_cs402.id, f_rao.name, "LH-101", False),
            ("Monday", "11:15 - 01:15 PM", c_cs401.id, "Dr. Sharma & TA", "Lab 3, CS Block", True),
            ("Monday", "02:00 - 03:00 PM", c_cs403.id, "Prof. Verma", "LH-101", False),
            
            ("Tuesday", "09:00 - 10:00 AM", c_cs404.id, f_nair.name, "LH-101", False),
            ("Tuesday", "10:00 - 11:00 AM", c_cs401.id, f_sharma.name, "LH-101", False),
            ("Tuesday", "11:15 - 12:15 PM", c_cs402.id, f_rao.name, "LH-101", False),
            ("Tuesday", "01:00 - 03:00 PM", c_cs404.id, f_nair.name, "Database Lab", True),
            
            ("Wednesday", "09:00 - 10:00 AM", c_cs403.id, "Prof. Verma", "LH-101", False),
            ("Wednesday", "10:00 - 11:00 AM", c_cs404.id, f_nair.name, "LH-101", False),
            ("Wednesday", "11:15 - 01:15 PM", c_cs402.id, f_rao.name, "Systems Lab", True),
            ("Wednesday", "02:00 - 03:00 PM", c_ma201.id, "Dr. Meena", "LH-101", False),
            
            ("Thursday", "09:00 - 10:00 AM", c_cs402.id, f_rao.name, "LH-101", False),
            ("Thursday", "10:00 - 11:00 AM", c_cs401.id, f_sharma.name, "LH-101", False),
            ("Thursday", "11:15 - 12:15 PM", c_cs404.id, f_nair.name, "LH-101", False),
            ("Thursday", "01:00 - 03:00 PM", c_cs401.id, "Prof. Ghosh", "Web Tech Lab", True),
            
            ("Friday", "09:00 - 10:00 AM", c_ma201.id, "Dr. Meena", "LH-101", False),
            ("Friday", "10:00 - 11:00 AM", c_cs403.id, "Prof. Verma", "LH-101", False),
            ("Friday", "11:15 - 12:15 PM", c_cs401.id, f_sharma.name, "LH-101", False),
            ("Friday", "01:00 - 03:00 PM", c_cs401.id, "Project Committee", "Project Lab 1", True)
        ]

        for day, slot, cid, fac, room, lab in tt_data:
            db.add(TimetableEntry(
                department_id=cse.id,
                semester_label="Sem 4",
                course_id=cid,
                faculty_name=fac,
                room_number=room,
                day_of_week=day,
                time_slot=slot,
                is_lab=lab
            ))

        # 10.1 Timetable Entries (ECE Sem 4)
        ece_tt_data = [
            ("Monday", "09:00 - 10:00 AM", c_ec401.id, "Dr. R. Mishra", "EC-101", False),
            ("Monday", "10:00 - 11:00 AM", c_ec402.id, "Prof. K. Verma", "EC-101", False),
            ("Monday", "11:15 - 01:15 PM", c_ec401.id, "Dr. R. Mishra & TA", "Analog Lab", True),
            ("Monday", "02:00 - 03:00 PM", c_ec403.id, "Prof. Sen", "EC-101", False),

            ("Tuesday", "09:00 - 10:00 AM", c_ec402.id, "Prof. K. Verma", "EC-101", False),
            ("Tuesday", "10:00 - 11:00 AM", c_ec401.id, "Dr. R. Mishra", "EC-101", False),
            ("Tuesday", "11:15 - 12:15 PM", c_ec404.id, "Dr. T. Das", "EC-101", False),
            ("Tuesday", "01:00 - 03:00 PM", c_ec404.id, "Dr. T. Das & TA", "Microcontroller Lab", True),

            ("Wednesday", "09:00 - 10:00 AM", c_ec403.id, "Prof. Sen", "EC-101", False),
            ("Wednesday", "10:00 - 11:00 AM", c_ec404.id, "Dr. T. Das", "EC-101", False),
            ("Wednesday", "11:15 - 01:15 PM", c_ec402.id, "Prof. K. Verma", "DSP Simulation Lab", True),
            ("Wednesday", "02:00 - 03:00 PM", c_ec401.id, "Dr. R. Mishra", "EC-101", False),

            ("Thursday", "09:00 - 10:00 AM", c_ec401.id, "Dr. R. Mishra", "EC-101", False),
            ("Thursday", "10:00 - 11:00 AM", c_ec402.id, "Prof. K. Verma", "EC-101", False),
            ("Thursday", "11:15 - 12:15 PM", c_ec403.id, "Prof. Sen", "EC-101", False),
            ("Thursday", "01:00 - 03:00 PM", c_ec401.id, "Dr. R. Mishra", "Electronic Circuits Lab", True),

            ("Friday", "09:00 - 10:00 AM", c_ec404.id, "Dr. T. Das", "EC-101", False),
            ("Friday", "10:00 - 11:00 AM", c_ec403.id, "Prof. Sen", "EC-101", False),
            ("Friday", "11:15 - 12:15 PM", c_ec402.id, "Prof. K. Verma", "EC-101", False),
            ("Friday", "01:00 - 03:00 PM", c_ec404.id, "Dr. T. Das", "Embedded Systems Lab", True)
        ]

        for day, slot, cid, fac, room, lab in ece_tt_data:
            db.add(TimetableEntry(
                department_id=ece.id,
                semester_label="Sem 4",
                course_id=cid,
                faculty_name=fac,
                room_number=room,
                day_of_week=day,
                time_slot=slot,
                is_lab=lab
            ))

        # 11. Exam Notices
        ex1 = ExamNotice(
            notice_code="EXAM-2026-01",
            title="Mid-Semester Examination Schedule - Even Sem 2026",
            date_issued="2026-03-10",
            exam_type="Midterm",
            applicable_to="B.Tech Sem 4 & Sem 6 (All Branches)",
            exam_window="April 06, 2026 to April 15, 2026",
            calculator_policy="Non-programmable scientific calculators (Fx-991MS / Fx-82MS) permitted only for Mathematics & Electronics papers.",
            hall_ticket_guidelines="Physical College ID Card & Printed Hall Ticket mandatory. Digital copies on phones are strictly prohibited. Reporting time 20 min prior.",
            malpractice_rules="Smartwatches, phones, and paper chits lead to immediate debarment under Institute Malpractice Statutes.",
            is_urgent=True
        )
        ex2 = ExamNotice(
            notice_code="EXAM-2026-02",
            title="Practical Lab Examinations & Viva Voce Notification",
            date_issued="2026-03-14",
            exam_type="Practical",
            applicable_to="All Lab Courses (Sem 4 & 6)",
            exam_window="May 02, 2026 to May 08, 2026",
            calculator_policy="As per course instructor instructions.",
            hall_ticket_guidelines="Duly signed and verified lab observation notebook and record required.",
            is_urgent=False
        )
        ex3 = ExamNotice(
            notice_code="EXAM-2026-03",
            title="Supplementary / Backlog Examination Registration Deadline",
            date_issued="2026-03-01",
            exam_type="Backlog",
            applicable_to="All eligible backlog candidates",
            deadline="March 28, 2026 (5:00 PM)",
            hall_ticket_guidelines="Register online via ERP portal (Fee: Rs. 500 per subject).",
            is_urgent=True
        )
        db.add_all([ex1, ex2, ex3])

        # 12. Administrative FAQs
        faqs = [
            ("Fees & Installments", "How do I apply for tuition fee installments?", "Submit an application endorsed by your parent and HOD to the Finance Office (Room A-104) before January 20th. Late fee of Rs. 100/day applies after deadline.", "Finance Desk (Room A-104)", "finance@campus.edu", "Ext 104"),
            ("Scholarships", "How do I apply for Merit-cum-Means (MCM) or National Scholarship Portal (NSP)?", "Submit applications to Student Welfare Section (Admin Block, 1st Floor). Required: Income certificate (< 2.5 LPA), marksheets (min 7.5 CGPA), Caste certificate (if applicable), and Aadhaar-seeded Bank passbook.", "Student Welfare Section (Room 108)", "scholarships@campus.edu", "Ext 108"),
            ("Library", "What are the Central Library hours and overdue book fine rules?", "Library is open 08:30 AM - 09:00 PM on weekdays, and 10:00 AM - 05:00 PM on weekends. 24/7 during exam weeks. Students can borrow up to 4 books for 14 days. Overdue fine is Rs. 5 per day per book.", "Central Library Circulation Desk", "library@campus.edu", "Ext 301"),
            ("Hostel", "What are hostel in-times and night-out pass rules?", "In-time is strictly 09:30 PM. Night-out or weekend leave pass must be requested 24 hours prior via Campus ERP app with parent SMS/email verification.", "Chief Warden Office (Block B)", "hostel@campus.edu", "Ext 401"),
            ("Bonafide", "How do I get an official Bonafide Certificate or Transcript?", "Request bonafide certificate via Student ERP under 'Services -> Certificates' (digital PDF issued within 24 hours). Official sealed transcripts require 5 working days and fee of Rs. 200 per set at Academic Section Counter 3.", "Academic Section (Counter 3)", "academic.records@campus.edu", "Ext 202"),
            ("Attendance", "What is the mandatory attendance requirement?", "Minimum 75% attendance is required in each theory and lab course. Relaxation up to 10% (minimum 65%) allowed on medical grounds if certified leave application is submitted to HOD within 3 days of resuming classes.", "Dean Academic Affairs Office", "dean.academics@campus.edu", "Ext 102"),
            ("Grievance", "What is the contact for Anti-Ragging and Student Counseling?", "Zero-tolerance anti-ragging campus. National Helpline: 1800-180-5522. Campus Internal Complaint Committee (ICC): Room Admin-202. Student mental health counselor available Mon-Fri 2-5 PM.", "Counseling Cell (Health Center Room 4)", "counseling@campus.edu", "9876543210")
        ]

        for cat, q, a, loc, em, ph in faqs:
            db.add(AdministrativeFAQ(
                category=cat,
                question=q,
                answer=a,
                office_location=loc,
                contact_email=em,
                contact_phone=ph
            ))

        # 13. Course Notes & Study Material (Comprehensive Lecture Notes & PDFs)
        notes = [
            CourseNote(
                course_id=c_cs401.id,
                title="Foundations of Algorithm Analysis & Recurrences",
                unit_number=1,
                unit_title="Asymptotic Notations & Divide-and-Conquer",
                topic_description="Big-O, Omega, Theta notations, Master Theorem, Substitution Method, Recursion Tree analysis, Merge Sort and Quick Sort proofs.",
                content_markdown="""# Unit 1: Foundations of Algorithm Analysis

## 1. Asymptotic Notations
In algorithm design, asymptotic analysis describes runtime growth as input size n approaches infinity.
- **Big-O Notation (O)**: Asymptotic upper bound. f(n) = O(g(n)) if there exist positive constants c and n0 such that 0 <= f(n) <= c*g(n) for all n >= n0.
- **Big-Omega Notation (Ω)**: Asymptotic lower bound. f(n) = Ω(g(n)) if there exist positive constants c and n0 such that 0 <= c*g(n) <= f(n) for all n >= n0.
- **Big-Theta Notation (Θ)**: Asymptotically tight bound. Holds when f(n) is both O(g(n)) and Ω(g(n)).

### Master Theorem for Divide-and-Conquer Recurrences
Given recurrence of the form: T(n) = a*T(n/b) + f(n), where a >= 1 and b > 1:
- **Case 1**: If f(n) = O(n^(log_b(a) - epsilon)), then T(n) = Θ(n^(log_b(a))).
- **Case 2**: If f(n) = Θ(n^(log_b(a)) * log^k(n)), then T(n) = Θ(n^(log_b(a)) * log^(k+1)(n)).
- **Case 3**: If f(n) = Ω(n^(log_b(a) + epsilon)) and regularity condition holds, then T(n) = Θ(f(n)).

## 2. Divide and Conquer Paradigm
Divide problem into subproblems of same type, solve recursively, and combine subproblem solutions.
- **Merge Sort**: Divides array in half, recursively sorts each half, and merges sorted halves in O(n) time. Total time: Θ(n log n).
- **Quick Sort**: Selects pivot, partitions array around pivot such that smaller elements precede pivot. Worst case O(n^2), Average case Θ(n log n).""",
                faculty_author="Dr. Sharma",
                academic_year="2025-2026",
                download_count=42
            ),
            CourseNote(
                course_id=c_cs401.id,
                title="Dynamic Programming & Greedy Strategies",
                unit_number=2,
                unit_title="Dynamic Programming Framework",
                topic_description="Optimal Substructure, Overlapping Subproblems, Memoization vs Tabulation, 0/1 Knapsack, Longest Common Subsequence (LCS), Matrix Chain Multiplication.",
                content_markdown="""# Unit 2: Dynamic Programming & Greedy Strategies

## 1. Principles of Dynamic Programming (DP)
Dynamic Programming is an optimization strategy applicable when a problem exhibits:
1. **Optimal Substructure**: An optimal solution to the problem contains optimal solutions to subproblems.
2. **Overlapping Subproblems**: The recursive algorithm visits the same subproblems repeatedly rather than generating new ones.

### 0/1 Knapsack Problem
Given n items with weights w[1..n] and values v[1..n], maximize total value in knapsack of capacity W:
- **Recurrence**:
  - If w[i] > w: K(i, w) = K(i-1, w)
  - Else: K(i, w) = max(K(i-1, w), v[i] + K(i-1, w - w[i]))
- **Complexity**: Time O(n*W), Space O(n*W) or optimized O(W).

## 2. Longest Common Subsequence (LCS)
Find length of longest subsequence present in both strings X[1..m] and Y[1..n]:
- If X[i] == Y[j]: c[i, j] = c[i-1, j-1] + 1
- Else: c[i, j] = max(c[i-1, j], c[i, j-1])
- Space and time complexity: O(m*n).

## 3. Greedy Algorithms vs DP
Greedy makes the locally optimal choice at each step without reconsidering prior decisions.
- **Huffman Coding**: Prefix code algorithm utilizing greedy priority queue for lossless data compression.
- **Fractional Knapsack**: Solved greedily by sorting by value-to-weight ratio in O(n log n).""",
                faculty_author="Dr. Sharma",
                academic_year="2025-2026",
                download_count=78
            ),
            CourseNote(
                course_id=c_cs402.id,
                title="Process Synchronization, Semaphores & Deadlocks",
                unit_number=1,
                unit_title="Concurrency & Synchronization",
                topic_description="Critical Section Problem, Peterson's Algorithm, Mutex locks, Counting Semaphores, Classic synchronization problems (Producer-Consumer, Readers-Writers), Coffman Deadlock Conditions.",
                content_markdown="""# Unit 1: Process Synchronization & Deadlocks

## 1. The Critical Section Problem
A critical section is a code segment where shared variables are accessed:
1. **Mutual Exclusion**: If process Pi is executing in its critical section, no other processes can execute in their critical sections.
2. **Progress**: If no process is executing and some want to enter, selection cannot be postponed indefinitely.
3. **Bounded Waiting**: Bound exists on times other processes enter after a process requested entry.

### Semaphores
Synchronization tool introduced by Dijkstra:
- `wait(S)` / `P(S)`: while S <= 0 do wait; S--;
- `signal(S)` / `V(S)`: S++;

## 2. Deadlock Characterization
A deadlock occurs when processes are permanently blocked waiting for resources held by each other:
1. **Mutual Exclusion**: Non-shareable resource mode.
2. **Hold and Wait**: Process holding resources while requesting additional.
3. **No Preemption**: Resources cannot be preempted forcibly.
4. **Circular Wait**: Set of waiting processes {P0, P1, ..., Pn} where P0 waits for P1, ..., Pn waits for P0.

### Banker's Algorithm
Safety algorithm utilizing Available, Max, Allocation, and Need vectors to evaluate safe states before granting resource requests.""",
                faculty_author="Prof. Rao",
                academic_year="2025-2026",
                download_count=56
            ),
            CourseNote(
                course_id=c_cs404.id,
                title="Relational Algebra, SQL & Normalization",
                unit_number=1,
                unit_title="Relational Schema Design & Normal Forms",
                topic_description="Relational data model, Select, Project, Join operations, Functional Dependencies, Lossless Decomposition, 1NF, 2NF, 3NF, BCNF, ACID transactions.",
                content_markdown="""# Unit 1: Relational Algebra & Database Normalization

## 1. Relational Algebra Operations
Fundamental procedural query language operations:
- **Selection (σ)**: Selects tuples that satisfy a given predicate.
- **Projection (π)**: Selects specified columns and eliminates duplicate rows.
- **Natural Join (⋈)**: Combines tuples from two relations on common attributes.
- **Set Operations**: Union (∪), Set Difference (-), Cartesian Product (×).

## 2. Database Normalization & Normal Forms
Prevents data redundancy, insertion, deletion, and update anomalies:
- **First Normal Form (1NF)**: All column values must be atomic (no repeating groups or arrays).
- **Second Normal Form (2NF)**: In 1NF and no non-prime attribute is partially dependent on any candidate key.
- **Third Normal Form (3NF)**: In 2NF and no transitive dependency exists between non-prime attributes (X -> A implies X is superkey or A is prime).
- **Boyce-Codd Normal Form (BCNF)**: Strictly for every functional dependency X -> Y, X must be a superkey.

## 3. Transaction ACID Properties
- **Atomicity**: All operations succeed or none are executed.
- **Consistency**: Preserves database invariants and integrity constraints.
- **Isolation**: Concurrent executions produce same state as serial execution.
- **Durability**: Committed changes persist across power failures and crashes.""",
                faculty_author="Dr. Anita Nair",
                academic_year="2025-2026",
                download_count=89
            ),
            CourseNote(
                course_id=c_cs601.id,
                title="Machine Learning Foundations & Supervised Models",
                unit_number=1,
                unit_title="Supervised Learning & Gradient Descent",
                topic_description="Linear Regression, Cost functions, Batch vs Stochastic Gradient Descent, Logistic Regression, Decision boundaries, Overfitting & Regularization (L1 Lasso / L2 Ridge).",
                content_markdown="""# Unit 1: Machine Learning Foundations

## 1. Supervised Learning Framework
Given dataset D = {(x1, y1), ..., (xm, ym)}, learn mapping function h(x) -> y that generalizes well to unseen data.

### Linear Regression & Mean Squared Error (MSE)
Hypothesis: h_theta(x) = theta_0 + theta_1*x_1 + ... + theta_n*x_n = theta^T * x
Cost function J(theta) = (1 / 2m) * sum((h_theta(x^(i)) - y^(i))^2)

### Gradient Descent Algorithm
Iteratively update weights opposite to gradient vector:
theta_j := theta_j - alpha * (∂J / ∂theta_j)
- Learning rate alpha controls step size. Too large causes divergence; too small causes slow convergence.

## 2. Logistic Regression & Classification
For binary classification where y in {0, 1}:
Hypothesis uses Sigmoid / Logistic function: g(z) = 1 / (1 + e^(-z))
Cross-Entropy Cost Function:
J(theta) = - (1/m) * sum( y^(i)*log(h_theta(x^(i))) + (1 - y^(i))*log(1 - h_theta(x^(i))) )

## 3. Overfitting & Regularization
High variance occurs when model fits noise in training data:
- **L2 Regularization (Ridge)**: Adds penalty lambda * sum(theta_j^2) to shrink weights smoothly.
- **L1 Regularization (Lasso)**: Adds penalty lambda * sum(|theta_j|) producing sparse feature selection.""",
                faculty_author="Dr. K. Patel",
                academic_year="2025-2026",
                download_count=64
            ),
            CourseNote(
                course_id=c_ec401.id,
                title="BJT, MOSFET Small-Signal Models & Operational Amplifiers",
                unit_number=1,
                unit_title="Active Devices & Frequency Response",
                topic_description="Hybrid-pi models, Common Emitter & Source Amplifiers, High frequency poles, Miller's Theorem, Op-Amp inverting/non-inverting configurations, Slew rate, CMRR.",
                content_markdown="""# Unit 1: Active Devices & Analog Signal Processing

## 1. BJT Small-Signal Hybrid-π Model
For small AC variations around the DC quiescent operating point (Q-point):
- Transconductance: gm = Ic / Vt (where thermal voltage Vt ≈ 26mV at 300K).
- Input resistance: r_pi = beta / gm = Vt / Ib.
- Output resistance: ro = Va / Ic (due to Early effect).

## 2. Operational Amplifier Characteristics
Ideal op-amp assumptions:
- Infinite open-loop gain (A_OL -> infinity).
- Infinite input impedance (R_in -> infinity, meaning zero input bias current).
- Zero output impedance (R_out -> 0).
- Infinite Common Mode Rejection Ratio (CMRR -> infinity).
- Virtual Ground Concept: In negative feedback, V+ ≈ V-.""",
                faculty_author="Dr. R. Mishra",
                academic_year="2025-2026",
                download_count=51
            )
        ]
        db.add_all(notes)

        db.commit()
        logger.info("Database seeding completed successfully!")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
