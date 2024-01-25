# cert-SSAT 

## Installation:

Running the toolchain using prototype (unverified) tools requires the following:

* A C and C++ compiler
* A python3 interpreter
* An installed version of the [CaDiCal SAT solver](https://github.com/arminbiere/cadical)
* An installed version of the [Drat-trim proof checker](https://github.com/marijnheule/drat-trim)
* SharpSSAT (attached)

## Directories

* **VerifiedChecker:**
    Code for the verified checker and counter
* **ssat_benchmarks:**
    SSAT benchmark set
* **src:**
    Code for the CPOG generator and prototype checker
* **test:**
    Two very simple test problems
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
