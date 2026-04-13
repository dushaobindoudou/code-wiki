# Production Readiness

## 结论（当前）

当前仓库可定义为：**文档与 Skill 规范的正式态（Docs/Skill GA）**，不是独立应用二进制发布态。

这意味着：
- 对外可稳定提供 `init / ingest / query / lint / schema / visualize` 的 Skill 规范与命令文档
- 对内有明确结构、规则与发布门禁脚本
- 变更可以通过自动化流程做持续健康检查

## 正式态门禁标准

发布前必须满足：

1. **核心文件完整**
   - `README.md`
   - `README_CN.md`
   - `AGENT.md`
   - `CLAUDE.md`
   - 各子 Skill `SKILL.md`

2. **关键能力可见**
   - README 中可见核心命令
   - 主 Skill 路由映射完整

3. **自动化检查通过**
   - 本地执行：`bash tools/qa/release-gate.sh`
   - CI 执行：`.github/workflows/release-gate.yml`

## 本地验证命令

```bash
bash tools/qa/release-gate.sh
```

通过即代表当前提交满足“正式态门禁”。

## 说明

- 若未来加入可执行代码（CLI/服务），应新增代码级测试（单测、集成测试、E2E）并升级本文件标准。
