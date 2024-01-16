INTERP = python3
TCHAIN = ../../tools/toolchain.py
VLEVEL=1

run:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

lrun:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf

srun:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) *.sdimacs

gen6:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x15.4.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x15.9.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x20.4.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x5.9.sdimacs

gen9:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x35.19.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x35.9.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x40.14.sdimacs

gen11:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x10.9.sdimacs

genTO:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x10.19.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x15.14.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x35.14.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x35.4.sdimacs

ssatTO:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x40.19.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) x40.9.sdimacs

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

