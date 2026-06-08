import { expect, test } from "@playwright/test";

const project = {
  schema_version: "research-os-project-v1",
  project_id: "demo",
  name: "Demo Research Project",
  project_file: "D:/ResearchOSProjects/demo.rosproj",
  project_root: "D:/ResearchOSProjects/demo",
  current_macro_phase: "loop",
  current_phase: "loop_acceptance_gate",
  default_profile_id: "custom-openai-compatible",
  codex: { thread_id: null, last_turn_id: null, last_status: "not_started" },
};

const choicePrompt = {
  prompt_id: "CP-TEST",
  stage: "initialization_intake",
  question: "What should be established before the next research loop?",
  recommended_option: "balanced",
  why_recommended: "The balanced route best fits an uncertain early-stage research project.",
  options: [
    { id: "balanced", label: "Balanced start", description: "Build goals, evidence, and validation path together.", is_recommended: true },
    { id: "evidence_first", label: "Evidence first", description: "Organize literature and facts before execution." },
  ],
  free_form_enabled: true,
  free_form_label: "Natural-language additions",
  free_form_placeholder: "Add research preferences",
};

const submissionWorkflow = {
  target_venue: "Neural Networks",
  article_type: "Full Article",
  target_section: "Mathematical and Computational Analysis",
  source_verification: [
    { id: "SRC-GUIDE", label: "Neural Networks Guide for Authors", status: "needs_online_refresh", required_evidence: "official guide URL" },
  ],
  proof_audit: [
    { id: "PROOF-GATES", label: "Gate constructions", status: "needs_review" },
  ],
  review_rounds: [],
  workflow_gaps: [],
};

test.beforeEach(async ({ page }) => {
  await page.route("http://127.0.0.1:8789/**", async (route) => {
    const url = new URL(route.request().url());
    const path = url.pathname;
    const json = (body: unknown) => route.fulfill({ contentType: "application/json", body: JSON.stringify(body) });
    if (path === "/health") return json({ ok: true, service: "research-os-sidecar", runtime: { codex_sdk_available: false } });
    if (path === "/api/projects/current") return json({ project: null });
    if (path === "/api/projects/create") return json({ project });
    if (path === "/api/profiles") return json({ profiles: [] });
    if (path === "/api/runtime/environment") return json({ codex_cli: null, codex_sdk_available: false, adapter: "mock" });
    if (path === "/api/runtime/events") {
      return json({ cursor: 1, events: [{ event_id: "ev-1", type: "assistant_message", message: "Evidence sketch completed; waiting for researcher acceptance." }] });
    }
    if (path === "/api/approvals") {
      return json({
        approvals: [
          {
            approval_id: "APR-1",
            method: "shell_command",
            risk: { risk: "medium", decision: "requires_confirmation", reason: "Local command requires researcher confirmation." },
            params: { command: "python -m pytest tests", cwd: "D:/ResearchOSProjects/demo" },
            created_at: "2026-06-07T22:00:00+08:00",
            status: "pending",
          },
        ],
      });
    }
    if (path === "/api/archive-preview") return json({ phase: "loop_acceptance_gate", macro_phase: "research_loop", dirty: true, changed_paths: ["PUBLIC/research_state.json"], secrets_scan: "passed" });
    if (path === "/api/archives") return json({ archives: [] });
    if (path === "/api/intake") return json({ ok: true });
    if (path === "/api/choice-response") return json({ response: { response_id: "CR-1" } });
    if (path === "/api/final-products") return json({ plan: { product_plan_id: "FP-1" } });
    if (path === "/api/workflow-gap") return json({ gap: { gap_id: "GAP-1", status: "recorded" } });
    if (path === "/api/state") {
      return json({
        project,
        research_state: { schema_version: "research-state-v1", status: "ready", submission_workflow: submissionWorkflow },
        submission_workflow: submissionWorkflow,
        choice_prompts: [choicePrompt],
        run_monitor: { runs: [] },
        archive_index: { archives: [] },
      });
    }
    return json({ ok: false, error: `unhandled mock route ${path}` });
  });
});

test("desktop project workflow is clickable and readable in English", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Research Project Workbench" })).toBeVisible();
  await page.getByRole("button", { name: /Choose save location/ }).click();
  await expect(page.getByText(/system file picker is unavailable/)).toBeVisible();
  await page.getByRole("button", { name: /Create project/ }).click();
  await expect(page.getByRole("heading", { name: "Materials and Goal" })).toBeVisible();
  await expect(page.getByText("Phase: Research Loop")).toBeVisible();
  await expect(page.getByText("Internal: Acceptance gate")).toBeVisible();

  await page.getByLabel("Research objective, constraints, venue rules, or free-form notes").fill("This is a desktop-side research material note.");
  await page.getByRole("button", { name: /Save goal and initialize/ }).click();
  await page.getByLabel("Natural-language additions").fill("Keep the software target visible.");
  await page.getByRole("button", { name: /Save choice/ }).click();

  await expect(page.getByRole("heading", { name: "Paper Submission Workflow" })).toBeVisible();
  await expect(page.getByText("Neural Networks", { exact: true })).toBeVisible();
  await expect(page.getByText("Source Authenticity", { exact: true })).toBeVisible();
  await page.getByLabel("Record a new app or workflow gap").fill("Source verification needs per-reference acceptance.");
  await page.getByRole("button", { name: /Record gap/ }).click();

  await page.getByRole("button", { name: /Enter Final Product/ }).click();
  await expect(page.getByRole("dialog", { name: "Enter Final Product Phase" })).toBeVisible();
  await page.getByLabel("Close final product selection").click();
  await expect(page.getByRole("dialog", { name: "Enter Final Product Phase" })).toHaveCount(0);

  await page.getByRole("button", { name: /Enter Final Product/ }).click();
  await page.getByRole("dialog", { name: "Enter Final Product Phase" }).getByLabel(/Paper/).check();
  await page.getByLabel("Natural-language target adjustment").fill("Target Neural Networks Full Article.");
  await page.getByRole("button", { name: /Confirm track/ }).click();

  await expect(page.getByText("Codex output")).toBeVisible();
  await expect(page.getByText("Evidence sketch completed; waiting for researcher acceptance.", { exact: true })).toBeVisible();
  await expect(page.getByText("shell_command")).toBeVisible();
  await expect(page.getByText("python -m pytest tests")).toBeVisible();
  await expect(page.getByText("1 changed paths")).toBeVisible();
  await page.getByRole("button", { name: /Refresh preview/ }).click();
  const html = await page.content();
  expect(html).not.toContain(String.fromCharCode(0xfffd));
});
