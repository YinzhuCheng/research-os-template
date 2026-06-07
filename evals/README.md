# Research OS Local Evals

These fixtures validate harness behavior without paid APIs, network calls, real
uploads, or external writeback.

Current fixture categories:

- `schema_regression_case`: strict schema and trailing HTML checks.
- `privacy_leak_case`: sentinel raw intake text must stay out of `CONTROL/`,
  `PUBLIC/`, and API responses.
- `failed_experiment_replay`: preserves failed/partial states instead of
  inferring success from files alone.
