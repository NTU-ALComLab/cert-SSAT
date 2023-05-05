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
// runGen in cpog-gen.cpp
static int run(FILE *cnf_file, FILE *nnf_file, Pog_writer *pwriter) {
    Cnf_reasoner cnf(cnf_file);
    Pog pog(&cnf);
    cnf.enable_pog(pwriter);
    pog.read_d4ddnnf(nnf_file);     // Yun-Rong Luo: read in d4ddnnf file and build pog (consisting of pog_node)
                                    // Yun-Rong Luo: Declare input clauses, root, operation and/or .... to *.cpog
    int root_literal = pog.get_root();

    if (one_sided)
	    unit_cid = cnf.assert_literal(root_literal);
    else if (monolithic)
	    unit_cid = cnf.monolithic_validate_root(root_literal);
    else
	    unit_cid = pog.justify(root_literal, false, use_lemmas);    // Yun-Rong Luo: print "Justify", start_assertion (print `a...`)....

    if (unit_cid == 0) // Undercount
	    return 10;

    // For one-sided, may need to delete clauses added by initial BCP
    cnf.delete_assertions();                                        // Yun-Rong Luo: print "Delete all but final asserted clause"
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
// runCheck in cpog-check.cpp
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
## Gen
#### Defining clauses 
1. OR node has extra hint in the end, the hint is added when a child is a node, the hint is the node's defining clause id +1
```
c Operation N5_OR
5 s 5 4 2 3 0
```

```
// in pog.cpp
bool Pog::concretize() {
    if (verblevel >= 5) {
	report(5, "Before concretizing:\n");
	show(stdout);
    }

    if (verblevel >= 2) {
	// Document input clauses
	cnf->pwriter->comment("Input clauses");
	for (int cid = 1; cid <= cnf->clause_count(); cid++)
	    cnf->document_input(cid);
    }

    // Insert declaration of root literal
    cnf->pwriter->declare_root(root_literal);

    for (Pog_node *np : nodes) {
	ilist args = ilist_copy_list(&(*np)[0], np->get_degree());
	int xvar = np->get_xvar();
	int defining_cid = 0;
	bool need_zero = false;
	switch (np->get_type()) {
	case POG_TRUE:
	case POG_AND:
	    defining_cid = cnf->start_and(xvar, args);
	    need_zero = false;
	    break;
	case POG_OR:
	    need_zero = true;
	    defining_cid = cnf->start_or(xvar, args);
	    for (int i = 0; i < np->get_degree(); i++) {
		// Find mutual exclusions
		int child_lit = (*np)[i];
		if (is_node(child_lit)) {                       // Yun-Rong Luo: The hint is added when a child is a node, the hint is the node's defining clause id +1
		    Pog_node *cnp = get_node(child_lit);
		    int hid = cnp->get_defining_cid() + 1;
		    cnf->add_hint(hid);                         
		}
	    }
	    break;
	default:
	    err(true, "POG Node #%d.  Can't handle node type with value %d\n", np->get_xvar(), (int) np->get_type());
	}
	cnf->finish_command(need_zero);                     // Yun-Rong Luo: print 0 in line end
	np->set_defining_cid(defining_cid);
	if (np->get_type() == POG_OR)
	    cnf->document_or(defining_cid, xvar, args);
	else
	    cnf->document_and(defining_cid, xvar, args);
	ilist_free(args);
	
    }
    return true;
}
```
### Justify
Assertion is in the form: `justify clause | 0 | hints 0` 
```
14 a 4 1 2 0 1 2 0
15 a 5 1 0 6 14 7 0
16 a 6 1 0 15 8 0
17 a 7 0 12 16 13 0
```

`justify` is a recursive function. Structure of `justify`:

```
int Pog::justify(int rlit, bool parent_or, bool use_lemma) {
    if (is_node(rlit)) {
        // main justify body 
    }
    else if (parent_or) {
	    // Special value to let OR verification proceed
	    jcid = TRIVIAL_ARGUMENT;
    } 
    else {
	    jcid = cnf->validate_literal(rlit, Cnf_reasoner::MODE_FULL);
    }
    return jcid;
}
```

Main justify body
```
	int rvar = IABS(rlit);
	Pog_node *rnp = get_node(rvar);

    // use lemma ....

    int xvar = rnp->get_xvar();
	Clause *jclause = new Clause();
	jclause->add(xvar);
	for (int alit : *cnf->get_assigned_literals())
	    jclause->add(-alit);

	std::vector<int> hints;
	cnf->new_context();

    // jclause and hints are modified here (TODO)
    switch (rnp->get_type()) {
	case POG_OR:
        // justify or ...
    case POG_AND:
        // justify and ...
    }

    jcid = cnf->start_assertion(jclause);       // print: jclause 0 
	for (int hint : hints)                      // print: hints
	    cnf->add_hint(hint);
	cnf->finish_command(true);                  // print 0
	incr_count(jtype);
	cnf->pop_context();
```
Justify `POG_OR`
```
        int clit[2];            // child literal
		int jid;                // justify clause id of the children
		int lhints[2][2];
		int hcount[2] = {0,0};
		int jcount = 0;         // count of non-trivial children justification 

        for (int i = 0; i < 2; i++) {
		    clit[i] = (*rnp)[i];        
		    lhints[i][hcount[i]++] = rnp->get_defining_cid()+i+1;
		    jid = justify(clit[i], true, true);
		    if (jid == 0) {
                // error handling
			    return 0;
		    } 
            else if (jid != TRIVIAL_ARGUMENT) {
			    jcount++;
			    lhints[i][hcount[i]++] = jid;
		    }
		}
```





## TODOs
1. See what is or node additional hints for 
2. See function `justify` and `apply lemma`
3. See clause deletion information
4. See cppg-check 
5. See cpog-count.py

