# Spreadsheet Automation with CPEE

This repository contains the Python backend, CPEE workflow models and evaluation evidence used in the thesis. The prototype combines reusable Google Sheets operations with workflow control and human participation.

CPEE stands for Cloud Process Execution Engine. It executes the workflows, calls the backend operations and coordinates the human tasks.

The four workflows are:

- Spreadsheet Order Filtering
- Invoice Registration
- Vendor Onboarding and Ticket Processing
- Travel Authorization Request Processing

## Repository contents

- [app.py](app.py): backend entry point.
- [config.py](config.py): backend configuration.
- [requirements.txt](requirements.txt): Python dependencies.
- [routes/](routes/): health, authorization and spreadsheet endpoints.
- [auth/](auth/): Google OAuth authorization and token handling.
- [services/](services/): Google Sheets service access.
- [utils/](utils/): request and backend API-key handling.
- [workflows/](workflows/): the four CPEE workflow models.
- [worklists/](worklists/): organizational model and user-task forms.
- [spreadsheets/](spreadsheets/): Excel exports from the 120 included regular executions.
- [logs/](logs/): regular-execution and error-handling logs.
- [metrics/](metrics/): explanations and worked examples for the evaluation metrics.

The spreadsheet exports and execution logs are evaluation evidence. They are not input files required to run the workflows.

## Requirements

You need:

- Python 3.10 or newer and pip.
- A Google account and a Google Cloud project with the Google Sheets API enabled.
- Google OAuth client credentials.
- Access to a CPEE engine and its browser interface.
- Access to the CPEE worklist interface for scenarios requiring human participation.
- Hosting for the organizational model and HTML forms.
- A backend URL that the selected CPEE engine can reach.

Using the CPEE website means that requests to the backend are sent by the CPEE engine. A localhost URL on your computer is therefore not sufficient for a remotely hosted engine.

## 1. Download and install the backend

Download the repository through GitHub's Code > Download ZIP option and extract it, or clone it with Git.

Open the extracted repository directory in your IDE or terminal. This is the directory containing `app.py`.

Create a Python virtual environment, either through your IDE or with:

```text
python -m venv .venv
```

Select the virtual environment as your project's Python interpreter. Before running the installation command, activate that environment in your terminal or use an IDE terminal configured to use it. Selecting an IDE interpreter does not necessarily update an already-open terminal.

Install the dependencies using that environment:

```text
python -m pip install -r requirements.txt
```

The commands assume that `python` refers to the selected interpreter. If your installation uses `python3`, use:

```text
python3 -m venv .venv
```

After activating or selecting that environment, install the dependencies with:

```text
python3 -m pip install -r requirements.txt
```

## 2. Configure the backend

Set the following environment variables for the process that runs `app.py`. You can use your IDE's run configuration or your operating system's environment-variable settings.

- `CPEE_API_KEY`: your chosen nonempty backend API key.
- `BASE_URL`: the externally accessible base URL of your backend, without a trailing slash.
- `OAUTH_REDIRECT_URI`: the complete callback URL ending in `/oauth2callback`.

`CPEE_API_KEY` is required for the backend to start. `BASE_URL` defaults to `http://localhost:9001`, and `OAUTH_REDIRECT_URI` defaults to `BASE_URL` followed by `/oauth2callback`. For another deployment, configure these values explicitly so that the callback points to the intended backend.

For example:

```text
BASE_URL=https://backend.example
OAUTH_REDIRECT_URI=https://backend.example/oauth2callback
```

`backend.example` is a placeholder. Replace it throughout these instructions with your actual backend address. The address must already be routed to the running backend; setting these variables does not establish that routing.

If your deployment uses a URL prefix, include it in both values.

`CPEE_API_KEY` protects the spreadsheet endpoints. It is separate from the Google OAuth client credentials and the worklist account.

The application reads environment variables directly. Creating a `.env` file alone does not configure it.

In `config.py`, check:

```python
HOST = "::1"
PORT = 9001
```

`9001` is the supplied port, not a required value. To use another available port, change `PORT` in `config.py` and configure your hosting to forward requests to that port. The current implementation does not read `PORT` from an environment variable.

