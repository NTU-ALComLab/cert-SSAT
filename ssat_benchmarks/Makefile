INTERP = python3
TCHAIN = ../tools/toolchain.py
VLEVEL=3

run:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

lrun:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf

srun:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc/*.sdimacs

.SUFFIXES: .cnf .log .lean_log

.cnf.log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) $<

.cnf.lean_log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) -F $<

clean:
	rm -f *~ d2p.log

superclean: clean
	rm -f tlc/*.nnf tlc/*.cpog tlc/*log tlc/*.prob
	rm -f *.nnf *.cpog *log

