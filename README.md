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

Download the repository through GitHub's Code > Download ZIP option and extract it or clone it with Git.

Open the extracted repository directory in your IDE or terminal. This is the directory containing `app.py`.

Create the virtual environment on the computer or server where the backend will run, in the project's final directory. If you move or transfer the project, recreate the environment at the destination and reinstall the dependencies.

Create a Python virtual environment in the repository directory:

```text
python -m venv .venv
```

If your Python installation uses `python3`, use this command instead:

```text
python3 -m venv .venv
```

Activate the environment using the command for your operating system and terminal. Run only the applicable activation command from the repository directory.

Windows — Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Windows — PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS or Linux — bash or zsh:

```sh
source .venv/bin/activate
```

After activation, install the dependencies in the same terminal:

```text
python -m pip install -r requirements.txt
```

After activation, the `python` command uses the virtual environment's interpreter, including when the environment was created using `python3`.

If you use an IDE, select `.venv` as the project's Python interpreter. Selecting an IDE interpreter does not necessarily activate an already-open terminal.

Keep this environment active when starting the backend later. If you open a new terminal, return to the repository directory and activate the environment again.

## 2. Set the backend API key, URL, host and port

Open `config.py` in your downloaded copy of the repository. The following instructions explain how to configure this local copy without setting environment variables.

### Set your backend API key

Find:

```python
API_KEY = os.environ["CPEE_API_KEY"]
```

Replace that line with:

```python
API_KEY = os.environ.get("CPEE_API_KEY", "YOUR_CHOSEN_BACKEND_API_KEY")
```

Replace `YOUR_CHOSEN_BACKEND_API_KEY` with your own nonempty backend API key. Keep the first `"CPEE_API_KEY"` unchanged.

Keep the validation code immediately below this line unchanged. It prevents the backend from starting with an empty or whitespace-only key.

Use the same key in the workflows' `api_key` arguments when following Section 6. This key protects the backend spreadsheet endpoints. It is separate from your Google OAuth credentials and worklist account.

Make this change in the execution copy that will run on your computer or server. If you edit it locally before deployment, upload the configured `config.py` to the backend directory on that server. Do not commit or push your actual key to the published repository.

### Set your backend URL

You need a backend address that the CPEE engine can reach. Your hosting setup must route requests from that address to the Python application. Entering an address in `config.py` does not establish this connection.

Find the `BASE_URL` block and replace `http://localhost:9001` with your backend address.

For example:

```python
BASE_URL = os.environ.get(
    "BASE_URL",
    "https://backend.example"
)
```

`https://backend.example` is a placeholder. Replace it with your actual backend address, without a trailing slash. Include any URL prefix required by your deployment.

Keep the first `"BASE_URL"` unchanged.

Leave the following block unchanged:

```python
OAUTH_REDIRECT_URI = os.environ.get(
    "OAUTH_REDIRECT_URI",
    f"{BASE_URL}/oauth2callback"
)
```

This derives the default Google authorization callback URL from `BASE_URL`. For the example above, the callback URL is:

```text
https://backend.example/oauth2callback
```

You will register this callback URL in Google Cloud in Section 3.

### Check HOST and PORT

In the same file, find:

```python
HOST = "::1"
PORT = 9001
```

These settings control the address and port on which the Python application listens.

Keep `PORT = 9001` if your hosting forwards requests to port `9001`. Otherwise, replace `9001` with the port required by your hosting setup.

`HOST = "::1"` uses IPv6 loopback. If your hosting forwards requests to IPv4 loopback, change it to:

```python
HOST = "127.0.0.1"
```

Use the listening address required by your hosting setup. The implementation reads `HOST` and `PORT` directly from `config.py`.

Changing the listening port does not automatically change the external backend address. If the external address changes, update `BASE_URL`, the callback URL registered in Google Cloud and the workflow endpoints described in Section 6.

### Save the configuration

Save `config.py` after making your changes. You will start the backend in Section 4.

Environment variables named `CPEE_API_KEY`, `BASE_URL` or `OAUTH_REDIRECT_URI` take precedence over the corresponding defaults in your edited file. If you previously set these variables, remove the overrides to use the file-based settings described here or update them to the intended values. An empty `CPEE_API_KEY` environment variable also overrides the file value and prevents startup.

No `.env` file is required for this setup.

Keep actual API keys, `client_secret.json` and generated token files out of the published repository.

## 3. Configure Google authorization

The backend uses OAuth authorization to access Google Sheets on behalf of a Google user. These Google credentials are separate from the backend API key configured in Section 2.

Open the [Google Cloud Console](https://console.cloud.google.com/) and complete the following steps.

1. **Create or select a project.**

   Use the project selector at the top of the console. Keep this project selected throughout the following steps.

2. **Enable the Google Sheets API.**

   Open APIs & Services > Library, search for Google Sheets API and click Enable. If the API is already enabled, no change is needed.

3. **Configure the consent screen.**

   Open Google Auth Platform > Branding. If configuration has not started, click Get Started and complete the application name, support email, audience and contact information.

   For testing with a personal Google account, select External as the audience. Complete and save the setup. Existing settings can be reviewed under Branding, Audience and Data Access.

4. **Add your Google account as a test user, where applicable.**

   If the audience is External and the publishing status is Testing, open Audience. Under Test users, click Add users, enter the email address of the Google account you will use to authorize spreadsheet access and save it.

   Use that same Google account during authorization in Section 4.

5. **Configure the spreadsheet scope.**

   Open Data Access > Add or remove scopes and select `https://www.googleapis.com/auth/spreadsheets`. If it is not listed, use the manual scope-entry option. Apply and save the selection.

   This is the scope requested by the backend's `SCOPES` setting in `config.py`.

6. **Create an OAuth client.**

   Open Google Auth Platform > Clients > Create client. Select Web application as the application type and enter a descriptive name.

   If you already have a Web application OAuth client for this setup, open it instead.

7. **Register the callback URL.**

   Under Authorized redirect URIs, add the callback URL determined in Section 2. Enter it here, not under Authorized JavaScript origins.

   For example, if your backend address is `https://backend.example`, the callback is `https://backend.example/oauth2callback`.

   Replace the example address with your actual backend address, including any deployment-specific URL prefix. The complete callback must exactly match the backend's `OAUTH_REDIRECT_URI` value. Create the client or save your changes.

8. **Download and place the credentials file.**

   Download the OAuth client's JSON file and rename it `client_secret.json`.

   Place it beside `app.py` on the computer or server where the backend will run. If you prepare the files on your computer but run the backend on a server, transfer `client_secret.json` to that server's backend directory.

   Do not use a service-account JSON file. Keep `client_secret.json` out of the published repository and publicly served web directories.

This completes the Google Cloud configuration. In Section 4, you will start the backend and authorize access through your browser. You do not need to create the `tokens` directory manually.

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

Use the same Python environment in which you installed the dependencies. Leave the terminal running the backend open while completing the following steps and executing workflows.

In all URLs below, replace `https://backend.example` with the backend address configured in Section 2, including any deployment-specific URL prefix.

In your web browser, open your backend URL followed by `/health`. For example:

```text
https://backend.example/health
```

The expected response contains:

```json
{"ok": true}
```

In the same browser, open the authorization endpoint:

```text
https://backend.example/authorize?user_id=default
```

This endpoint returns JSON containing an `authorization_url`. It does not redirect you automatically. Copy the complete value of `authorization_url`, without the surrounding quotation marks, into your browser. Sign in with the intended Google account and grant access.

After the callback completes, check:

```text
https://backend.example/auth/status?user_id=default
```

The response should contain `"authorized": true`.

The backend creates the `tokens` directory when saving authorization. Keep `user_id` set to `default` in the supplied workflows unless you deliberately configure another authorization context consistently.

If a workflow stops because Google authorization is missing, complete authorization and manually restart it. Authorization does not automatically resume the stopped workflow.

## 5. Prepare the worklist files

The [worklists directory](worklists/) contains `org.xml` and the three forms used by the workflows.

In `worklists/org.xml`, adjust the subject identity to match the worklist account that will perform the human tasks. In particular, configure the subject's `uid` for that account.

Use the subject's `uid` as your username in the CPEE worklist interface. This worklist identity is separate from the backend's `user_id` argument, whose supplied value `default` identifies the saved Google authorization context.

Host `org.xml` and the HTML files at URLs accessible to the worklist service and the browser displaying the tasks.

The forms are:

- `define_price_list.html`: provide a new price-list name.
- `correct_vendor_information.html`: provide missing vendor information.
- `personal_car_decision.html`: accept or reject personal-car use.

Starting `app.py` does not make `org.xml` or the HTML forms available through web URLs. Place these files in a directory served by your web server, which may differ from the backend directory. The same server can host both the backend and these files.

The public URLs depend on your web server's configuration. A filesystem path alone does not establish a working URL. Before configuring the workflow arguments in Section 6, open the public URL of `org.xml` and each form in a browser. Confirm that they return the expected XML or HTML content rather than a “Not Found” page or a login page. The URLs must also be accessible to the worklist service. A GitHub file-view page does not serve the form itself.

Publish only the organizational model and forms in this directory. Keep backend configuration containing API keys, `client_secret.json` and generated token files outside publicly served directories.

## 6. Import and configure the workflows

The workflow files are:

- [Thesis_Workflow_Spreadsheet_Order_Filtering.xml](workflows/Thesis_Workflow_Spreadsheet_Order_Filtering.xml)
- [Thesis_Workflow_Invoice_Registration.xml](workflows/Thesis_Workflow_Invoice_Registration.xml)
- [Thesis_Workflow_Vendor_Onboarding_and_Ticket_Processing.xml](workflows/Thesis_Workflow_Vendor_Onboarding_and_Ticket_Processing.xml)
- [Thesis_Workflow_Travel_Authorization_Request_Processing.xml](workflows/Thesis_Workflow_Travel_Authorization_Request_Processing.xml)

These XML files are already included in the `workflows` directory of your cloned or extracted repository. No separate download is required.

Open the [CPEE interface](https://cpee.org/flow/) and create a new instance. Use the `load testset` control to select the downloaded workflow XML file. This loads its data objects, endpoints and process model together.

Before starting it, make the following changes. These can be made manually in CPEE or in a local copy of the XML before importing it.

If you edit a local XML file after importing it, load the updated file into a fresh CPEE instance and check the scenario inputs in Section 7 before starting it. Uploading the XML to your backend server does not update the model already loaded in CPEE.

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

Replace every `BACKEND_API_KEY` placeholder in the `api_key` arguments with the backend API key configured in Section 2.

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
- In the repeated task, enter two spaces, followed by `Corrected Price List`, followed by two spaces and submit.

For I3, the first response causes another user-task invocation. The second response is trimmed and `Corrected Price List` is stored and added once to the price lists.

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

Both acceptance and rejection of personal-car use are recorded and processing continues to `Submitted`. Rejection of personal-car use does not reject the entire travel request.

## 8. Execute and inspect the results

After configuring the deployment settings and scenario inputs:

1. Start the workflow in CPEE.
2. For scenarios requiring human participation, open the [CPEE worklist interface](https://cpee.org/worklist/) and sign in using the account whose identity you configured in `org.xml`.
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
