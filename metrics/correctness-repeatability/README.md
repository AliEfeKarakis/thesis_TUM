This directory explains how the functional-correctness results and the summary of correct repeated executions reported in the thesis were obtained.

The assessment covers the 120 included regular executions: 12 scenarios with 10 executions per scenario. The 12 error-handling tests are evaluated separately.

The [regular execution logs](../../logs/regular/) contain returned spreadsheet records, activity histories, workflow states and human-task responses where applicable. The [spreadsheet exports](../../spreadsheets/) provide the corresponding generated results.

The reported manual checks compared the recorded results and workflow behavior with the predefined scenario expectations. These checks covered:

- The intended successful result.
- Expected headers and data records.
- The absence of missing or additional records within the tested ranges.
- The required workflow path.
- The sequence and returned responses of human tasks, where applicable.

Reaching a successful final state alone was not sufficient to pass. Formatting, fonts and column widths were excluded. Semantically equivalent numerical representations were accepted, such as 79 and 79.0. String normalization was limited to the behavior required by each scenario.

Each included regular execution belongs to one category:

- Passed (`P`): sufficient evidence confirms that all relevant criteria were met.
- Failed (`F`): evidence shows that at least one criterion was violated.
- Unevaluable (`U`): no violation was established, but the available evidence was insufficient to confirm all relevant criteria.

The total number of included executions is:

```text
N = P + F + U
```

When all included executions are evaluable (`U = 0`), functional correctness is calculated as:

```text
FC = P / N
```

The result is the proportion of included executions that passed. Multiplying it by 100 gives the percentage.

All 120 included regular executions were evaluable and passed:

```text
P = 120
F = 0
U = 0
N = 120

FC = 120 / 120 = 1.00 = 100%
```

Example:

S1 is the Spreadsheet Order Filtering scenario with mixed order statuses. Its predefined requirement is to retain only completed orders.

The expected input contains four orders:

- ORD-001: Completed.
- ORD-002: Pending.
- ORD-003: Completed.
- ORD-004: Cancelled.

The expected Completed Orders output contains the header and the complete records for ORD-001 and ORD-003, in their original order.

The [S1 run 01 execution log](../../logs/regular/Spreadsheet_Order_Filtering/S1_Mixed_Statuses/run_01_bc6c1de1-de78-4cda-b714-9a39de43968c.xes.yaml) provides the following evidence:

- Read Raw Orders (`a6`) returned the expected header and all four input records.
- Verify Completed Orders (`a13`) returned the expected header and the two completed-order records.
- No expected record was missing and no additional record appeared in the returned output.
- The activity history recorded the expected reading and writing activities, and the workflow reached the finished state.
- No human task was invoked, as expected for this scenario.

The returned Completed Orders values were:

```text
Order ID | Customer | Product      | Amount | Status
ORD-001  | Alice    | Laptop Stand | 49.9   | Completed
ORD-003  | Clara    | Mouse        | 29.5   | Completed
```

The comparison covered the full returned records, not only their order IDs or statuses. Together with the workflow evidence, these observations supported classifying the execution as passed.

---

For this evaluation, repeatability means the repetition of correct behavior under the specified scenario conditions.

Each repetition used a new workflow instance with the same configured business data and prescribed human responses for that scenario. Generated spreadsheet IDs could differ. Execution-time variation was analyzed separately.

For scenario `s`:

- `P_s` is the number of passed executions.
- `N_s` is the total number of included executions, including failed or unevaluable executions.

When all included executions in the scenario are evaluable, the proportion of correct repeated executions is:

```text
R_s = P_s / N_s
```

All 10 executions in the [S1 scenario directory](../../logs/regular/Spreadsheet_Order_Filtering/S1_Mixed_Statuses/) passed:

```text
P_S1 = 10
N_S1 = 10

R_S1 = 10 / 10 = 1.00 = 100%
```

The same result was obtained for each of the other 11 scenarios.

This calculation is equivalent to functional correctness for the same scenario because it uses the same executions and pass criteria. Its purpose is to show that the requirements were met repeatedly with the same scenario inputs and specified human responses. Repeated incorrect results would not count as successful repetitions.

These results describe the included executions. They do not extend coverage to untested inputs or establish reproducibility across different deployments or operators. External service conditions and operator delays were not kept constant.
