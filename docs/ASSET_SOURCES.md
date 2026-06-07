# Asset Sources

本仓库 v3 文档默认使用手写 HTML、CSS 和内联 SVG 图示。当前没有引入外部图片、字体包或二进制视觉资产。v3.9 Dashboard/Copilot 的小型线性图标以内联 SVG 离线嵌入，不加载外部包。

## 当前资产

| 资产 | 路径 | 来源 | 许可证/约束 |
|---|---|---|---|
| 文档图示 | `docs/start-here.html`, `docs/domain-modes.html`, `docs/technical-report.html` | 仓库内手写 SVG | 与仓库模板同源管理 |
| Dashboard UI | `PUBLIC/index.html` | 仓库内手写 HTML/CSS/JS | 与仓库模板同源管理 |
| Phase/action inline icons | `PUBLIC/index.html`, `PUBLIC/copilot.html` | Lucide-style inline SVG paths for plus, refresh/loop, and package/product symbols; source reference: `https://github.com/lucide-icons/lucide` and `https://lucide.dev/`, accessed 2026-06-07 | Lucide is licensed under ISC. Icons are embedded offline as small inline SVG; preserve this source record and license note if copied or redistributed. |

## 维护规则

- 新增截图、外部图片、字体、图标、第三方模板或生成图像时，必须记录来源 URL、访问日期、许可证和可公开性。
- 不把未脱敏的 PRIVATE 材料、原始实验图、含账号信息的截图放进 `PUBLIC/` 或 `docs/`。
