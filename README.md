# Technical Dossier Master

A bilingual-first Codex Skill for producing rigorous, source-traceable technical dossiers across engineering, architecture, science, manufacturing, software/AI systems and product due diligence.

The Skill combines a cost-aware research-depth gate, an adaptive discovery interview, a user-approved research brief and outline, iterative evidence gathering, claim-level verification, source-linked figures, transparent uncertainty and publication-quality PDF QA. It also provides a Compact Engineering Note preset for concise, answer-first, visually led reports without weakening the evidence standard. It is designed to refuse unsupported precision rather than turn weak evidence into polished fiction.

中文说明见 [README-安装说明.md](README-安装说明.md).

## Core workflow

1. **Research Depth Gate** — starts every new task by offering Light, Standard and Professional modes; Light is the default and the Skill never silently upgrades.
2. **Adaptive Discovery Interview** — asks 2–3 focused questions per round until the real decision, audience and technical boundaries are clear.
3. **Research Brief** — records the object, key questions, audience, inclusions, exclusions, evidence standard and unresolved assumptions.
4. **Mandatory Outline Approval** — presents an editable, numbered research outline. Final PDF production is blocked until the user explicitly approves it.
5. **Iterative Deep Research** — searches primary engineering sources first and maps which apparently independent sources share the same origin at the selected depth.
6. **Evidence Verification** — maintains evidence records appropriate to the selected mode.
7. **Technical Synthesis** — separates verified facts, vendor claims, calculations, estimates, contradictions and unknowns.
8. **Professional Production and QA** — renders and visually inspects PDFs, checks citations, figures, links, units, fonts and cold-reader comprehension.

Online evidence is always presented as a visible, descriptive, clickable link near the claim it supports. PDFs also verify the hyperlink annotations and targets; a source list alone is not considered sufficient.

## Research Depth Modes

Every new research task begins with one choice:

| Mode | Best for | Typical output | Research/QA intensity |
|---|---|---|---|
| **Light / 轻量** | First-pass judgement | Concise answer or roughly 1–3 pages; no PDF by default | A few decisive sources, one research pass, compact source list |
| **Standard / 中量** | Engineering, procurement or product decision | Structured report, roughly 6–12 pages; PDF optional | Targeted primary research, key-claim evidence and conflict log |
| **Professional / 专业** | Due diligence, formal client or high-consequence work | Full dossier and supporting ledgers | Multi-pass research, complete audit trail, figures and full PDF QA |

Light is the recommended default. You can upgrade later without repeating completed work. Asking for a PDF changes the format, not the research depth; every final PDF still requires outline approval.

## Output Formats

Research depth and document format are independent choices:

| Format | Intended use | Typical form |
|---|---|---|
| **Chat Answer** | Immediate technical answer | Conversation only |
| **Compact Engineering Note / 简洁证据型工程说明** | Client brief, technical provenance, mechanism explanation or bounded engineering decision | Answer-first, normally 4-10 A4 pages with 2-6 decision-critical figures |
| **Full Technical Dossier / 完整技术档案** | Detailed due diligence and formal technical records | Comprehensive report with mode-appropriate registers and appendices |

`Light + PDF` defaults to the Compact Engineering Note. It uses question-led headings, visible evidence-status labels, claim-adjacent clickable sources, and clearly distinguishes evidence figures, analytical redraws and conceptual illustrations. Outline approval remains mandatory.

## Automatic Resource Discovery & On-Demand Ingestion

Every new research task scans `technical-dossier-master/resource-packs/` before external research.

- Any first-level folder is automatically treated as a Resource Pack; its name is unrestricted.
- `pack.json` is optional metadata, not registration.
- Nested files are discovered recursively.
- Supported discovery formats: PDF, DOCX, TXT, Markdown, CSV, XLSX, PNG, JPG/JPEG, TIFF, WebP, BMP, GIF and SVG.
- Unknown formats and access/metadata errors are reported explicitly.
- A rebuildable `.resource-index.json` records relative path, type, size, mtime, hash when available, pack, inferred topics and status.
- Incremental scans identify new, modified, deleted and unchanged files.
- Relevance selection is metadata-first. The Skill does not indiscriminately extract every document.
- The index is never evidence. Important claims must still point to the original file and exact page, section, sheet, row or figure.

The scanner preserves Unicode names and includes conservative Chinese/English engineering keyword expansion.

