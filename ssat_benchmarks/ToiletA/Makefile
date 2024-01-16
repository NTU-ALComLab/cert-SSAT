INTERP = python3
TCHAIN = ../../tools/toolchain.py
VLEVEL=1

run:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

lrun:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf

srun:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) *.sdimacs

undone:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_01.2.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_01.3.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_01.4.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_01.5.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_01.6.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_01.7.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_01.8.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_01.9.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_01.13.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_01.14.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_01.16.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_05.*.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_08_10.2.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) toilet_a_10*.sdimacs

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

