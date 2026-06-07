import { invoke } from "@tauri-apps/api/core";

type DialogPath = string | { path?: string; file?: string } | null | undefined;

function normalizeDialogPath(value: DialogPath): string | null {
  if (!value) return null;
  if (typeof value === "string") return value;
  return value.path ?? value.file ?? null;
}

function ensureRosproj(path: string): string {
  return path.toLowerCase().endsWith(".rosproj") ? path : `${path}.rosproj`;
}

async function invokeDialog<T>(command: string, options: Record<string, unknown>): Promise<T | null> {
  return invoke<T | null>(command, { options });
}

export async function selectExistingRosproj(): Promise<string | null> {
  const selected = await invokeDialog<DialogPath>("plugin:dialog|open", {
    title: "打开 Research OS 项目",
    multiple: false,
    directory: false,
    filters: [{ name: "Research OS Project", extensions: ["rosproj"] }],
  });
  return normalizeDialogPath(selected);
}

export async function chooseRosprojSavePath(defaultPath: string): Promise<string | null> {
  const selected = await invokeDialog<DialogPath>("plugin:dialog|save", {
    title: "创建 Research OS 项目",
    defaultPath,
    filters: [{ name: "Research OS Project", extensions: ["rosproj"] }],
  });
  const normalized = normalizeDialogPath(selected);
  return normalized ? ensureRosproj(normalized) : null;
}
