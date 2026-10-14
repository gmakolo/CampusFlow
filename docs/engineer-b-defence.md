# Explain five Engineer B tests — Refs #2

All new code/tests are AI-assisted drafts for miikese to inspect, reproduce, and explain. Passing tests do not substitute for the fellow's defence.

1. **`test_casefold_matches_unicode_sharp_s`**: puts `Straße` in a title and searches for `STRASSE`. It must match. This tests the required Unicode normalization, not just English upper/lower case.
2. **`test_combined_filters_use_and`**: fixtures deliberately differ in category, status, and priority. Only `T001` matches every requested filter. Using OR would include additional records and fail the test.
3. **`test_results_do_not_alias_nested_notes`**: edits both a returned title and a nested note, then compares the original collection with a deep snapshot. This proves result edits cannot mutate stored records.
4. **`test_known_fixture_has_accurate_totals`**: four records give exact status/category/priority counts, three unresolved, one resolved, and 25%. Comparing whole groups catches omissions and double-counting.
5. **`test_invalid_answers_retry_without_consuming_question`**: feeds invalid answers before six valid submissions. The score remains 6/6, the prompt count includes retries, and invalid input does not advance the question.

Additional useful checks: empty reports are 0%; reopened tickets use current status; note-menu tests assert calls to A's mocked API; failed load adapters preserve memory; the CLI blocks resolved mutation while the direct backend bug remains visible separately.

## Practice commands

```bash
python3 -m unittest tests.test_search.SearchTests.test_combined_filters_use_and -v
python3 -m unittest tests.test_search.SearchTests.test_results_do_not_alias_nested_notes -v
python3 -m unittest tests.test_reports.ReportingTests.test_known_fixture_has_accurate_totals -v
python3 -m unittest tests.test_understanding.UnderstandingCheckTests.test_invalid_answers_retry_without_consuming_question -v
python3 main.py
```

Choose quiz option 12 and answer independently. Explanations are displayed for mentor discussion and are not graded by keywords. Changing an expected value to force a test to pass is not a defence; explain the fixture, contract, assertion, and failure mode.