Changing `PORT` does not automatically update `BASE_URL` or `OAUTH_REDIRECT_URI`. If the externally accessible backend address changes, update these environment variables, the workflow endpoint URLs and the authorized redirect URI in Google Cloud accordingly. If only the internal listening port changes and the external address remains unchanged, those external URLs can remain unchanged.

`HOST` controls the address on which the Python server listens. The supplied value is IPv6 loopback. If your hosting setup forwards requests to IPv4 loopback, change it to:

```python
HOST = "127.0.0.1"
```

Use the listening address and port required by your hosting setup. `BASE_URL` describes the externally accessible address, while `HOST` and `PORT` configure where the Python application listens.

Configure your hosting so that requests to the backend URL reach this Python application. The university-server URLs contained in the workflow files must be replaced as described below.

Keep actual API keys, `client_secret.json` and generated token files out of the published repository.

## 3. Configure Google authorization

In Google Cloud:

1. Create or select a project.
2. Enable the Google Sheets API.
3. Configure the Google Auth platform and consent settings.
4. If the application uses an external testing audience, add the Google account you will use as a test user.
5. Configure the Google Sheets scope used by the backend:

```text
https://www.googleapis.com/auth/spreadsheets
```

6. Create an OAuth client with application type Web application.
7. Add the exact `OAUTH_REDIRECT_URI` value as an authorized redirect URI.
8. Download the OAuth client JSON file, rename it `client_secret.json` and place it beside `app.py`.

The backend uses OAuth authorization for a Google user. It does not use a service-account configuration.

See Google's documentation for [OAuth consent configuration](https://developers.google.com/workspace/guides/configure-oauth-consent) and [OAuth client credentials](https://developers.google.com/workspace/guides/create-credentials).

## 4. Start the backend and authorize access

Run `app.py` from the repository root using the configured Python environment:

```text
python app.py
```

If your configured Python environment uses the `python3` command instead, run:

```text
python3 app.py
```

Use the same Python environment in which you installed the dependencies. Keep the backend running while executing workflows.

Open your backend URL followed by `/health`. For example:

```text
https://backend.example/health
```

The expected response contains:

```json
{"ok": true}
```

Then open:

```text
https://backend.example/authorize?user_id=default
```

This endpoint returns JSON containing an `authorization_url`. Open that URL, sign in with the intended Google account and grant access.

After the callback completes, check:

```text
https://backend.example/auth/status?user_id=default
```

The response should contain `authorized=true`.

The backend creates the `tokens` directory when saving authorization. Keep `user_id` set to `default` in the supplied workflows unless you deliberately configure another authorization context consistently.

If a workflow stops because Google authorization is missing, complete authorization and manually restart it. Authorization does not automatically resume the stopped workflow.

## 5. Prepare the worklist files

The [worklists directory](worklists/) contains `org.xml` and the three forms used by the workflows.

In `worklists/org.xml`, adjust the subject identity to match the worklist account that will perform the human tasks. In particular, configure the subject's `uid` for that account.

Host `org.xml` and the HTML files at URLs accessible to the worklist service and the browser displaying the tasks.

The forms are:

- `define_price_list.html`: provide a new price-list name.
- `correct_vendor_information.html`: provide missing vendor information.
- `personal_car_decision.html`: accept or reject personal-car use.

Starting `app.py` does not make `org.xml` or the HTML forms available through web URLs. Serve these files through a web server so that the worklist service and the browser can retrieve them. This can use the same server as the backend; a separate server is not required.

The URLs must serve the XML or HTML content. A GitHub file-view page does not serve the form itself.

## 6. Import and configure the workflows

The workflow files are:

- [Thesis_Workflow_Spreadsheet_Order_Filtering.xml](workflows/Thesis_Workflow_Spreadsheet_Order_Filtering.xml)
- [Thesis_Workflow_Invoice_Registration.xml](workflows/Thesis_Workflow_Invoice_Registration.xml)
- [Thesis_Workflow_Vendor_Onboarding_and_Ticket_Processing.xml](workflows/Thesis_Workflow_Vendor_Onboarding_and_Ticket_Processing.xml)
- [Thesis_Workflow_Travel_Authorization_Request_Processing.xml](workflows/Thesis_Workflow_Travel_Authorization_Request_Processing.xml)

