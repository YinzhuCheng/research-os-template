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
- resource budget reference,
- resource ledger entry when real resources were consumed.

Do not silently skip failed checks. If execution is partial, record status as `blocked` or `failed` with errors.