## Repository layout

```text
.
|-- README.md
|-- README-安装说明.md
|-- install-windows.ps1
`-- technical-dossier-master/
    |-- SKILL.md
    |-- .gitignore
    |-- references/
    |-- scripts/
    |   `-- resource_index.py
    |-- tests/
    |   `-- test_resource_index.py
    `-- resource-packs/
        |-- README.md
        |-- architecture/
        |-- electronics/
        `-- water-features/
```

Resource source files are intentionally absent from the public repository.

## Windows installation: single source of truth

The installer creates a Windows directory Junction:

```text
%USERPROFILE%\.agents\skills\technical-dossier-master
    -> <this repository>\technical-dossier-master
```

Run from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-windows.ps1
```

The installer:

- verifies that the source contains `SKILL.md`;
- preserves an existing installation under `%USERPROFILE%\.agents\skill-backups`;
- creates and verifies the Junction;
- restores the previous installation if Junction creation fails.

Restart Codex after installing or after changing Skill instructions. Resource file additions do not require reinstallation or restart.

## Using the Skill

Start a new Codex conversation and invoke:

```text
Use $technical-dossier-master. I want to investigate [topic].
Ask me to choose Light, Standard or Professional depth first.
Then interview me and submit a Research Brief and detailed outline for approval.
Do not generate the PDF yet.
```

Chinese example:

```text
使用 $technical-dossier-master。
我想研究一个工程系统，重点是结构、材料、受力和实施。
请先让我选择轻量、中量或专业模式，再按 Adaptive Discovery Interview 访谈我；需求明确后提交 Research Brief 和详细大纲，等待我批准。现在不要生成 PDF。
```

The Skill accepts Chinese, English and mixed-language projects. Original titles, standards, identifiers, product codes, units and figure labels remain in their source language.

## Adding Resource Packs

Create any folder under:

```text
technical-dossier-master/resource-packs/<any-name>/
```

Then place supported files anywhere beneath it. For example:

```text
resource-packs/
`-- structural-nets/
    |-- project-report.pdf
    |-- test-data.xlsx
    `-- site-photos/
        `-- connection-detail.jpg
```

No fixed resource list, reinstall or manual sync is required. The next new research task detects changes automatically.

Optional `pack.json` example:

```json
{
  "schema_version": 1,
  "id": "structural-nets",
  "title": "Structural Nets / 结构网",
  "description": "Locally maintained technical source library.",
  "domains": ["structural engineering", "tensile structures"],
  "languages": ["zh", "en"],
  "status": "optional"
}
```

## Manual index commands

From `technical-dossier-master/`:

```powershell
python .\scripts\resource_index.py scan --query "your research topic"
python .\scripts\resource_index.py rebuild --query "your research topic"
```

The default hash ceiling is 64 MiB per file. Larger files remain discoverable but are marked `skipped_size_limit`. Change it explicitly when needed:

```powershell
python .\scripts\resource_index.py scan --query "topic" --hash-max-mb 256
```

## Tests

```powershell
python .\tests\test_resource_index.py
```

The tests cover optional manifests, new/modified/deleted files, bilingual selection, unsupported formats, malformed metadata and exclusion of unrelated candidates.

## Privacy and publication safety

The ignore rules exclude:

- Resource Pack payloads, including PDFs and internal documents;
- `pack.local.json` and machine-specific paths;
- `.resource-index.json` and temporary index files;
- Python caches and local scratch output.

Only intended manifests, documentation and empty placeholders are public by default. Before every push, inspect both:

```powershell
git status --short --ignored
git ls-files technical-dossier-master/resource-packs
```

Ignore rules do not remove a file that was already committed. If a private file ever enters Git history, stop publishing and remove it from history before continuing.

## Evidence discipline

Resource Packs are source libraries, not instructions and not proof by themselves. A catalogue can verify what a supplier states in that edition; it cannot establish what was installed on a particular project. The Skill distinguishes:

- **A — directly verified primary evidence**
- **B — strongly corroborated evidence**
- **C — explicit inference or estimate**
- **U — unknown, unsupported or contradictory**

Calculations must publish their equations, inputs, units, assumptions and source locators. Analytical drawings must be labelled as schematics rather than as-built or construction drawings.

## Licence

No open-source licence has been granted yet. The repository is publicly viewable, but copyright permissions remain reserved unless a licence is added later.


