This directory explains how the error-handling results reported in the thesis were assessed and summarized.

The assessment covers 12 error-handling tests: four cases, E1–E4, with three tests per case. Each test used a new instance of the Spreadsheet Order Filtering workflow and the business data from scenario S1.

These tests were evaluated separately from the 120 included regular executions.

The [error-handling execution logs](../../logs/errors/) contain the recorded responses, activity histories and workflow states. The reported manual checks compared this evidence with the predefined response and workflow-behavior requirements for each case.

The comparison covered:

- The content of the returned response.
- The HTTP status code where specified in the case requirements.
- The required workflow path and stopping point.
- Whether the rejected activity was reported as successfully completed.
- Whether subsequent activities were executed when they should not have been.

Reaching the stopped state alone was not sufficient to pass.

The case-specific requirements were:

- E1 — Missing Google authorization: return `authorized=false`, `error_type=auth_required` and an authorization URL. Store the authorization information and follow the modeled authorization-required stop before any spreadsheet operation.
- E2 — Invalid backend API key: return HTTP 401 with `ok=false`, `error_type=unauthorized` and a message identifying the invalid or missing API key.
- E3 — Invalid write input: return an explicit input-validation response with an HTTP status in the 400–499 range and a message identifying the invalid input.
- E4 — Nonexistent worksheet: catch the Google Sheets error and return JSON containing `ok=false`, `operation=readData` and an explanation identifying the invalid range.

For E2–E4, the affected activity must not be reported as successfully completed, and subsequent workflow activities must not be executed.

E4 evaluates the reporting of the external-service error and the resulting workflow stop. Preserving the HTTP status returned by Google Sheets was not part of its pass criteria. The observed conversion of HTTP 400 to HTTP 500 therefore does not change the E4 classification, but passing E4 does not demonstrate correct HTTP-status preservation.

Each test belongs to one category:

- Passed: sufficient evidence confirms that all response and workflow-behavior requirements for the case were met.
- Failed: evidence shows that at least one requirement was violated.
- Unevaluable: the evidence is insufficient to establish either a pass or a failure.

The numbers of passed, failed and unevaluable tests are denoted by `P_EH`, `F_EH` and `U_EH`, respectively. The suffix `EH` identifies counts belonging to the error-handling tests.

Example:

In E3, the literal text `nil` was supplied in the `values` argument of Write Headers (`a8`). The operation expects a JSON-encoded array of rows. This was an invalid input value, not a missing argument or a JSON null value.

The predefined requirements were:

- An explicit input-validation response with an HTTP status in the 400–499 range and a message identifying the invalid input.
- No successful completion of the rejected write activity.
- A workflow stop without subsequent activity execution.

The [E3 run 01 execution log](../../logs/errors/E3/run_01_25da437a-d080-4231-8432-463c3e160ed8.xes.yaml) records an HTTP 500 response containing a `JSONDecodeError`. The write activity was not recorded as successfully completed. CPEE stopped at Write Headers without calling subsequent workflow activities.

The workflow-stop requirement was met, but the required input-validation response was missing. The test was therefore classified as failed.

The other two E3 tests showed the same outcome. Their logs are available in the [E3 directory](../../logs/errors/E3/).

The error-handling ratio is calculated as:

```text
EH = P_EH / (P_EH + F_EH)
```

The denominator counts tests that can be classified as passed or failed. Unevaluable tests are reported separately and are excluded from this denominator. The ratio is undefined if there are no evaluable tests.

The recorded classifications were:

- E1: 3 passed, 0 failed, 0 unevaluable.
- E2: 3 passed, 0 failed, 0 unevaluable.
- E3: 0 passed, 3 failed, 0 unevaluable.
- E4: 3 passed, 0 failed, 0 unevaluable.

Therefore:

```text
P_EH = 3 + 3 + 0 + 3 = 9
F_EH = 0 + 0 + 3 + 0 = 3
U_EH = 0

Total tests = P_EH + F_EH + U_EH = 12

EH = 9 / (9 + 3) = 0.75 = 75%
```

The result means that 9 of the 12 evaluable tests met all requirements defined for their respective cases. All 12 tests reached the stopped state, but the three E3 tests failed because stopping alone did not satisfy their response requirements.

This ratio summarizes four selected error cases within one workflow. It does not estimate how often the prototype would handle other faults correctly or demonstrate automatic recovery.
