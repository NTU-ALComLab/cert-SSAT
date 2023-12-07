INTERP = python3
TCHAIN = ../tools/toolchain.py
VLEVEL=5

run:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

lrun:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf

srun:
	cd sand-castle; make srun
	cd RobotsD2_easy;    make srun
	cd conformant_easy;  make srun 
	cd tiger;       make srun
	cd Counter;     make srun
	cd tlc;         make srun
	cd gttt_3x3;    make srun
	cd ev-pr-4x4;   make srun
	cd Tree;        make srun
	cd Connect2;    make srun
	cd k_ph_p;      make srun
	cd k_branch_n;  make srun
	cd Adder;       make srun
                                     
.SUFFIXES: .cnf .log .lean_log

.cnf.log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) $<

.cnf.lean_log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) -F $<

clean:
	rm -f *~ d2p.log

superclean: clean
	cd Adder;       make superclean 
	cd RobotsD2_easy;    make superclean 
	cd conformant_easy;  make superclean 
	cd k_ph_p;      make superclean 
	cd tiger;       make superclean 
	cd Connect2;    make superclean 
	cd MaxCount;    make superclean 
	cd ToiletA;     make superclean 
	cd ev-pr-4x4;   make superclean 
	cd sand-castle; make superclean 
	cd tlc;         make superclean 
	cd Counter;     make superclean 
	cd PEC;         make superclean 
	cd Tree;        make superclean 
	cd gttt_3x3;    make superclean 
	cd MPEC;        make superclean 
	cd Planning-CTE;make superclean 
	cd arbiter;     make superclean 
	cd k_branch_n;  make superclean 
	cd stracomp;    make superclean 
	rm -f *.nnf *.cpog *log *cnf

