# Notes for code tracing
## Global Paremeters
```cpp
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

```cpp
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

    // For one-sided, may need to delete clauses added by initial BCP   // Yun-Rong Luo: reverse implication proof or one-sided proof
    cnf.delete_assertions();                                            // Yun-Rong Luo: print "Delete all but final asserted clause"
    std::vector<int> overcount_literals;
    bool overcount = false;
    for (int cid = 1; !overcount && cid <= cnf.clause_count(); cid++) {
	    bool deleted = pog.delete_input_clause(cid, unit_cid, overcount_literals); // Yun-Rong Luo: delete ith clause
	    if (!deleted)
	        overcount = true;
    }

    return 20(overcount) or 10(undercount) or 0(correct)

}
```

```cpp
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
```cpp
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
```cpp
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
```cpp
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
    return jcid;            // Yun-Rong Luo: jcid is the id of the target clause
}
```

##### Main justify body
```cpp
	int rvar = IABS(rlit);
	Pog_node *rnp = get_node(rvar);

    // use lemma ....
    if (use_lemma && cnf->use_lemmas && rnp->want_lemma()) {
	    int jid = apply_lemma(rnp, parent_or);
	    if (jid == 0)
		    cnf->pwriter->diagnose("Failed lemma.  Giving up on validation of node %s", rnp->name());
	    return jid;                                 // Yun-Rong Luo: If lemma applied, jcid returned here
	}

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
##### Justify `POG_OR`
```cpp
        incr_count(COUNT_VISIT_OR);
		int clit[2];                            // Yun-Rong Luo: child literal
		int jid;                                // Yun-Rong Luo: justify clause id of the children
		int lhints[2][2];
		int hcount[2] = {0,0};
		int jcount = 0;                         // Yun-Rong Luo: count of non-trivial children justification

        // Yun-Rong Luo: Assume u = u_0 + u_1, asserting literals: P=l_1, ..., l_n
        // YUN-RONG Luo: Assume u_0 contains ~x, u_1 contains x
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
			    lhints[i][hcount[i]++] = jid;   // Yun-Rong Luo: (u_0 + x  +  ~l_1 + .... + ~l_n ) TODO???
                                                // Yun-Rong Luo: (u_1 + ~x +  ~l_1 + .... + ~l_n ) TODO???
		    }
		}

        if (jcount > 1) 
        {
		    // Must prove in two steps
		    int slit = first_literal(clit[0]);          // Yun-Rong Luo: u_0 contains ~x
		    Clause *jclause0 = new Clause();            // Yun-Rong Luo: (x + u + ~l_1 + .... + ~l_n ) 
		    jclause0->add(-slit);
		    jclause0->add(xvar);
		    for (int alit : *cnf->get_assigned_literals())
			jclause0->add(-alit);
		    cnf->pwriter->comment("Justify node %s", rnp->name());
		    int cid0 = cnf->start_assertion(jclause0);
		    for (int h = 0; h < hcount[0]; h++)
			cnf->add_hint(lhints[0][h]);                // Yun-Rong Luo: hints for jclause0 are: (u + ~u_0), (u_0 + x  +  ~l_1 + .... + ~l_n )
		    cnf->finish_command(true);
		    incr_count(COUNT_OR_JUSTIFICATION_CLAUSE);

		    hints.push_back(cid0);                      // Yun-Rong Luo: hints for jclause: jclause0 (x + u + ~l_1 + .. + ~l_n), (u + ~u_1), (u_1 + ~x +  ~l_1 + .... + ~l_n )
		    for (int h = 0; h < hcount[1]; h++)
			hints.push_back(lhints[1][h]);
		    jtype = COUNT_OR_JUSTIFICATION_CLAUSE;
		} 
        else 
        {
		    // Can do with single proof step
		    incr_count(COUNT_OR_JUSTIFICATION_CLAUSE);  
		    for (int i = 0; i < 2; i++)                 // Yun-Rong Luo: u = u_0 (no branching decision)
			for (int h = 0; h < hcount[i]; h++)
			    hints.push_back(lhints[i][h]);          // Yun-Rong Luo: hints for jclause: (u + ~u_0), (u_0 + ~l_1, ..., ~l_n)
		}
