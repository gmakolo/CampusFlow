"""Engineer B: scoring, retry, question-bank independence and ungraded reflection."""
from copy import deepcopy
from unittest import TestCase
from unittest.mock import Mock
from campusflow.question_bank import QUESTIONS
from campusflow.understanding_check import run_understanding_check, score_answers


class UnderstandingCheckTests(TestCase):
    def test_assessment_has_six_required_questions(self):
        self.assertEqual(len(QUESTIONS), 6)
        self.assertTrue(all(set(q["choices"]) == {"A", "B", "C", "D"} for q in QUESTIONS))

    def test_all_correct_scores_six(self):
        self.assertEqual(score_answers([q["correct"] for q in QUESTIONS]), 6)

    def test_all_wrong_scores_zero(self):
        answers = ["A" if q["correct"] != "A" else "D" for q in QUESTIONS]
        self.assertEqual(score_answers(answers), 0)

    def test_mixed_choices_count_only_correct_submissions(self):
        self.assertEqual(score_answers(["b", "c", "a", "c", "a", "b"]), 4)

    def test_invalid_or_incomplete_answer_lists_are_rejected(self):
        for answers in ([], ["A"] * 5, ["A"] * 7, ["X"] * 6):
            with self.subTest(answers=answers), self.assertRaises(ValueError):
                score_answers(answers)

    def test_scoring_uses_supplied_question_bank_without_changing_it(self):
        custom = ({"correct": "A"}, {"correct": "D"})
        before = deepcopy(custom)
        self.assertEqual(score_answers(["a", "d"], custom), 2)
        self.assertEqual(custom, before)

    def test_invalid_answers_retry_without_consuming_question(self):
        reader = Mock(side_effect=["X", "", " b ", "c", "b", "c", "c", "b", "My first explanation", "My second explanation"])
        writer = Mock()
        result = run_understanding_check(reader, writer)
        self.assertEqual(result["score"], 6)
        self.assertEqual(reader.call_count, 10)
        self.assertEqual(sum(c.args[0] == "Choose A, B, C or D." for c in writer.call_args_list), 2)

    def test_explanations_are_recorded_but_not_graded(self):
        reader = Mock(side_effect=["A"] * 6 + ["", "An explanation without grading keywords", "Another explanation"])
        result = run_understanding_check(reader, Mock())
        self.assertEqual(result["score"], 0)
        self.assertEqual(len(result["explanations"]), 2)
        self.assertNotIn("explanation_score", result)

    def test_answers_are_not_revealed_before_submission(self):
        output = []
        choices = iter([q["correct"] for q in QUESTIONS] + ["First explanation", "Second explanation"])
        def reader(prompt):
            if prompt.startswith("Your answer"):
                self.assertFalse(any("Correct answer:" in text or "Final score:" in text for text in output))
            return next(choices)
        run_understanding_check(reader, output.append)
        self.assertIn("Final score: 6/6", "\n".join(output))

    def test_end_of_input_does_not_invent_a_completed_score(self):
        writer = Mock()
        with self.assertRaises(EOFError):
            run_understanding_check(Mock(side_effect=EOFError), writer)
        self.assertFalse(any("Final score:" in c.args[0] for c in writer.call_args_list))
