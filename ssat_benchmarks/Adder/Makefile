INTERP = python3
TCHAIN = ../../tools/toolchain.py
VLEVEL=1

run:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

lrun:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf

srun:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) *.sdimacs

gen11:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) Adder2-2-c.sdimacs

eval:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) adder-2-sat.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) adder-2-unsat.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) adder-4-sat.sdimacs

.SUFFIXES: .cnf .log .lean_log

.cnf.log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) $<

.cnf.lean_log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) -F $<

clean:
	rm -f *~ d2p.log

extraclean: clean
	rm -f *.nnf *.cpog *.prob

superclean: clean
	rm -f *.nnf *.cpog *log *.cnf *.prob

