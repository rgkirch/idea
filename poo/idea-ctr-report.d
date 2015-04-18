# vim: ft=make
.PHONY: idea-ctr-report._graphics
idea-ctr-report.aux idea-ctr-report.aux.make idea-ctr-report.d idea-ctr-report.pdf: $(call path-norm,/usr/share/texlive/texmf-dist/tex/latex/base/article.cls)
idea-ctr-report.aux idea-ctr-report.aux.make idea-ctr-report.d idea-ctr-report.pdf: $(call path-norm,idea-ctr-report.tex)
.SECONDEXPANSION:
