# Domain Profiles

Research OS keeps domain knowledge in structured profiles instead of free-form prompt piles.
Each domain has:

- `profile.yaml`: taxonomy anchors, research paradigms, artifacts, quality gates, lifecycle states, and harness boundaries.
- `agents.yaml`: callable agent roles with inputs, outputs, allowed paths, forbidden paths, resource policy, network policy, external-write policy, and public-output policy.

The default project remains research-neutral. A domain profile is activated only when the researcher selects it, or when source material clearly points to that field and the phase gate records that decision.

Current deep profiles:

- [基础数学](fundamental-mathematics/profile.yaml)
- [应用数学](applied-mathematics/profile.yaml)
- [机器学习](machine-learning/profile.yaml)
- [计算机科学](computer-science/profile.yaml)
- [统计学](statistics/profile.yaml)

Validation entrypoints:

- `scripts/check_domain_profiles.ps1`
- `scripts/check_agent_capabilities.ps1`
- `scripts/check_domain_templates.ps1`
- `scripts/check_domain_router.ps1`
