INTERP = python3
TCHAIN = ../tools/toolchain.py
VLEVEL=5

run:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

lrun:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf

srun:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) sand-castle_easy/*.sdimacs

.SUFFIXES: .cnf .log .lean_log

.cnf.log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) $<

.cnf.lean_log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) -F $<

clean:
	rm -f *~ d2p.log

superclean: clean
	rm -f tlc/*.nnf tlc/*.cpog tlc/*log tlc/*.prob
	rm -f gttt_3x3/*.nnf gttt_3x3/*.cpog gttt_3x3/*log gttt_3x3/*.prob
	rm -f sand-castle/*.nnf sand-castle/*.cpog sand-castle/*log sand-castle/*.prob
	rm -f sand-castle_easy/*.nnf sand-castle_easy/*.cpog sand-castle_easy/*log sand-castle_easy/*.prob
	rm -f *.nnf *.cpog *log

