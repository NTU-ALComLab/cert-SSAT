# cert-SSAT 
A stochastic Boolean satisfiability(SSAT) verification framework implemented on top of the model counting verification framework [CPOG](https://github.com/rebryant/cpog.git)

## Installation:

Running the toolchain using prototype (unverified) tools requires the following:

* A C and C++ compiler
* A python3 interpreter
* Compiled CaDiCal SAT solver, Drat-trim proof checker, and SharpSSAT SSAT solver (included in tools as submodules)

## Directories
* **ssat_benchmarks:**
    SSAT benchmark set
* **src:**
    Code for the CPOG generator and prototype checker
* **tools:**
    Code for a scripting program that runs the entire toolchain (put SharpSSAT, cadical, drat-trim here)

## Make Options

* **install:**
    Compiles evalSSAT, cpog-gen, cpog-check
* **srun:**
    Runs SharpSSAT, evalSSAT, cpog-gen, cpog-check on ssat_benchmark files
* **clean:**
    Removes intermediate files
* **superclean:**
    Removes all generated files
