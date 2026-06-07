use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use tauri::Manager;

struct SidecarProcess(Mutex<Option<Child>>);

impl Drop for SidecarProcess {
    fn drop(&mut self) {
        if let Ok(mut child) = self.0.lock() {
            if let Some(process) = child.as_mut() {
                let _ = process.kill();
            }
        }
    }
}

fn repo_root_from_manifest() -> Option<PathBuf> {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest.parent()?.parent()?.parent().map(PathBuf::from)
}

fn sidecar_locations(app: &tauri::App) -> Option<(PathBuf, PathBuf)> {
    if let Ok(resource_dir) = app.path().resource_dir() {
        let packaged_sidecar = resource_dir.join("research-os-sidecar").join("sidecar_server.py");
        let packaged_seed = resource_dir.join("research-os-core");
        if packaged_sidecar.exists() && packaged_seed.exists() {
            return Some((packaged_sidecar, packaged_seed));
        }
    }
    let repo_root = repo_root_from_manifest()?;
    Some((
        repo_root.join("apps").join("research-os-sidecar").join("sidecar_server.py"),
        repo_root,
    ))
}

fn spawn_sidecar(app: &tauri::App) -> Option<Child> {
    let (sidecar, seed_root) = sidecar_locations(app)?;
    if !sidecar.exists() {
        eprintln!("Research OS sidecar script not found: {}", sidecar.display());
        return None;
    }
    let mut candidates = Vec::new();
    if let Ok(path) = std::env::var("RESEARCH_OS_PYTHON") {
        candidates.push(path);
    }
    candidates.push("python".to_string());
    candidates.push("py".to_string());

    for python in candidates {
        match Command::new(&python)
            .arg(&sidecar)
            .arg("--serve")
            .arg("--seed-root")
            .arg(&seed_root)
            .stdin(Stdio::null())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
        {
            Ok(child) => return Some(child),
            Err(error) => eprintln!("Could not start sidecar with {python}: {error}"),
        }
    }
    None
}

#[tauri::command]
fn sidecar_url() -> &'static str {
    "http://127.0.0.1:8789"
}

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .setup(|app| {
            app.manage(SidecarProcess(Mutex::new(spawn_sidecar(app))));
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![sidecar_url])
        .run(tauri::generate_context!())
        .expect("error while running Research OS desktop");
}
