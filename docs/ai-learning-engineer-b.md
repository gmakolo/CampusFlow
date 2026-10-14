# Engineer B AI-assisted study evidence — Refs #2

These are **assistant-executed study experiments**, prepared for miikese to reproduce and explain. They are not fabricated first-person learner reflections or proof of independent human authorship. Engineer A's existing `docs/ai-learning-log.md` is preserved.

## Exercise 1: casefold versus lower

Question investigated: Does `lower()` give the same Unicode title-search behavior as `casefold()`?

AI guidance: Both ignore many case differences, but casefold handles additional Unicode caseless comparisons. Use the assessment's required `casefold()` for both query and title.

Unrelated experiment actually executed:

```python
book = "Straße notebook"
assert "STRASSE".lower() not in book.lower()
assert "STRASSE".casefold() in book.casefold()
```

Observed output: lower match `False`; casefold match `True`. Independent assertions passed. Project regression: `SearchTests.test_casefold_matches_unicode_sharp_s`. Decision: casefold on both sides; no fuzzy punctuation/spelling correction is promised.

Learner to complete after running it: What did you expect? Why does the result differ? Can you explain the corresponding test in your own words?

## Exercise 2: shallow-copy proposal rejected after testing

Question investigated: Is `record.copy()` enough to keep read-only search results from affecting a ticket's nested notes?

Candidate design considered: copy dictionaries with `.copy()` (as in the previous personal repository's flat eight-field records). This was **rejected after verification**, not described as an invented AI hallucination.

Unrelated experiment actually executed:

```python
from copy import deepcopy
book = {"title": "Library book", "notes": [{"message": "Original"}]}
shallow = book.copy()
shallow["notes"][0]["message"] = "Changed"
assert book["notes"][0]["message"] == "Changed"
book = {"title": "Library book", "notes": [{"message": "Original"}]}
independent = deepcopy(book)
independent["notes"][0]["message"] = "Changed"
assert book["notes"][0]["message"] == "Original"
```

Observed output: shallow copy protected nested notes `False`; deep copy protected them `True`. Independent assertions passed. Decision: `deepcopy` search results and the optional sorted view. Project regression: `SearchTests.test_results_do_not_alias_nested_notes`.

Learner to complete: Explain the difference between copying a dictionary and copying its nested objects. Which test demonstrates the invariant?

## Genuine test-development corrections in this session

Two initial new test assertions failed: one expected the literal word `Invalid` although the CLI returned a more precise category message; another compared a printed score against an output list entry with a leading newline. Assertions were corrected to check the intended semantic output, retaining the state, ID, and scoring checks. These were assertion mismatches, not falsely labelled business-rule defects.

## Human work still required

Miikese must reproduce the experiments, record personal questions/reflections honestly, take the quiz independently, explain two answers, and review the implementation. Gmakolo must supply her own Next contribution and learning/review evidence. No human review, approval, reflection, or assessment score is invented by this document.
