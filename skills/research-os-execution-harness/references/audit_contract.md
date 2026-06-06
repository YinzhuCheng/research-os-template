# Audit Contract

Every execution must have:

- work order ID,
- inputs,
- allowed paths,
- forbidden paths,
- expected outputs,
- acceptance criteria,
- privacy level,
- result status.

Do not silently skip failed checks. If execution is partial, record status as `blocked` or `failed` with errors.
