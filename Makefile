ENV := tpack-research
PY := conda run -n $(ENV) python

.PHONY: help merge docx docx-merged docx-id docx-en docx-id-no-toc docx-en-no-toc docx-id-toc docx-en-toc docx-quick

help:
	@printf "Targets:\n"
	@printf "  make merge           Regenerate merged EN+ID markdown\n"
	@printf "  make docx            Build ID DOCX (no TOC, no merge)\n"
	@printf "  make docx-merged     Merge + build ID DOCX (no TOC)\n"
	@printf "  make docx-id         Build ID DOCX (no TOC)\n"
	@printf "  make docx-en         Build EN DOCX (no TOC)\n"
	@printf "  make docx-id-no-toc  Build ID DOCX without TOC\n"
	@printf "  make docx-en-no-toc  Build EN DOCX without TOC\n"
	@printf "  make docx-id-toc     Build ID DOCX with TOC\n"
	@printf "  make docx-en-toc     Build EN DOCX with TOC\n"
	@printf "  make docx-quick      Build ID DOCX only (no merge)\n"

merge:
	$(PY) paper/merge_paper.py --all

docx: docx-id

docx-merged: merge docx-id

docx-id:
	$(PY) paper/word_pipeline/scripts/md_to_docx_academic.py --lang id --no-toc

docx-en:
	$(PY) paper/word_pipeline/scripts/md_to_docx_academic.py --lang en --no-toc

docx-id-no-toc:
	$(PY) paper/word_pipeline/scripts/md_to_docx_academic.py --lang id --no-toc

docx-en-no-toc:
	$(PY) paper/word_pipeline/scripts/md_to_docx_academic.py --lang en --no-toc

docx-quick:
	$(PY) paper/word_pipeline/scripts/md_to_docx_academic.py --lang id --no-toc

docx-id-toc:
	$(PY) paper/word_pipeline/scripts/md_to_docx_academic.py --lang id --toc

docx-en-toc:
	$(PY) paper/word_pipeline/scripts/md_to_docx_academic.py --lang en --toc
