# Compact Engineering Note / 简洁证据型工程说明

Use this profile when the user wants a concise, visually led, evidence-traceable engineering document. It is an output format, not a weaker evidence standard. Research effort remains governed by the selected Light, Standard or Professional mode.

## Reader promise

The reader should be able to determine within 30 seconds:

1. the principal conclusion;
2. what is directly verified;
3. what is inferred;
4. the most important unresolved point; and
5. the next useful engineering action.

## Recommended scale

- Normally 4-10 A4 portrait pages.
- Normally 2-6 decision-critical figures.
- One principal technical question per page or coherent spread.
- Do not enforce a fixed page count or one-section-per-page rule.
- Prefer a short document with an explicit evidence gap over padded prose.

## Information architecture

Adapt rather than mechanically copy this sequence:

1. **Cover + direct conclusion** - title, scope, evidence cut-off date, one-paragraph answer and the dominant figure.
2. **What is actually confirmed?** - strongest direct evidence and its limits.
3. **How does it work?** - physical, structural, hydraulic, electrical, software or system mechanism as relevant.
4. **What path, force or process is involved?** - analytical diagram or original engineering figure.
5. **What equipment and parameters are public?** - compact table separating project-specific facts from generic product examples.
6. **What comparable technology is transferable?** - bounded comparison, not a vendor catalogue.
7. **What remains unknown and how should it be verified?** - missing drawings, measurements, interviews or tests.
8. **Clickable source index** - concise source list with direct original links and figure credits.

Omit irrelevant pages. A short provenance question may need only four or five pages.

## Heading style

Prefer headings that state either a precise technical question or a defensible conclusion:

- `雾效是否使用了特殊雾化设备？`
- `雾为什么能够短暂悬浮？`
- `公开资料只能确认哪些设备参数？`
- `现有证据仍不能证明什么？`

Avoid vague headings such as `背景`, `分析`, `技术介绍` or `其他` when a more specific question can be written.

## Evidence labels

Use these visible Chinese labels in a Chinese report, with English equivalents when useful:

- **【来源确认】 / Source-confirmed** - an inspected source directly supports the claim.
- **【交叉印证】 / Corroborated** - multiple credible sources independently support the claim.
- **【工程推断】 / Engineering inference** - reasoned interpretation based on stated evidence and assumptions.
- **【尚未确认】 / Unverified** - decisive evidence was not located, was inaccessible or is contradictory.

These display labels complement, rather than replace, the A/B/C/U evidence grades. Do not use colour alone to communicate status. Put the label beside the relevant sentence, table row or figure interpretation.

## Figure roles

Classify every figure as one of the following:

1. **Evidence figure / 证据图** - original photograph, drawing, CFD/FEA result, test plot, patent figure or manufacturer document.
2. **Analytical redraw / 分析重绘** - a faithful redraw used to clarify relationships found in cited evidence.
3. **Conceptual illustration / 概念示意** - an explanatory hypothesis that is not evidence of the actual project.

Every caption must state: figure number; what it shows; owner/author; source and locator or URL; year if known; and figure role. Analytical redraws and conceptual illustrations must carry a conspicuous label such as `分析示意，非施工图 / analytical schematic, not a construction drawing`.

Use images to prove or explain. Do not add decorative images merely to fill space. Never embed a supplied style-reference PDF or its assets in the reusable/public Skill unless the user owns the material and explicitly authorises redistribution.

## Page and typography system

- A4 portrait by default; use landscape only for a technically necessary drawing or table.
- White background, dark text and one restrained blue or blue-green accent.
- Suggested margins: 18-22 mm left/right and 16-20 mm top/bottom.
- Suggested main title: 20-24 pt; page/section title: 15-18 pt.
- Chinese body text must remain at least 9.5 pt; captions and source text at least 8 pt at actual A4 print size.
- Use a Chinese/Latin font combination with reliable embedding and full glyph coverage.
- Use a small running header for project / subject / document type and a footer for evidence cut-off date and page number.
- Use pale table fills only when text contrast remains accessible in print.
- Do not shrink source lines until they become technically unreadable.
- Do not force a new page when it creates large unexplained blank areas.

## Source-link behaviour

- Put descriptive, clickable source links close to the claim or caption they support.
- Keep source IDs compact, but never make the reader decode IDs without a titled source index.
- Link to the original project, manufacturer, journal, patent or official document page, not a search result.
- The final source index must state what each source proves and what it does not prove.
- Verify PDF link annotations and targets during QA.

## Writing rules

- Lead with the answer, then show evidence and limits.
- Use short paragraphs, compact tables and annotated figures.
- Separate project-specific facts from generic technology examples.
- Do not infer installed equipment from visual resemblance alone.
- End each substantive page with an engineering implication only when it follows from the evidence.
- Preserve negative findings. `未找到公开证据` is a useful result when the search boundary is stated.

## Compact-note outline approval

The mandatory outline may itself be compact, but it must still be approved before final PDF production. For each proposed page or section, state:

- the question it resolves;
- expected evidence;
- intended figure; and
- known evidence gap.

Approval of a compact outline does not authorise invented figures or unavailable proprietary data.

