INTERP = python3
TCHAIN = ../../tools/toolchain.py
VLEVEL=1

run:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

lrun:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf

srun:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) *.sdimacs

eval:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa10-30.sdimacs
#   $(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa10-10.sdimacs
#	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa10-15.sdimacs
#	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa10-20.sdimacs
#	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa10-25.sdimacs

invalidOP:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa2-10.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa2-15.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa2-20.sdimacs 
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa2-25.sdimacs 
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa2-30.sdimacs 
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa2-35.sdimacs 
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa2-40.sdimacs 
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa2-45.sdimacs 
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tree-exa2-50.sdimacs 



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

