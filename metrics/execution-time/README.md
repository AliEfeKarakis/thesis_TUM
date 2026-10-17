This directory documents how the execution-time results reported in the thesis were calculated from the saved CPEE execution logs.

The analysis uses the [regular execution logs](../../logs/regular/).

All 120 included regular executions were eligible for the timing analysis: they satisfied the functional-correctness criteria, ran uninterrupted and contained complete start and finish timestamps. Each of the 12 scenarios contains 10 executions.

The 12 error-handling tests are excluded from these timing summaries. Slow executions were not removed simply because their durations were unusually long.

For each execution, the duration was calculated as:

Execution duration = finish timestamp − start timestamp

The start timestamp is the `time:timestamp` of the `state/change` event with `cpee:state: running`. The finish timestamp is the `time:timestamp` of the `state/change` event with `cpee:state: finished`. Time zone offsets are taken into account when calculating the difference.

The duration is expressed in seconds. It excludes configuration time before the workflow enters the running state. It includes spreadsheet operations, verification reads, external communication and, where applicable, worklist waiting and human interaction.

These values describe the duration of the workflow, not the processing time of the backend alone. Durations of parallel activities are not added together to calculate the workflow duration.

Example:

S1 is the Spreadsheet Order Filtering scenario with mixed order statuses.

The [execution log for S1, run 01](../../logs/regular/Spreadsheet_Order_Filtering/S1_Mixed_Statuses/run_01_bc6c1de1-de78-4cda-b714-9a39de43968c.xes.yaml) contains these state timestamps:

- Running: `2026-10-12T13:08:03.220858+02:00`
- Finished: `2026-10-12T13:08:09.971155+02:00`

Both timestamps have the same date and time zone offset. Subtracting the start timestamp from the finish timestamp gives:

```text
13:08:09.971155 − 13:08:03.220858 = 6.750297 seconds
```

For each scenario, the same execution durations are used to calculate:

- Number of executions (`n`): the number eligible for timing analysis.
- Mean: the sum of the durations divided by `n`.
- Median: the middle duration after sorting; for an even number of executions, the average of the two middle durations.
- Sample standard deviation: subtract the mean from each duration, square these differences, add them together, divide by `n − 1`, and take the square root.

The mean, median and sample standard deviation are expressed in seconds.

The durations of runs 01–10, in run order, are:

```text
6.750297, 6.029603, 6.553605, 8.327036, 7.161023,
6.089350, 5.642508, 6.530522, 7.715375, 5.602406
```

The corresponding logs are available in the [S1 scenario directory](../../logs/regular/Spreadsheet_Order_Filtering/S1_Mixed_Statuses/).

The summaries are calculated as follows:

- Number of executions: `n = 10`.
- Mean: the durations sum to `66.401725` seconds. Dividing by 10 gives `6.6401725` seconds.
- Median: after sorting, the fifth and sixth durations are `6.530522` and `6.553605` seconds. Their average is `6.5420635` seconds.
- Sample standard deviation: the sum of squared differences from the mean is approximately `7.052993` seconds squared. Dividing by 9 and taking the square root gives approximately `0.885249` seconds.

Rounded to three decimal places, these are the values reported in the thesis:

- Mean: `6.640` seconds.
- Median: `6.542` seconds.
- Sample standard deviation: `0.885` seconds.

Calculations use the unrounded durations; rounding is applied to the reported summaries.
