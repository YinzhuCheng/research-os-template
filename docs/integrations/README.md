# Integration Registry

`components.yaml` records open-source systems that Research OS Desktop may reference or adapt. The default policy is to record metadata and adapter boundaries without vendoring large third-party source trees.

Each component record should include:

- Source URL, paper URL when available, license, and access date.
- Research OS stages or product tracks that the component may support.
- Install entry points or documentation links.
- Required environment variable names, without real secret values.
- Input, output, and audit-artifact mappings.
- Sandbox, cost, privacy, external writeback, and license risks.

When adding a component, start from `../../templates/yaml/integration_component.template.yaml`, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_integrations.ps1
```
