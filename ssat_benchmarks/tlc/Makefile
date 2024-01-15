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
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-2.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-3.sdimacs 
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-4.sdimacs 
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-5.sdimacs 
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-7.sdimacs 
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-8.sdimacs 

genInvalid:
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-10.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-16.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-17.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-18.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-19.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-20.sdimacs
	$(INTERP) $(TCHAIN) -S -v $(VLEVEL) tlc01-nonuniform-depth-9.sdimacs

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