```

##### Justify `POG_AND`
```cpp
        incr_count(COUNT_VISIT_AND);
		int cnext = 0;
		// If parent is OR, first argument is splitting literal
		if (parent_or) 
        {
		    int clit0 = (*rnp)[cnext++];
		    cnf->push_assigned_literal(clit0);          // Yun-Rong Luo: OR node calls: validate(u_0, P \cup ~x, \psi) and validate(u_1, P \cup x, \psi)
		    jclause->add(-clit0);
		    cnf->pwriter->comment("Justify node %s, assuming literal %d",
					  rnp->name(), clit0);
		    // Assertion may enable BCP, but it shouldn't lead to a conflict
		    if (cnf->bcp(false) > 0) {
			cnf->pwriter->diagnose("BCP encountered conflict when attempting to justify node %s with assigned literal %d\n",
					       rnp->name(), clit0);
			return 0;
		    }
		} 
        else {
		    cnf->pwriter->comment("Justify node %s", rnp->name());
		}

		// Bundle up the literals and justify them with single call
		std::vector<int> lits;              
		std::vector<int> jids;
		for (; cnext < rnp->get_degree(); cnext++) {        // Yun-Rong Luo: lits exclude clit0
		    int clit = (*rnp)[cnext];
		    if (is_node(clit))
			break;
		    lits.push_back(clit);
		}
		if (lits.size() > 0) {
#if DEBUG
		    cnf->pwriter->comment("Justification of node %s includes justifying %d literals",
					  rnp->name(), lits.size());
		    cnf->pwriter->comment_container("  Literals", lits);
#endif
		    report(4, "Justify node %s, starting with %d literals\n", rnp->name(), lits.size());
		    // Hack to detect whether SAT call was made
		    int prev_sat_calls = get_count(COUNT_SAT_CALL);

		    cnf->validate_literals(lits, jids)              // Yun-Rong Luo: literals validated here

		    if (get_count(COUNT_SAT_CALL) > prev_sat_calls)
			incr_count(COUNT_VISIT_AND_SAT);
		    for (int jid : jids)
			hints.push_back(jid);
		}

		// Now deal with the node arguments
		bool partition = false;
		std::unordered_map<int,int> var2rvar;
		std::unordered_map<int,std::set<int>*> rvar2cset;
		std::set<int> *save_clauses = NULL;
		std::set<int> *pset = NULL;
		for (; cnext < rnp->get_degree(); cnext++) {
		    int clit = (*rnp)[cnext];
		    if (!partition && cnext < rnp->get_degree()-1 && is_node(clit)) {
			// Must partition clauses
			cnf->partition_clauses(var2rvar, rvar2cset);
			partition = true;
			save_clauses = new std::set<int>;
			cnf->extract_active_clauses(save_clauses);
			report(4, "Justifying node %s.  Partitioned clauses into %d sets\n", rnp->name(), rvar2cset.size());
		    }
		    if (partition) {
			int llit = first_literal(clit);
			auto fid = var2rvar.find(IABS(llit));
			if (fid == var2rvar.end()) {
			    // This shouldn't happen
			    cnf->pwriter->diagnose("Partitioning error.  Couldn't find representative for variable %d, representing first child of N%d",
				IABS(llit), IABS(clit));
			    err(true, "Cannot recover from partitioning error.  Node %s has %d children.  Partitioner found %d partitions.\n",
				rnp->name(), rnp->get_degree(), rvar2cset.size());
			}
			int rvar = fid->second;
			pset = rvar2cset.find(rvar)->second;
			// Restrict clauses to those relevant to this partition
			cnf->set_active_clauses(pset);
		    } 
		    int jid = justify(clit, false, true);
		    if (jid == 0) {
			cnf->pwriter->diagnose("Justification of node %s failed.  Argument = %d", rnp->name(), clit);
			if (partition)
			    cnf->pwriter->diagnose(" Clauses were split into %d partitions", rvar2cset.size());
			return 0;
		    }
		    hints.push_back(jid);
		    if (pset != NULL)
			delete pset;
		}
		hints.push_back(rnp->get_defining_cid());
		if (save_clauses != NULL)
		    cnf->set_active_clauses(save_clauses);
		jtype = COUNT_AND_JUSTIFICATION_CLAUSE;
