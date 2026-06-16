# Research OS v4.3 Researcher QA Baseline

Timestamp: 2026-06-07T23:16:30.4408131+08:00

## Method

- Ran a mocked sidecar Playwright walkthrough from a researcher perspective.
- Captured desktop and narrow viewport screenshots under the ignored local directory:
  `apps/research-os-desktop/test-results/researcher-qa/baseline/`
- Screenshots were not committed.

## Captured Paths

- `desktop-01-project-center.png`
- `desktop-02-workspace.png`
- `desktop-03-choice-prompt.png`
- `desktop-04-final-product-modal.png`
- `desktop-05-final-product-selected.png`
- `narrow-01-project-center.png`
- `narrow-02-workspace.png`
- `narrow-03-choice-prompt.png`
- `narrow-04-final-product-modal.png`
- `narrow-05-final-product-selected.png`
- `summary.json`

## Baseline Result

- Existing Playwright workflow passed on desktop and narrow viewport.
- The screenshot script reported no browser console errors.
- The screenshot script reported no Unicode replacement character in rendered HTML.
- A corrected mojibake scan found no real desktop source mojibake; the previous large hit count was a PowerShell encoding false positive.

## Researcher-Facing Issues Found

- The project header displays the raw internal macro phase value `loop`; researchers need a Chinese macro-stage label and the internal stage can be secondary.
- The runtime panel renders raw JSON events, which is useful for debugging but not suitable as the primary execution stream.
- The approval panel does not give enough immediate context about the pending command, risk, affected scope, and decision consequence.
- The archive panel uses terse values such as `有`; it should explain whether there are uncommitted changes and what will be captured.
- The project center still depends on typed paths for `.rosproj` create/open; a desktop app should offer native file/folder dialogs with a validated fallback.
- The first-run profile panel is functional but too technical; it needs clearer copy around secret references and model/provider testing.
