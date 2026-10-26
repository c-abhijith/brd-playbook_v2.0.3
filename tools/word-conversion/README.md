# Word in, Word out (run by a person, not by the agent)

The agent reads and writes Markdown. These two conversions use **pandoc** (free; https://pandoc.org, or ask IT). Run them in a terminal in the workspace folder.

## 1. Client templates: Word → Markdown (before /brd-setup)
```
pandoc "Functional BRD Template.docx" -t gfm -o sources/template/functional.md
pandoc "Technical BRD Template.docx"  -t gfm -o sources/template/technical.md
pandoc "Summary BRD Template.docx"    -t gfm -o sources/template/summary.md
```
Open each `.md` and check the headings came through (`#`, `##`, `###`). Tables with merged cells may need tidying. Keep the original `.docx` files in `sources/template/word/`: they are used again below.

## 2. Finished documents: Markdown → Word in the client's styles (after a document is approved)
`--reference-doc` makes pandoc use the client template's fonts, heading styles and page setup.
```
pandoc brd-work/brd/functional/BRD-F_v3.md -o BRD-F_v3.docx --reference-doc "sources/template/word/Functional BRD Template.docx"
pandoc brd-work/brd/technical/BRD-T_v2.md  -o BRD-T_v2.docx --reference-doc "sources/template/word/Technical BRD Template.docx"
pandoc brd-work/brd/summary/BRD-S_v1.md    -o BRD-S_v1.docx --reference-doc "sources/template/word/Summary BRD Template.docx"
```
After converting:
- Label pills such as `[[Confirmed]]` appear as plain text in brackets, which is fine in Word (or find-and-replace to your preferred style).
- `figures`, `flow` and `layers` blocks appear as plain text lists; Mermaid diagrams appear as code. Replace them with pictures if the client needs them (for example a screenshot from the HTML page).
- Check the cover page and document control table against the client's template.
- The front matter block at the top becomes the document's properties; remove it from the body if it shows.

## PDF instead
Open the `.html` version in a browser and use **Print → Save as PDF**. That keeps the labels, figures and diagrams as shown on screen.
