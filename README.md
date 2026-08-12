# Codex Personal Memory Engine

一个可审查的 Codex 个人协作画像 Starter Kit：从自然交互中记录最小必要证据，定期形成可被反驳的候选画像，而不是把一次提问或一句偏好直接变成“人格设定”。

它由三个部件组成：

```text
Hook（采集） -> 私有 inbox（原始事件） -> Skill（归纳） -> 候选画像/审查报告
```

## 为什么不是“自动记住一切”

- 提问不是不懂：只有自我解释、概念辨析、实际判断、项目产物或明确纠正，才能作为认知边界的证据。
- 一次偏好不是长期偏好：新结论先是 `candidate`，需要独立证据与反证审查。
- 先影子运行：默认不让画像改变回答；先审查误判，再决定是否允许轻量个性化。
- 数据本地私有：原始对话和推断出的画像都不属于这个仓库，也不应提交到 Git。

## 仓库内容

| 目录 | 作用 |
| --- | --- |
| `hooks/` | 在 `UserPromptSubmit` 与 `Stop` 事件写入最小化的本地记录 |
| `skill/` | 处理 inbox、形成可追溯候选画像的 Codex Skill |
| `templates/` | 私有运行时目录的空模板、数据 schema 与评测题 |
| `config/` | 采集范围的示例配置 |
| `scripts/` | 本地安装与校验脚本 |

## 安装（本地、可撤销）

1. 克隆仓库后，在其根目录运行：

   ```bash
   ./scripts/install-local.sh
   ```

2. 编辑 `~/.codex/personal-memory/config.json`，把 `workspace_scope` 改成你希望采集的**一个具体工作区绝对路径**。没有这个配置，Hook 会安全地不采集。

3. 重启 Codex，打开 `/hooks` 审查并信任 `UserPromptSubmit` 与 `Stop`。

4. 在 Codex 中正常工作；Hook 只把新消息写进 `~/.codex/personal-memory/private-inbox/`。

5. 需要归纳时，让 Codex 使用 `$personal-memory-engine`。它会生成候选与审查报告；影子模式中不得更新 `active-profile.md`。

运行 `./scripts/verify-install.sh` 可检查配置与数据结构。删除 `~/.codex/hooks.json` 中对应的两项 Hook，并移走 `~/.codex/personal-memory/`，即可停止和移除该系统。

## 隐私与安全

- 不上传 `~/.codex/personal-memory/`；它包含真实对话、证据和个人画像。
- Hook 在写入前对常见 API key、Bearer token、密码/密钥赋值做基础脱敏；这不是完整的秘密扫描器。
- 只对 `workspace_scope` 内的会话工作目录采集。
- Hook 不调用模型、不读取旧 transcript、不修改项目文件，也不向模型返回额外上下文。
- 不推断诊断、敏感属性或广泛人格标签。

## 状态模型

| 状态 | 含义 | 能否改变回答 |
| --- | --- | --- |
| `candidate` | 单条或弱证据形成的待审查结论 | 否 |
| `active_hypothesis` | 至少两条独立证据、无强反证、范围明确 | 仅可轻量调节 |
| `confirmed_principle` | 用户确认或长期高一致性证据 | 可在明确范围内使用 |

## 公开发布检查

公开 fork 或二次开发前，请运行：

```bash
git status --ignored
git check-ignore -v private-inbox/example.jsonl evidence/events.jsonl runtime/active-profile.md
./scripts/verify-install.sh
```

确认仓库中没有真实 JSONL、用户名、绝对私有路径、令牌或个人画像。
