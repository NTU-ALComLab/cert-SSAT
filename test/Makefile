INTERP = python3
TCHAIN = ../tools/toolchain.py
VLEVEL=2

test:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

otest:
	$(INTERP) $(TCHAIN) -1 -v  $(VLEVEL) *.cnf

lowtest:
	$(INTERP) $(TCHAIN) -1 -S -v  $(VLEVEL) *.cnf

uptest:
	$(INTERP) $(TCHAIN) -S -v  $(VLEVEL) *.cnf

ltest:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf
 

.SUFFIXES: .cnf .log .lean_log

.cnf.log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) $<

.cnf.lean_log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) -F $<

clean:
	rm -f *~ d2p.log

superclean: clean
	rm -f *.nnf *.cpog *log