```

##### Lemma 
```cpp
int Pog::apply_lemma(Pog_node *rp, bool parent_or) {
    report(3, "Attempting to prove/apply lemma for node .\n", rp->name());
    Lemma_instance *instance = cnf->extract_lemma(rp->get_xvar(), parent_or);   // Yun-Rong Luo: extract lemma of current active clauses

    // Search for compatible lemma
    Lemma_instance *lemma = rp->get_lemma();    // Yun-Rong Luo: retrieve the lemma of node rp
    while (lemma != NULL) {
	if (lemma->signature == instance->signature)
	    break;
	lemma = lemma->next;
    }

    if (lemma == NULL) {
	// The instance becomes the new lemma.  Must prove it
	lemma = instance;
	rp->add_lemma(lemma);                       // Yun-Rong Luo: set the node's lemma

	cnf->setup_proof(lemma);
	lemma->jid = justify(lemma->xvar, lemma->parent_or, false); // Yun-Rong Luo: prove lemma

    if (lemma->jid == 0)
	    return 0;

	cnf->restore_from_proof(lemma);                             // Yun-Rong Luo: restore context
	incr_count(COUNT_LEMMA_DEFINITION);
    }

    if (lemma->jid == 0)
	    return 0;

    // Yun-Rong Luo: lemma is previously proved, now apply it
    incr_count(COUNT_LEMMA_APPLICATION);
    int jid = cnf->apply_lemma(lemma, instance);
    return jid;     
}
```

#### Delete input clauses 
```cpp
bool Pog::delete_input_clause(int cid, int unit_cid, std::vector<int> &overcount_literals) {
    Clause *cp = cnf->get_input_clause(cid);
    // Label each node by whether or not it is guaranteed to imply the clause
    std::vector<bool> implies_clause;
    implies_clause.resize(nodes.size());
    // Vector starting with clause ID and then having hints for deletion
    std::vector<int> *dvp = new std::vector<int>;
    dvp->push_back(cid);
    if (cp->tautology()) {
	    cnf->pwriter->clause_deletion(dvp);
	    delete dvp;
	    return true;
    }
    dvp->push_back(unit_cid);

    // Yun-Rong Luo: bottom up one pass of the POG
    for (int nidx = 0; nidx < nodes.size(); nidx++) {
	Pog_node *np = nodes[nidx];
	bool implies = false;
	switch (np->get_type()) {
	case POG_AND:
	    implies = false;
	    // Must have at least one child implying the clause
	    for (int i = 0; i < np->get_degree(); i++) {
		int clit = (*np)[i];
		if (is_node(clit)) {
		    implies = implies_clause[clit-max_input_var-1];
		    if (implies) {
			    dvp->push_back(np->get_defining_cid()+i+1);
			    break;
		    }
		} else {
		    implies = cp->contains(clit);               // Yun-Rong Luo: if clit \in cp, then ~cp \implies ~clit
		    if (implies) {
			dvp->push_back(np->get_defining_cid()+i+1);
			break;
		    }
		}
	    }
	    break;
	case POG_OR:
	    // Must have all children implying the clause
	    implies = true;
	    for (int i = 0; i < np->get_degree(); i++) {
		int clit = (*np)[i];
		if (is_node(clit)) {
		    implies &= implies_clause[clit-max_input_var-1];
		} else
		    implies &= cp->contains(clit);
	    }
	    if (implies)
		dvp->push_back(np->get_defining_cid());
	    break;
	default:
	    err(true, "Unknown POG type %d for node N%d\n", (int) np->get_type(), np->get_xvar());
	}
	implies_clause[nidx] = implies;	    
    }
    bool proved = implies_clause[nodes.size()-1];
    if (proved)
	cnf->pwriter->clause_deletion(dvp);
    else {
	cp->show(stdout);
	if (get_deletion_counterexample(cid, implies_clause, overcount_literals))
	    err(false, "Error attempting to delete clause.  Prover failed to generate proof, but also couldn't generate counterexample\n");
    }
    delete dvp;
    return proved;
}
```


## TODOs
1. See what is or node additional hints for 
2. See function `justify` and `apply lemma`
3. See clause deletion information
4. See cppg-check 
5. See cpog-count.py