Open the [CPEE interface](https://cpee.org/flow/) and create a new instance. Import the selected XML file using the testset-loading option so that its data objects, endpoints and process model are loaded together.

Before starting it, make the following changes. These can be made manually in CPEE or in a local copy of the XML before importing it.

### Backend endpoints

Replace the university backend address in the workflow endpoints with your backend address. Preserve each operation path and HTTP method.

For an HTTPS deployment, for example:

```text
Old:
https-get://lehre.bpm.in.tum.de/ports/9001/auth/status

New:
https-get://backend.example/auth/status
```

```text
Old:
https-post://lehre.bpm.in.tum.de/ports/9001/createSpreadsheet

New:
https-post://backend.example/createSpreadsheet
```

Apply the same replacement to every spreadsheet-operation endpoint present in the model.

The `https-get` and `https-post` prefixes are CPEE endpoint notation. Keep them for HTTPS endpoints. An HTTP deployment uses the corresponding `http-get` and `http-post` prefixes.

Do not replace unrelated CPEE service URLs. If you use the supplied hosted worklist service, its endpoint remains:

```text
https-post://cpee.org/worklist/server/
```

### Backend API key

Replace every `BACKEND_API_KEY` placeholder in the `api_key` arguments with the value configured as `CPEE_API_KEY` in your backend environment.

Keep the argument name `api_key` unchanged.

Make these replacements only in your execution copies. Published workflow models should retain the placeholder.

### Organizational-model and form URLs

In the corresponding user tasks, update the following entries under Arguments:

- Organisation Model: the hosted URL of your `org.xml`.
- Form Link: the hosted URL of the appropriate HTML form.

Assign the forms as follows:

- Define New Price List in Invoice Registration: `define_price_list.html`
- Correct Vendor Information in Vendor Onboarding and Ticket Processing: `correct_vendor_information.html`
- Personal Car Decision in Travel Authorization Request Processing: `personal_car_decision.html`

All three tasks use the hosted organizational-model URL. When editing the XML directly, these argument names are `orgmodel` and `form`.

The supplied URLs point to the original university deployment and must be replaced for another deployment.

## 7. Configure the scenario inputs

The published models contain initial data objects and activity arguments. Some business inputs must be configured before execution.

The evaluation used the settings below. Scenario differences were introduced through input values and prescribed human responses, without changing the workflow control logic or backend operation implementations.

For each execution, use a fresh workflow instance. Keep data objects not listed as scenario inputs at their imported initial values. Do not copy generated spreadsheet IDs, previous results or completed-run state into a new execution.

To repeat a scenario, you can save a private copy of the configured testset before starting it and load that copy into a new instance for each execution. Save it before execution so that it contains the configured inputs and initial state rather than results from a completed run. Keep copies containing your actual backend API key out of the published repository.

Use the Data Objects area for the named workflow inputs. Where `nil` is specified below, retain the model's initial `nil` value. Configure `personalCarRequested` as a Boolean `true` or `false`.

### Spreadsheet Order Filtering: S1–S3

Select Append Sample Orders (`a7`). Configure its `values` argument.

For S1, use:

```json
[
  ["ORD-001", "Alice", "Laptop Stand", 49.9, "Completed"],
  ["ORD-002", "Bob", "Keyboard", 79.0, "Pending"],
  ["ORD-003", "Clara", "Mouse", 29.5, "Completed"],
  ["ORD-004", "David", "Monitor", 249.0, "Cancelled"]
]
```

For S2 and S3, keep the order IDs, customers, products and amounts unchanged. Change only the status values:

- S1: `Completed`, `Pending`, `Completed`, `Cancelled`
- S2: `Completed`, `Completed`, `Completed`, `Completed`
- S3: `Pending`, `Cancelled`, `Pending`, `Cancelled`

The expected Completed Orders output contains:

- S1: `ORD-001` and `ORD-003`
- S2: all four orders
- S3: the header without order records

These scenarios do not require user tasks during regular execution.

### Invoice Registration: I1–I3

For all three scenarios, set `invoiceCurrency` to `EUR`.

Keep the existing price-list inputs in Append Existing Price Lists unchanged: `Price List A`, `Price List B` and `Price List C`.

For I1:

- `invoiceName`: `Invoice-Test-01`
- `requestedPriceList`: `Price List A`
- No human response is required.

For I2:

- `invoiceName`: `Invoice-Test-02`
- `requestedPriceList`: `Special Price List`
- In Define New Price List, enter `Special Price List` and submit once.

For I3:

- `invoiceName`: `Invoice-Test-03`
- `requestedPriceList`: `Validation Test List`
- In the first Define New Price List task, enter exactly three ordinary spaces and submit.
- In the repeated task, enter two spaces, followed by `Corrected Price List`, followed by two spaces, and submit.

For I3, the first response causes another user-task invocation. The second response is trimmed, and `Corrected Price List` is stored and added once to the price lists.

### Vendor Onboarding and Ticket Processing: V1–V3

For all three scenarios, set:

- `vendorName`: `Example Supplies`
- `vendorCountry`: `Germany`
- `contactPerson`: `Test Contact`

For V1:

- `requestId`: `VENDOR-TEST-01`
- `vendorTaxId`: `TEST-TAX-001`
- `requestEvidence`: `Test request documentation`
- No correction task is required.

For V2:

- `requestId`: `VENDOR-TEST-02`
- `vendorTaxId`: retain the initial `nil` value
- `requestEvidence`: `Test request documentation`
- In Correct Vendor Information, enter `TEST-TAX-002` in the Tax ID field and retain the other values.

For V3:

- `requestId`: `VENDOR-TEST-03`
- `vendorTaxId`: retain the initial `nil` value
- `requestEvidence`: retain the initial `nil` value
- In the first correction task, enter `TEST-TAX-003` in the Tax ID field and exactly three spaces in Request Evidence. Retain the other values.
- In the repeated task, retain `TEST-TAX-003` and enter `Test request documentation` in Request Evidence. Retain the other values.

For V3, the first response remains incomplete. Ticket creation occurs after the second, complete response.

### Travel Authorization Request Processing: T1–T3

For all three scenarios, set:

- `employeeName`: `Test Employee`
- `destination`: `Berlin`
- `startDate`: `2026-11-10`
- `endDate`: `2026-11-12`
- `travelPurpose`: `Project meeting`

For T1:

- `travelRequestId`: `TRAVEL-TEST-01`
- `personalCarRequested`: `false`
- No personal-car decision task is required.

For T2:

- `travelRequestId`: `TRAVEL-TEST-02`
- `personalCarRequested`: `true`
- Select `Accept` in Personal Car Decision and submit.

For T3:

- `travelRequestId`: `TRAVEL-TEST-03`
- `personalCarRequested`: `true`
- Select `Reject` in Personal Car Decision and submit.

Both acceptance and rejection of personal-car use are recorded, and processing continues to `Submitted`. Rejection of personal-car use does not reject the entire travel request.

## 8. Execute and inspect the results

After configuring the deployment settings and scenario inputs:

1. Start the workflow in CPEE.
2. For scenarios requiring human participation, open the worklist interface using the account configured in `org.xml`.
3. Complete the tasks using the responses specified for the selected scenario.
4. Inspect the final workflow state, execution log and generated spreadsheet.

The four workflows have no explicit stop activity at the end of their normal execution paths. After successful completion of the final activities, they can reach the `finished` state. The intentional stop in the Authorization Required branch remains separate from normal completion.

Each regular execution creates a new spreadsheet. Its identifier is stored in the `spreadsheetId` data object. Open that spreadsheet in Google Sheets using:

```text
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
```

Replace `SPREADSHEET_ID` with the generated identifier.

The final verification activities read back spreadsheet records. Their names do not mean that they automatically perform the full correctness assessment described in the thesis.

The evaluation used 10 fresh executions per scenario, with the same business inputs and prescribed human responses within each scenario. Running the prototype once does not require repeating all 120 executions.

## Evaluation evidence and metric explanations

The [regular logs](logs/regular/) and [spreadsheet exports](spreadsheets/) document the 120 included regular executions. The [error-handling logs](logs/errors/) document 12 separate tests.

The following READMEs explain the assessments and calculations, including worked examples:

- [Execution time](metrics/execution-time/README.md).
- [Functional correctness and correct repeated executions](metrics/correctness-repeatability/README.md).
- [Error handling](metrics/error-handling/README.md).
- [Operation reuse](metrics/operation-reuse/README.md).

Actual backend API-key values in published workflow models and logs have been replaced with `BACKEND_API_KEY`. The intentionally invalid key used in error case E2 is preserved as test evidence.
