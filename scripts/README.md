# scripts 区

此目录保存确定性辅助脚本：

- schema 校验。
- 隐私扫描。
- 公开导出。
- hash/manifest 工具。
- dashboard 静态检查。
- LaTeX/图表 QA。

Windows 默认执行策略可能禁止直接运行 `.ps1`。验证时使用：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_schemas.ps1
```

仪表盘静态检查：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_dashboard.ps1
```

LaTeX 源码静态检查：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_latex_sources.ps1
```

Research OS v2 检查：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_research_neutrality.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_harness.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_resource_guard.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_live_evidence.ps1
```

如系统 `python` 不可用，可显式传入可用 Python 运行时来编译 hooks：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_harness.ps1 -PythonPath "C:\path\to\python.exe"
```

Skill 结构检查：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_skills.ps1
```

Research OS v3 文档、集成和 skill 镜像检查：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\sync_skill_mirror.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_skill_mirror.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_integrations.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_html_docs.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_docs_links.ps1
```
