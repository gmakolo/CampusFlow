"""Engineer B: pure scoring and an interactive six-question understanding check."""

from .question_bank import QUESTIONS


def normalize_answer(answer):
    if not isinstance(answer, str) or answer.strip().upper() not in ("A", "B", "C", "D"):
        raise ValueError("Choose A, B, C or D.")
    return answer.strip().upper()


def score_answers(answers, questions=QUESTIONS):
    """Score submitted choices only. Written explanations are never auto-graded."""
    if len(answers) != len(questions):
        raise ValueError("Submit one answer for each question.")
    normalized = [normalize_answer(answer) for answer in answers]
    return sum(answer == question["correct"] for answer, question in zip(normalized, questions))


def run_understanding_check(input_fn=None, output_fn=None, questions=QUESTIONS):
    input_fn = input if input_fn is None else input_fn
    output_fn = print if output_fn is None else output_fn
    if len(questions) < 2:
        raise ValueError("The interactive check needs at least two questions to explain.")
    answers = []
    output_fn("\n===== Engineering Understanding Check =====")
    output_fn("Choose A/B/C/D for each question. Explain two answers for mentor discussion.")
    for index, question in enumerate(questions, 1):
        output_fn(f"\nQ{index}. {question['prompt']}")
        for letter, text in question["choices"].items():
            output_fn(f"  {letter}. {text}")
        while True:
            try:
                answer = normalize_answer(input_fn("Your answer (A/B/C/D): "))
                break
            except ValueError as error:
                output_fn(str(error))
        answers.append(answer)
        output_fn("Answer recorded.")
    score = score_answers(answers, questions)
    output_fn(f"\nFinal score: {score}/{len(questions)}")
    explanations = {}
    for number in (1, 2):
        while True:
            explanation = input_fn(f"Explain your answer to Q{number} in your own words: ").strip()
            if explanation:
                explanations[number] = explanation
                break
            output_fn("Please add your own explanation for mentor discussion.")
    output_fn("\nMentor discussion notes (not automatically graded):")
    for number, explanation in explanations.items():
        output_fn(f"  Q{number}: {explanation}")
    return {"score": score, "maximum": len(questions), "answers": answers, "explanations": explanations}
