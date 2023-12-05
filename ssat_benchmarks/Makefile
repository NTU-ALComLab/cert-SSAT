INTERP = python3
TCHAIN = ../../tools/toolchain.py
VLEVEL=1

run:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

lrun:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf

srun:
	cd tlc; $(INTERP) $(TCHAIN) -S -v $(VLEVEL) *.sdimacs
	cd ev-pr-4x4-log; $(INTERP) $(TCHAIN) -S -v $(VLEVEL) *.sdimacs

.SUFFIXES: .cnf .log .lean_log

.cnf.log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) $<

.cnf.lean_log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) -F $<

clean:
	rm -f *~ d2p.log

superclean: clean
	rm -f *.nnf *.cpog *log

