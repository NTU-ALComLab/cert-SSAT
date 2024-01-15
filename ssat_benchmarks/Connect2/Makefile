INTERP = python3
TCHAIN = ../../tools/toolchain.py
VLEVEL=1

run:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

lrun:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf

srun:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) *.sdimacs

invalidOP:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) cf_2_3x3_w_.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) cf_2_3x5_w_.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) cf_2_3x7_w_.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) cf_2_3x7_w_.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) cf_2_3x9_w_.sdimacs

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

