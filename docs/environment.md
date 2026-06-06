# Environment Requirements

This repository is intentionally lightweight. Normal operation needs a shell, Git, Python, and a browser. Codex app integration is optional but recommended for the browser copilot workflow.

Operating-system package names and install commands change over time. The scripts below document the expected environment and include conservative checks, but you may need to adjust package manager commands for your OS version, enterprise image, proxy, or permission model.

## Required For Normal Local Use

- Git 2.40 or newer.
- PowerShell 5.1 on Windows, or PowerShell 7+ on macOS/Linux if you want to run the `.ps1` scripts there.
- Python 3.10 or newer.
- A modern browser for `PUBLIC/index.html` and `PUBLIC/copilot.html`.
- Local filesystem access to the repository root.

## Recommended For Codex App Use

- Codex desktop app with this repository opened as a trusted workspace.
- The repo-scoped skills under `.agents/skills/`.
- The repo-scoped plugin marketplace at `.agents/plugins/marketplace.json` if you want to install the Research OS Copilot plugin.
- Network access only when refreshing live evidence or downloading open-access references.

## Optional Capabilities

- LaTeX distribution such as TeX Live or MiKTeX, only when `dissemination.paper_enabled: true`.
- Node.js, only for external frontend tooling or browser QA outside Codex. The built-in copilot bridge uses Python standard library only.
- `winget`, Homebrew, or `apt`, only if you want the install script to try installing missing system tools.

## Install And Check

Windows PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_environment.ps1
```

Attempt package-manager installs on Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_environment.ps1 -InstallMissing
```

Run checks and standard validation:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_environment.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_schemas.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_skills.ps1
```

Start the local browser copilot bridge:

```powershell
python .agents/plugins/plugins/research-os-copilot/scripts/research_os_copilot_server.py --serve
```

Then open:

- `http://127.0.0.1:8765/`
- `http://127.0.0.1:8765/index.html`

## OS Notes

- Windows 10/11: `winget` is the default install path in `install_environment.ps1`. Older images may need Microsoft Store App Installer, Chocolatey, or manual installers.
- macOS: use PowerShell 7 (`pwsh`) plus Homebrew or manual installers. The script can check tools but does not assume Homebrew is present.
- Ubuntu/Debian: use PowerShell 7 (`pwsh`) plus `apt` or your system package manager. Package names can vary by release.
- Corporate or cloud machines may block package managers, script execution, localhost ports, or browser access. In that case install Git/Python manually and rerun `check_environment.ps1`.

## Privacy And Cost

- Do not put API keys, tokens, cookies, SSH keys, or authorization headers in repo files.
- Runtime uploads belong under `PRIVATE/` and are excluded from git.
- Reference downloads are best-effort open-access or landing-page attempts; the script does not bypass paywalls.
- Paid resources, cloud, external writeback, public export, and submission require human confirmation.
