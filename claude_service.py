import google.generativeai as genai
import json
from app.core.config import settings
from app.models.quiz import QuizQuestion, QuizOption

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")

async def generate_questions(topic, difficulty, num_questions):
    prompt = f"""Generate {num_questions} multiple choice quiz questions
about "{topic}" at {difficulty} difficulty level.

Return ONLY valid JSON, no markdown, no extra text:
{{
  "questions": [
    {{
      "id": 1,
      "question": "Question text here?",
      "options": [
        {{"label": "A", "text": "Option A"}},
        {{"label": "B", "text": "Option B"}},
        {{"label": "C", "text": "Option C"}},
        {{"label": "D", "text": "Option D"}}
      ],
      "correct_label": "A",
      "explanation": "Why this is correct.",
      "roastWrong": "Funny roast for wrong answer.",
      "cheerRight": "Encouragement for correct answer."
    }}
  ]
}}"""

    response = model.generate_content(prompt)

    raw = response.text.strip()

    # Clean markdown if Gemini adds it
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)

    questions = []
    for q in data["questions"]:
        options = [QuizOption(**opt) for opt in q["options"]]
        questions.append(QuizQuestion(
            id=q["id"],
            question=q["question"],
            options=options,
            correct_label=q["correct_label"],
            explanation=q["explanation"],
            roastWrong=q.get("roastWrong", "Wrong!"),
            cheerRight=q.get("cheerRight", "Correct!")
        ))

    return questions