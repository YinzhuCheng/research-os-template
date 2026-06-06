# 开源组件集成

`components.yaml` 记录 Research OS v3 可参考或可适配的自动研究组件。默认策略是积极集成接口和经验，但不 vendoring 大段第三方源码。

每个组件记录：

- 来源 URL、论文 URL、许可证和访问日期。
- 适合连接的 Research OS 阶段。
- 安装入口或文档入口。
- 需要的环境变量名，不记录真实值。
- 输入、输出和审计产物映射。
- sandbox、成本、隐私、外部写回和许可证风险。

新增组件时先复制 `../../templates/yaml/integration_component.template.yaml`，填完后运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_integrations.ps1
```
