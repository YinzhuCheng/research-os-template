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

Skill 结构检查：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_skills.ps1
```
