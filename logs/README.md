This directory contains published versions of the CPEE execution logs that provide the basis for the analysis presented in the thesis.

- `regular/`: 120 included regular executions across 12 scenarios, with 10 executions per scenario.
- `errors/`: 12 error-handling tests across four cases, with three tests per case.

Regular logs are grouped by workflow and scenario. Error-handling logs are grouped by case, E1–E4.
Original filenames identify the run number and workflow instance.
To prevent disclosure of credentials, actual backend API-key values in these published copies have been replaced with `BACKEND_API_KEY`.
The invalid API key value intentionally used in E2 has been preserved as part of the test evidence.
Apart from these replacements of credentials, the content of the logs remains unchanged.

The logs contain workflow execution details and the corresponding responses. The corresponding spreadsheet files for the included regular executions are available at: https://github.com/AliEfeKarakis/thesis_TUM/tree/f8dc93439631ec1f53705cd4f9de297e5f6b7f0f/spreadsheets

Error-handling tests were conducted separately from regular runs. Their results should be interpreted in accordance with the case-specific requirements described in the “Evaluation” chapter.
