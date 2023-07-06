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
```
// runGen in cpog-gen.cpp
static int run(FILE *cnf_file, FILE *nnf_file, Pog_writer *pwriter) {
    Cnf_reasoner cnf(cnf_file);
    Pog pog(&cnf);
    cnf.enable_pog(pwriter);
    pog.read_d4ddnnf(nnf_file);     // Yun-Rong Luo: read in d4ddnnf file and build pog (consisting of pog_node)
                                    // Yun-Rong Luo: call Pog::concretize()
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

## Gen
#### Read D4 d-DNNNF
```
bool Pog::read_d4ddnnf(FILE *infile) {
    // Mapping from NNF ID to POG Node ID
    std::map<int,int> nnf_idmap;
    // Set of POG nodes that have at least one parent
    std::unordered_set<int> node_with_parent;
    // Vector of arguments for each POG node
    std::vector<std::vector<int> *> arguments;
    // Capture arguments for each line
    std::vector<int> largs;
    int line_number = 0;
    // Statistics
    int nnf_node_count = 0;
    int nnf_explicit_node_count = 0;
    int nnf_edge_count = 0;
    while (true) {
	pog_type_t ntype = POG_NONE;
	line_number++;
	int c = get_token(infile);
	int rc = 0;
	if (c == EOF)
	    break;
	if (c != 0) {                                   // Yun-Rong Luo: d4 declare node: o <id> 0 | a <id> 0 | t <id> 0 | f <id> 0
	    for (int t = POG_TRUE; t <= POG_OR; t++)
		if (c == pog_type_char[t])
		    ntype = (pog_type_t) t;
	    if (ntype == POG_NONE)
		err(true, "Line #%d.  Unknown D4 NNF command '%c'\n", line_number, c);
	    nnf_node_count++;
	    nnf_explicit_node_count++;
	    Pog_node *np = new Pog_node(ntype);
	    int pid = add_node(np);
	    arguments.push_back(new std::vector<int>);
	    bool ok = read_numbers(infile, largs, &rc);
	    if (!ok)
		err(true, "Line #%d.  Couldn't parse numbers\n", line_number);
	    else if (largs.size() == 0 && rc == EOF)
		break;
	    else if (largs.size() != 2)
		err(true, "Line #%d.  Expected 2 numbers.  Found %d\n", line_number, largs.size());
	    else if (largs.back() != 0)
		err(true, "Line #%d.  Line not zero-terminated\n", line_number);
	    else
		nnf_idmap[largs[0]] = pid;
	    report(3, "Line #%d.  Created POG node %s number %d from NNF node %d\n",
		   line_number, pog_type_name[ntype], pid, largs[0]); 
	} else {                                        // Yun-Rong Luo: d4 declare edge: <parent_id> <child_id> S  0 
                                                    // Yun-Rong Luo: S=empty set or a set of literals: l_1, l_2, ...,  l_n 
                                                    // Yun-Rong Luo: S=empty set is the case where <parent_id> is AND node
                                                    // Yun-Rong Luo: S=l_1, l_2, ..., l_n is the case where <parent_id> is OR node
                                                    // Yun-Rong Luo: l_1 is the decision, l_2, ..., l_n is implied by BCP
	    nnf_edge_count++;
	    bool ok = read_numbers(infile, largs, &rc);

	    // Find parent
	    auto fid = nnf_idmap.find(largs[0]);
	    int ppid = fid->second;                     // Yun-Rong Luo: ppid = <parent_id> (in POG) 

	    // Find second node
	    fid = nnf_idmap.find(largs[1]);
	    int spid = fid->second;                     // Yun-Rong Luo: spid = <child_id>  (POG)
	    int cpid = spid;                            // Yun-Rong Luo: cpid = the id of a new AND NODE consisting of l_1, ..., l_n, spid 

	    if (largs.size() > 3) {                     // Yun-Rong Luo: the case where S is not empty set
		// Must construct AND node to hold literals 
		nnf_node_count++;
		Pog_node *anp = new Pog_node(POG_AND);
		cpid = add_node(anp);                       // Yun-Rong Luo: cpid = AND(l_1,...,l_n, spid)
		std::vector<int> *aargs = new std::vector<int>;
		arguments.push_back(aargs);
		for (int i = 2; i < largs.size()-1; i++)    // Yun-Rong Luo: arguments are stored in the order: l_1, ..., l_n, spid
		    aargs->push_back(largs[i]);
		aargs->push_back(spid);
		report(3, "Line #%d. Created POG AND Node %d to hold literals between NNF nodes %d and %d\n",
		       line_number, cpid, largs[0], largs[1]); 
	    }
	    std::vector<int> *pargs = arguments[ppid-max_input_var-1];
	    pargs->push_back(cpid);                     // Yun-Rong Luo: cpid is the real explicit child id of ppid
	    node_with_parent.insert(cpid);
	    report(4, "Line #%d.  Adding edge between POG nodes %d and %d\n", line_number, ppid, cpid);
	}
    }
    // Add arguments
    for (int pid = max_input_var + 1; pid <= max_input_var + nodes.size(); pid++) {
	Pog_node *np = get_node(pid);
	std::vector<int> *args = arguments[pid-max_input_var-1];
	np->add_children(args);
	delete args;
    }

    // ....

    return (concretize());
}
```
#### Concretize POG
```
// in pog.cpp
bool Pog::concretize() {

	// Document input clauses
	cnf->pwriter->comment("Input clauses");
	for (int cid = 1; cid <= cnf->clause_count(); cid++)
	    cnf->document_input(cid);

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
	    defining_cid = cnf->start_and(xvar, args);      // Yun-Rong Luo: print " id p v l_1 l_2 ...... l_n " 
                                                        // Yun-Rong Luo: add_proof_clause(): proof_clauses.pushback(AND defining clauses) 
	    need_zero = false;
	    break;
	case POG_OR:
	    need_zero = true;
	    defining_cid = cnf->start_or(xvar, args);       // Yun-Rong Luo: print " id s v l_1 l_2" 
                                                        // Yun-Rong Luo: add_proof_clause(): proof_clauses.pushback(OR defining clauses)

	    for (int i = 0; i < np->get_degree(); i++) {
		    // Find mutual exclusions
		    int child_lit = (*np)[i];                   // Yun-Rong Luo: access the ith children
		    if (is_node(child_lit)) {                       
		        Pog_node *cnp = get_node(child_lit);
		        int hid = cnp->get_defining_cid() + 1;  // Yun-Rong Luo: child_1 = AND(l_1, l_2, ..., l_n, C_1)
                                                        // Yun-Rong Luo: child_2 = AND(~l_1, l_n+1, ..., l_m, C_2)
                                                        // Yun-Rong Luo: hid_1 is the clause: ( ~child_1 + l_1  )
                                                        // Yun-Rong Luo: hid_2 is the clause: ( ~child_2 + ~l_1 )
		        cnf->add_hint(hid);                         
		    }
	    }
	    break;
	default:
	    err(true, "POG Node #%d.  Can't handle node type with value %d\n", np->get_xvar(), (int) np->get_type());
	}
	cnf->finish_command(need_zero);                     // Yun-Rong Luo: print 0 in line end
	np->set_defining_cid(defining_cid);                 // Yun-Rong Luo: Each node is associated defining_cid
	if (np->get_type() == POG_OR)
	    cnf->document_or(defining_cid, xvar, args);     // Yun-Rong Luo: print Implicit declarations of defining clauses
	else
	    cnf->document_and(defining_cid, xvar, args);
	ilist_free(args);
	
    }
    return true;
}
```
#### Justify
Assertion is in the form: `a <justify clause> 0 <hints> 0` 
```
14 a 4 1 2 0 1 2 0
15 a 5 1 0 6 14 7 0
16 a 6 1 0 15 8 0
17 a 7 0 12 16 13 0
```

`justify` is a recursive function. It is called `validate` in the paper. 

##### No Lemma Version
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
	Clause *jclause = new Clause();                 // Yun-Rong Luo: jclause is target clause in the paper
	jclause->add(xvar);     
	for (int alit : *cnf->get_assigned_literals())
	    jclause->add(-alit);

	std::vector<int> hints;
	cnf->new_context();                             // Yun-Rong Luo: TODO

    switch (rnp->get_type()) {
	case POG_OR:
        // justify or ...
    case POG_AND:
        // justify and ...
    }

    jcid = cnf->start_assertion(jclause);       // Yun-Rong Luo: add_proof_clause(jclause)
                                                // Yun-Rong Luo: print jclause 0
                                                // Yun-Rong Luo: deletion_stack.pushback(new vector<int>(jcid)))

	for (int hint : hints)                      // Yun-Rong Luo: print hints
	    cnf->add_hint(hint);
	cnf->finish_command(true);                  // Yun-Rong Luo: print 0
	incr_count(jtype);
	cnf->pop_context();                         // Yun-Rong Luo: TODO
```
Justify `POG_OR`
```
        incr_count(COUNT_VISIT_OR);
		int clit[2];                            // Yun-Rong Luo: child literal
		int jid;                                // Yun-Rong Luo: justify clause id of the children
		int lhints[2][2];
		int hcount[2] = {0,0};
		int jcount = 0;                         // Yun-Rong Luo: count of non-trivial children justification

        // Yun-Rong Luo: Assume u = u_0 + u_1, asserting literals: P=l_1, ..., l_n
		for (int i = 0; i < 2; i++) {
		    clit[i] = (*rnp)[i];                // Yun-Rong Luo: u_i
		    lhints[i][hcount[i]++] = rnp->get_defining_cid()+i+1;   // Yun-Rong Luo: (u + ~u_i) 

		    jid = justify(clit[i], true, true); // Yun-Rong Luo: parent_or=true, use_lemma=true
		    if (jid == 0) {
			    cnf->pwriter->diagnose("Justification of node %s failed.  Couldn't validate %s child %d.  Splitting literal = %d",
					       rnp->name(), i == 0 ? "first" : "second", clit[i], first_literal(clit[i]));
			    return 0;
		    } 
            else if (jid != TRIVIAL_ARGUMENT) {
			    jcount++;
			    lhints[i][hcount[i]++] = jid;   // Yun-Rong Luo: (u_0 + x + ~l_1 + .... + ~l_n ) 
                                                // Yun-Rong Luo: (u_1 + ~x + ~l_1 + .... + ~l_n ) 
		    }
		}

        if (jcount > 1) 
        {
		    // Must prove in two steps
		    int slit = first_literal(clit[0]);
		    Clause *jclause0 = new Clause();
		    jclause0->add(-slit);
		    jclause0->add(xvar);
		    for (int alit : *cnf->get_assigned_literals())
			jclause0->add(-alit);
		    cnf->pwriter->comment("Justify node %s", rnp->name());
		    int cid0 = cnf->start_assertion(jclause0);
		    for (int h = 0; h < hcount[0]; h++)
			cnf->add_hint(lhints[0][h]);
		    cnf->finish_command(true);
		    incr_count(COUNT_OR_JUSTIFICATION_CLAUSE);
		    hints.push_back(cid0);
		    for (int h = 0; h < hcount[1]; h++)
			hints.push_back(lhints[1][h]);
		    jtype = COUNT_OR_JUSTIFICATION_CLAUSE;
		} 
        else 
        {
		    // Can do with single proof step
		    incr_count(COUNT_OR_JUSTIFICATION_CLAUSE);
		    for (int i = 0; i < 2; i++)
			for (int h = 0; h < hcount[i]; h++)
			    hints.push_back(lhints[i][h]);
		}

        
```





## TODOs
1. See what is or node additional hints for 
2. See function `justify` and `apply lemma`
3. See clause deletion information
4. See cppg-check 
5. See cpog-count.py

