install:
	cd src ; make install

linstall:
	cd VerifiedChecker ; make install

srun:
	cd ssat_benchmarks ; make srun

lrun:
	cd ssat_benchmarks ; make lrun

clean:
	rm -f *~
	cd ssat_benchmarks; make clean
	cd src ; make clean
	cd test ; make clean
	cd tools ; make clean

superclean:
	rm -f *~
	cd ssat_benchmarks; make superclean
	cd src ; make superclean
	cd test ; make superclean
	cd tools ; make superclean
