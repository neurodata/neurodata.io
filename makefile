LATEX = pdflatex
SPELL = aspell
TEX = neurodata_bib
BIBTEX = biber
ECHO = echo

default: $(TEX).tex 
	$(LATEX) $(TEX); $(BIBTEX) $(TEX); $(LATEX) $(TEX); $(LATEX) $(TEX);
	$(RM) -f  *.blg *.dvi *.log *.toc *.lof *.lot *.cb *.bbl *.brf *.out *.aux $(TEX).ps 
	open -g $(TEX).pdf &

#download:
#	wget --backups=1 https://neurodata.io/bib_files/pubs_pre_prints.bib
#	wget --backups=1 https://neurodata.io/bib_files/pubs_peer_reviewed.bib
#	wget --backups=1 https://neurodata.io/bib_files/pubs_conf.bib
#	wget --backups=1 https://neurodata.io/bib_files/pubs_tech_reports.bib
#	wget --backups=1 https://neurodata.io/bib_files/pubs_other.bib
#	wget --backups=1 https://neurodata.io/bib_files/talks_invited.bib
#	wget --backups=1 https://neurodata.io/bib_files/talks_other.bib

view: $(TEX).tex 
	$(LATEX) $(TEX); $(BIBTEX) $(TEX); $(LATEX) $(TEX); $(LATEX) $(TEX)
	open $(TEX).pdf &

clean:
	$(RM) -f *.aux *.bcf *.blg *.dvi *.log *.toc *.lof *.lot *.cb *.bbl $(TEX).ps $(TEX).pdf *~

check:
	@echo "Passing the check will cause make to report Error 1."
	$(LATEX) $(TEX)  | grep -i undefined
