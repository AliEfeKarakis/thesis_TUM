This directory explains how operation reuse was assessed and how the distinct-workflow counts reported in the thesis were obtained.

The analysis covers all 10 implemented spreadsheet operations and the four evaluated workflows:

- Spreadsheet Order Filtering.
- Invoice Registration.
- Vendor Onboarding and Ticket Processing.
- Travel Authorization Request Processing.

The evidence consists of the [workflow models](../../workflows/), the [120 included regular execution logs](../../logs/regular/) and the [backend route definitions](../../routes/sheets_routes.py). The application entry point, [app.py](../../app.py), imports the spreadsheet route module.

Two counts were determined for each operation:

- Modeled workflows: the number of distinct workflow models containing at least one call to the operation.
- Observed workflows: the number of distinct workflows whose included execution logs record at least one call to the operation.

A workflow contributes at most one to each count for an operation. Multiple activities calling the same operation, repeated calls within loops and repeated executions of the same workflow do not increase its distinct-workflow count. An endpoint declaration without an activity calling that endpoint is not counted as modeled use.

Calls in the workflow models and service endpoints recorded in the logs were compared with the backend route definitions. Source inspection examined whether the workflows used shared handlers or separate implementations for individual workflows. Differences in arguments and workflow control logic were distinguished from changes to backend code.

All four workflows used the same backend deployment, whose implementation remained unchanged during the evaluated executions.

Example: updateCell

The `updateCell` operation writes a single value to a specified spreadsheet location.

Its modeled use is:

- Spreadsheet Order Filtering: no call to `updateCell`, contributing 0.
- Invoice Registration: Write Invoice Name (`a9`), Write Invoice Currency (`a10`) and Write Selected Price List (`a16`) call `updateCell`. Together, these activities contribute 1 workflow.
- Vendor Onboarding and Ticket Processing: activities including Write Ticket ID (`a39`) call `updateCell`, contributing 1 workflow.
- Travel Authorization Request Processing: activities including Write Authorization Status Submitted (`a15`) call `updateCell`, contributing 1 workflow.

Therefore:

```text
Modeled workflows using updateCell = 0 + 1 + 1 + 1 = 3
```

The included execution logs record calls to `updateCell` in Invoice Registration, Vendor Onboarding and Ticket Processing, and Travel Authorization Request Processing. No call to this operation appears in the included Spreadsheet Order Filtering executions.

For example, the [I1 run 01 execution log](../../logs/regular/Invoice_Registration/I1_Existing_Price_List/run_01_d331d27f-64b8-49e8-a1b5-d9d622e2b424.xes.yaml) records the invoice activities calling this operation.

Therefore:

```text
Observed workflows using updateCell = 3
```

These are counts of workflows, not counts of activity calls or execution runs.

In the backend source, the `/updateCell` route is handled by `update_cell()`. It receives `spreadsheetId`, `range` and `value` and performs the corresponding Google Sheets update. The three workflows use this shared handler with different argument values. The handler does not contain separate implementations for invoice, vendor or travel processing.

The complete results are listed below. Each pair gives the modeled-workflow count followed by the observed-workflow count:

- `createSpreadsheet`: 4 modeled, 4 observed.
- `createSheet`: 4 modeled, 4 observed.
- `deleteSheet`: 0 modeled, 0 observed.
- `renameResource`: 0 modeled, 0 observed.
- `updateCell`: 3 modeled, 3 observed.
- `updateManyCells`: 4 modeled, 4 observed.
- `appendData`: 4 modeled, 4 observed.
- `readData`: 4 modeled, 4 observed.
- `formatRange`: 4 modeled, 4 observed.
- `resizeDimension`: 4 modeled, 4 observed.

Seven operations were used in all four workflows, and `updateCell` was used in three. Thus, eight operations were used across multiple workflows through shared backend handlers without workflow-specific implementation changes.

The implemented operations `deleteSheet` and `renameResource` were not used by the four workflow models or their included executions. These executions therefore provide no evidence of their reuse.

The counts and source inspection support operation reuse within the evaluated workflows. They do not measure the effort required to add another workflow or establish portability to another application's API.
