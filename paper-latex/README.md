# Elsevier Smart Health LaTeX Template (Project Local)

This folder provides a LaTeX starter aligned with the repository's Word template:

- `paper/word_pipeline/template/elsevier_smart_health_template.docx`

It is prepared for manuscript drafting in this project (PjBL-TPACK-STEM-ESD).

## Files

- `main.tex` - main manuscript entry point
- `preamble.tex` - packages and style settings
- `sections/*.tex` - section placeholders (IMRAD)
- `tables/table_example.tex` - table format example
- `references.bib` - BibTeX placeholder

## Style Notes (mapped from DOCX template)

- Page size: A4
- Margins (approx): left 0.53 in, right 0.53 in, top 1.00 in, bottom 0.58 in
- Body text target: around 9.5 pt equivalent
- Compact heading and paragraph spacing
- Table style: journal style (`booktabs`, compact spacing)

## Build (LaTeX Workshop, VS Code)

This folder is ready for LaTeX Workshop.

- Open `paper-latex` as your VS Code workspace/folder.
- Open `main.tex`.
- Build with command palette: `LaTeX Workshop: Build LaTeX project`.
- Default recipe: `latexmk (pdf)`.
- Auto build on save is enabled in `paper-latex/.vscode/settings.json`.

Alternative recipe available in LaTeX Workshop:

- `pdflatex -> bibtex -> pdflatex*2`

No `make` workflow is required.

## Next Step

After template validation, copy manuscript content section-by-section into
`sections/*.tex`, then connect references in `references.bib`.
