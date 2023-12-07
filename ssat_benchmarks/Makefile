INTERP = python3
TCHAIN = ../tools/toolchain.py
VLEVEL=5

run:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

lrun:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf

srun:
	cd Adder;       make srun
	cd RobotsD2;    make srun
	cd conformant;  make srun
	cd k_ph_p;      make srun
	cd tiger;       make srun
	cd Connect2;    make srun
	cd MaxCount;    make srun
	cd ToiletA;     make srun
	cd ev-pr-4x4;   make srun
	cd sand-castle; make srun
	cd tlc;         make srun
	cd Counter;     make srun
	cd PEC;         make srun
	cd Tree;        make srun
	cd gttt_3x3;    make srun
	cd MPEC;        make srun
	cd Planning-CTE;make srun
	cd arbiter;     make srun
	cd k_branch_n;  make srun
	cd stracomp;    make srun
                                     
.SUFFIXES: .cnf .log .lean_log

.cnf.log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) $<

.cnf.lean_log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) -F $<

clean:
	rm -f *~ d2p.log

superclean: clean
	cd Adder;       make srun
	cd RobotsD2;    make srun
	cd conformant;  make srun
	cd k_ph_p;      make srun
	cd tiger;       make srun
	cd Connect2;    make srun
	cd MaxCount;    make srun
	cd ToiletA;     make srun
	cd ev-pr-4x4;   make srun
	cd sand-castle; make srun
	cd tlc;         make srun
	cd Counter;     make srun
	cd PEC;         make srun
	cd Tree;        make srun
	cd gttt_3x3;    make srun
	cd MPEC;        make srun
	cd Planning-CTE;make srun
	cd arbiter;     make srun
	cd k_branch_n;  make srun
	cd stracomp;    make srun
	rm -f *.nnf *.cpog *log *cnf

