FAQS = [
    {"question": "How can I prepare for semester exams?", "answer": "Collect the current syllabus, prioritize high-weight topics, practice previous question papers, and revise with short notes. Build a realistic daily timetable."},
    {"question": "How can I improve my coding skills?", "answer": "Practice a small problem daily, explain your approach, test edge cases, and review mistakes. Start with arrays, strings, hash maps, and basic algorithms."},
    {"question": "How do I apply for an internship?", "answer": "Prepare a one-page resume, build or document projects, check trusted company and college placement portals, and tailor each application to the role."},
    {"question": "What should I do if I miss an assignment deadline?", "answer": "Contact the instructor as soon as possible, explain briefly and honestly, ask whether late submission is allowed, and check the course policy."},
    {"question": "How do I reset my college portal password?", "answer": "Use the official portal's password-reset option. If it does not work, contact the college IT/help desk. Never share your password or OTP."},
    {"question": "Where can I find the syllabus?", "answer": "Check the official university or college website, department portal, or learning management system. Confirm the academic year and course code."},
    {"question": "How can I prepare for placements?", "answer": "Practice data structures and algorithms, revise CS fundamentals, build projects you can explain, prepare your resume, and practice technical and HR interviews."},
    {"question": "What if I do not understand a topic?", "answer": "Ask for a simpler explanation, a real-world analogy, a worked example, and then a short quiz to check understanding."},
]

def find_faq(question):
    q = question.lower()
    # Simple keyword-based retrieval; the LLM still generates the final answer.
    keywords = {
        0: ("semester exam", "exam preparation", "study plan", "revision"),
        1: ("coding skills", "learn coding", "programming practice", "leetcode"),
        2: ("internship", "internships"),
        3: ("assignment deadline", "late assignment", "miss an assignment"),
        4: ("reset password", "portal password", "forgot password"),
        5: ("syllabus", "course outline"),
        6: ("placement", "placements", "interview preparation"),
        7: ("don't understand", "do not understand", "explain simply", "confused")
    }
    for idx, terms in keywords.items():
        if any(term in q for term in terms):
            return FAQS[idx]
    return None
