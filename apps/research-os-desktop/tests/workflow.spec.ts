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
  question: "下一步优先建立什么？",
  recommended_option: "balanced",
  why_recommended: "均衡路径最适合当前不确定的早期研究。",
  options: [
    { id: "balanced", label: "均衡启动", description: "同时建立目标、证据和验证路径。", is_recommended: true },
    { id: "evidence_first", label: "证据优先", description: "先梳理文献和事实。" },
  ],
  free_form_enabled: true,
  free_form_label: "自然语言补充",
  free_form_placeholder: "补充研究偏好",
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
      return json({ cursor: 1, events: [{ event_id: "ev-1", type: "assistant_message", message: "已完成证据草图，等待研究者验收。" }] });
    }
    if (path === "/api/approvals") {
      return json({
        approvals: [
          {
            approval_id: "APR-1",
            method: "shell_command",
            risk: { risk: "medium", decision: "requires_confirmation", reason: "本地命令需要研究者确认。" },
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

test("desktop project workflow is clickable and readable", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "研究项目工作台" })).toBeVisible();
  await page.getByRole("button", { name: /选择保存位置/ }).click();
  await expect(page.getByText(/当前不是 Tauri 桌面运行环境/)).toBeVisible();
  await page.getByRole("button", { name: /创建项目/ }).click();
  await expect(page.getByRole("heading", { name: "材料与目标" })).toBeVisible();
  await expect(page.getByText("阶段：半自动循环研究阶段")).toBeVisible();
  await expect(page.getByText("内部：验收门")).toBeVisible();

  await page.getByLabel("研究材料、目标、草稿或链接").fill("这是一段桌面端研究材料。");
  await page.getByRole("button", { name: /保存材料并初始化/ }).click();
  await page.getByLabel("自然语言补充").fill("保留软件产物目标。");
  await page.getByRole("button", { name: /保存选择/ }).click();

  await expect(page.getByRole("heading", { name: "论文投稿工作流" })).toBeVisible();
  await expect(page.getByText("Neural Networks", { exact: true })).toBeVisible();
  await expect(page.getByText("来源真实性核查")).toBeVisible();
  await page.getByLabel("记录新的 app 或工作流不足").fill("来源核查表需要逐条验收。");
  await page.getByRole("button", { name: /记录缺口/ }).click();

  await page.getByRole("button", { name: /进入最终产物/ }).click();
  await expect(page.getByRole("dialog", { name: "进入最终产物阶段" })).toBeVisible();
  await page.getByLabel("关闭最终产物选择").click();
  await expect(page.getByRole("dialog", { name: "进入最终产物阶段" })).toHaveCount(0);

  await page.getByRole("button", { name: /进入最终产物/ }).click();
  await page.getByRole("dialog", { name: "进入最终产物阶段" }).getByLabel(/论文/).check();
  await page.getByLabel("自然语言目标调整").fill("论文目标为 Neural Networks Full Article。");
  await page.getByRole("button", { name: /确认进入/ }).click();

  await expect(page.getByText("Codex 输出")).toBeVisible();
  await expect(page.getByText("已完成证据草图，等待研究者验收。", { exact: true })).toBeVisible();
  await expect(page.getByText("shell_command")).toBeVisible();
  await expect(page.getByText("python -m pytest tests")).toBeVisible();
  await expect(page.getByText("1 个待存档变更")).toBeVisible();
  await page.getByRole("button", { name: /刷新预览/ }).click();
  const html = await page.content();
  expect(html).not.toContain(String.fromCharCode(0x942e));
  expect(html).not.toContain(String.fromCharCode(0x9352));
  expect(html).not.toContain(String.fromCharCode(0x7ecb));
  expect(html).not.toContain(String.fromCharCode(0xfffd));
});
