MODES = {
    "zero": {"label": "Zero-shot", "description": "Direct question, no examples."},
    "few": {"label": "Few-shot", "description": "Uses examples to guide answer style."},
    "role": {"label": "Role prompting", "description": "Answers as a friendly computer science tutor."},
    "faq": {"label": "Intelligent FAQ", "description": "General student assistant with FAQ context when available."}
}

BASE_SYSTEM = (
    "You are a helpful study assistant for college students. Be accurate, clear, and useful. "
    "Use simple language, define technical terms, and give examples when useful. "
    "Do not invent college-specific rules, deadlines, contact details, attendance requirements, or policies. "
    "If required information is not provided, say you do not have enough information and suggest checking the official college source."
)

def build_prompt(question, mode, history=None, faq_match=None):
    history = history or []
    conversation = ""
    if history:
        conversation = "\n\nRecent conversation:\n" + "\n".join(
            f"{'Student' if item['role'] == 'user' else 'Assistant'}: {item['content']}"
            for item in history
        )

    if mode == "zero":
        system = BASE_SYSTEM + " Answer the student's question directly. No examples are supplied."
        prompt = f"Student question: {question}\n\nGive a clear, direct answer."
    elif mode == "few":
        system = BASE_SYSTEM + " Follow the demonstrated concise question-and-answer style."
        prompt = (
            "Use the examples as a guide for clarity and format, not as facts about the new question.\n\n"
            "Example 1\nQuestion: What is a CPU?\n"
            "Answer: CPU means Central Processing Unit. It executes program instructions and performs calculations.\n\n"
            "Example 2\nQuestion: What is RAM?\n"
            "Answer: RAM means Random Access Memory. It temporarily holds data that programs are using.\n\n"
            f"Now answer this question:\nQuestion: {question}\nAnswer:"
        )
    elif mode == "role":
        system = (
            "You are a patient, friendly computer science professor teaching a beginner. "
            "Explain concepts simply, use one relatable example, and end with three key takeaways when appropriate. "
            + BASE_SYSTEM
        )
        prompt = f"Student question: {question}\nTeach the topic in a beginner-friendly way."
    else:
        system = BASE_SYSTEM + (
            " For study questions, organize the answer with short headings or bullets when useful. "
            "For exam questions, match the requested mark length. For FAQ questions, be practical and concise."
        )
        faq_context = ""
        if faq_match:
            faq_context = (
                "\n\nPotentially relevant FAQ reference (use only if relevant; do not treat it as official policy unless "
                "it explicitly provides that information):\n"
                f"Question: {faq_match['question']}\nAnswer: {faq_match['answer']}"
            )
        prompt = (
            "Answer the student's request. If it asks about a college-specific policy not present in the context, "
            "state that the official policy needs to be checked.\n"
            f"{faq_context}{conversation}\n\nStudent: {question}\nAssistant:"
        )
    return prompt, system
