# Notes for code tracing
## Global Paremeters
```
verbLevel = 1

oneSided = False
monolithic = False
useLemma = True
group = True
useLean = False
```
- oneSided = True: Generate one-sided proof (don't validate assertions)
- monolithic = True: Do validation with single call to SAT solver
- useLemma = False: Expand each node, rather than using lemmas
- group = False: Prove each literal separately, rather than grouping into single proof
- useLean = True: Run Lean checker to formally check
- force is default set to !useLean

## Toochain flow
- runD4:
- runGen: cpog-gen, code in src/
- useLean: 
    - runLeanCheck: VerifiedChecker/build/bin/checker
- not useLean:
    - runCheck: cpog-check, code in src/
    - runCount: tools/cpog-count.py

```
// runGen
static int run(FILE *cnf_file, FILE *nnf_file, Pog_writer *pwriter) {
    Cnf_reasoner cnf(cnf_file);
    Pog pog(&cnf);
    cnf.enable_pog(pwriter);
    pog.read_d4ddnnf(nnf_file);     // read in d4ddnnf file and build pog (consisting of pog_node)
    int root_literal = pog.get_root();

    if (one_sided)
	    unit_cid = cnf.assert_literal(root_literal);
    else if (monolithic)
	    unit_cid = cnf.monolithic_validate_root(root_literal);
    else
	    unit_cid = pog.justify(root_literal, false, use_lemmas);

    if (unit_cid == 0) // Undercount
	    return 10;

    // For one-sided, may need to delete clauses added by initial BCP
    cnf.delete_assertions();
    std::vector<int> overcount_literals;
    bool overcount = false;
    for (int cid = 1; !overcount && cid <= cnf.clause_count(); cid++) {
	    bool deleted = pog.delete_input_clause(cid, unit_cid, overcount_literals);
	    if (!deleted)
	        overcount = true;
    }

    return 20(overcount) or 10(undercount) or 0(correct)

}
```

```
// runCheck
void run(char *cnf_name, char *cpog_name) {
    cnf_read(cnf_name);
    cpog_read(cpog_name);               
    int root = cpog_final_root();
	if (one_sided)
	    data_printf(0, "ONE-SIDED VALID.  CPOG representation partially verified\n");
	else
	    data_printf(0, "FULL-PROOF SUCCESS.  CPOG representation verified\n");
    }

}
```
Proving lies in `cpog_read()` and `cpog_final_root()`

```
// runCount
```

## TODOs
1. Understand CPOG format and its generation
2. Find forward & backward checking
3. See cpog-count.py

