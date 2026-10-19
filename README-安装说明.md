# Technical Dossier Master v2.4.0 — Compact Engineering Note Edition

## Install on Windows / Codex Desktop
1. Keep this project at its intended long-term location; it becomes the single source of truth.
2. In File Explorer, navigate to this project directory and type `powershell` in the address bar.
3. Run: `powershell -NoProfile -ExecutionPolicy Bypass -File .\install-windows.ps1`
4. Restart Codex and start a new chat; test with `$technical-dossier-master`.

## Add knowledge resources / 添加资源
Maintain resources only in `<仓库路径>\technical-dossier-master\resource-packs`. The installed user-level path is a Junction to this source. Do not move or delete the cloned repository while the Junction is active.

Create any folder below `resource-packs` or use an existing pack, then add supported files anywhere inside it. `pack.json` is optional. The next research task scans changes automatically. Keep machine-specific paths and local overrides out of public manifests.

## GitHub publication
Publish the `technical-dossier-master/` directory, plus documentation and installer if desired. `.gitignore` excludes resource payloads, `pack.local.json` and `.resource-index.json`. Before pushing, verify using `git status` and `git ls-files`, especially if files had already been tracked (ignore rules don't untrack existing files). Respect copyrights and private data.

## Note
Editing this F-drive project immediately updates the files visible through `$HOME\.agents\skills\technical-dossier-master`; do not reinstall after ordinary edits. Restart Codex after changing `SKILL.md` or other Skill instructions. Adding, modifying or deleting Resource Pack files requires no restart: the next task-start scan detects it. The installer preserves prior installations outside the Skill search directory before creating the Junction.

## 研究深度 / Research depth

每个新研究任务会先询问：轻量、 中量或专业。轻量是默认和推荐起点；Skill 不会静默升级。只要求生成 PDF 不代表自动切换到专业模式，但所有最终 PDF 仍需先批准大纲并完成渲染检查。

## 输出形式 / Output format

研究深度与文档形式彼此独立：

- **Chat Answer**：直接在对话中回答。
- **Compact Engineering Note / 简洁证据型工程说明**：结论先行、每页解决一个主要技术问题，通常为 4-10 页 A4、2-6 张关键图。轻量研究要求 PDF 时默认使用此形式。
- **Full Technical Dossier / 完整技术档案**：完整技术档案及与研究深度匹配的台账和附录。

简洁工程说明仍然必须完成大纲审批、证据分级、可点击来源和最终 PDF 渲染检查。简洁不等于降低证据标准。


