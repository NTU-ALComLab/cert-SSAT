INTERP = python3
TCHAIN = ../tools/toolchain.py
VLEVEL=5

run:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) *.cnf

lrun:
	$(INTERP) $(TCHAIN) -F -v $(VLEVEL) *.cnf

srun:
	cd tlc;                 make srun 
	cd gttt_3x3;            make srun 
	cd ev-pr-4x4;           make srun 
	cd Tree;                make srun 
	cd Connect2;            make srun 
	cd k_ph_p;              make srun  #killed
	cd k_branch_n;          make srun  #killed
	cd tiger;               make srun 
	cd Adder;               make srun 
	cd Counter;             make srun 
	cd PEC;                 make srun 
	cd MPEC;                make srun  #killed
	cd conformant;          make srun 
	cd RobotsD2;            make srun 
	cd MaxCount;            make srun  #killed 
	cd ToiletA;             make srun  #killed
	cd sand-castle;         make srun  #killed
	cd stracomp;            make srun 

easy1:
	cd gttt_3x3;            make srun # 9/9 (sharpSSAT/all)
	cd ev-pr-4x4;           make srun # 7/7
	cd Tree;                make srun # 14/14
	cd tiger;               make srun # 5/5

easy2:
	cd stracomp;            make srun # 31/60
	cd tlc;                 make srun # 13/13

easy3:
	cd Connect2;            make srun # 16/16
	cd Adder;               make srun # 5/6
	cd PEC;                 make srun # 4/4

undone:
	cd RobotsD2;            make srun # 5/10
	cd conformant;          make srun # 3/24
	cd Counter;             make srun # 8/8
    
                                     
.SUFFIXES: .cnf .log .lean_log

.cnf.log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) $<

.cnf.lean_log:
	$(INTERP) $(TCHAIN) -v $(VLEVEL) -F $<

clean:
	rm -f *~ d2p.log

superclean1:
	cd tlc;                 make superclean 
	cd gttt_3x3;            make superclean 
	cd ev-pr-4x4;           make superclean 
	cd Tree;                make superclean 
	cd Connect2;            make superclean 
	cd k_ph_p;              make superclean 
	cd k_branch_n;          make superclean 
	cd tiger;               make superclean

superclean2:
	cd Adder;               make superclean 
	cd Counter;             make superclean 
	cd PEC;                 make superclean 
	cd MPEC;                make superclean 
	cd conformant;          make superclean 
	cd RobotsD2;            make superclean 

superclean3:
	cd MaxCount;            make superclean 
	cd ToiletA;             make superclean 
	cd sand-castle;         make superclean 
	cd stracomp;            make superclean

superclean: clean superclean1 superclean2 superclean3
	rm -f *.nnf *.cpog *log *cnf

