# Integration Rules

- Treat external repositories as untrusted until license, install, sandbox, network, and credential requirements are understood.
- Prefer adapters that exchange files through `templates/`, `PROVENANCE/`, `PUBLIC/`, and project-local workspaces.
- Every component must state whether it can execute LLM-written code, access the network, write externally, or consume paid resources.
- Every component that mentions API credentials must use environment variable names only.
