install:
	cd src ; make install

linstall:
	cd VerifiedChecker ; make install

ptest:
	cd test ; make test

otest:
	cd test ; make otest

lowtest:
	cd test ; make lowtest

uptest:
	cd test ; make uptest

ltest:
	cd test ; make ltest


run:
	cd benchmarks ; make run

lrun:
	cd benchmarks ; make lrun

srun:
	cd ssat_benchmarks ; make srun

clean:
	rm -f *~
	cd benchmarks; make clean
	cd src ; make clean
	cd test ; make clean
	cd tools ; make clean

superclean:
	rm -f *~
	cd benchmarks; make superclean
	cd src ; make superclean
	cd test ; make superclean
	cd tools ; make superclean
