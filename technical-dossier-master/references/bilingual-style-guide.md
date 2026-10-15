# Bilingual working standard / 双语工作规范

## Language detection / 语言判断
- Take the latest user message as the primary language cue. Chinese, English, and code-switched replies are equally valid.
- At discovery, ask the output preference only when it will affect deliverables: **中文主体（英文术语） / English / 中英双语**. If user has already specified it, do not ask again.
- Never force the user to repeat technical input in the other language. Translate internally while protecting original technical meaning.

## Technical lexicon / 专业术语
Maintain a glossary for each dossier with `Original term | 中文 | English | Acronym | Definition | Source/standard | Translation confidence`. Explain ambiguous translations and jurisdiction-specific terminology.
Original source names, standards, brands, part numbers, units, formulas, and diagram legends remain unchanged; annotate them bilingually if needed.

## Document modes / 文件语言模式
- **ZH:** Chinese explanation with English technical terminology on first mention and bilingual glossary.
- **EN:** English technical prose using consistent British English unless otherwise requested; Chinese names retained when traceable to original Chinese-language sources.
- **BI:** bilingual headings, abstract, glossary, figure captions and core conclusions. Detailed paragraphs may be written in one selected primary language with the other language summaries to avoid duplicating length unless full parallel text is requested.
- All modes include bilingual metadata/source titles where this materially aids retrieval.

## Quality review / 翻译与排版检查
- Review dangerous near-synonyms: design load vs ultimate load, mass vs weight, flow rate vs velocity, proof/test vs certification, nominal vs maximum, temporary works vs permanent works.
- Check unit conversions, qualifiers, tolerances, load cases, model numbers, page citations and dates in both languages.
- Ensure CJK glyphs render correctly, English and Chinese type remain readable, and the bilingual presentation does not crowd drawings.
- When a translation is uncertain, preserve the original and mark **暂译 / provisional translation**, not a fabricated standard term.
