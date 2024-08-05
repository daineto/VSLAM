from unified_planning.shortcuts import *
from itertools import product, combinations
from copy import deepcopy

def get_fluent_value(fluent, state):
        current_instance = state
        while current_instance is not None:
            value_found = current_instance._values.get(fluent, None)
            if value_found is not None:
                return value_found._content.payload
            current_instance = current_instance._father

def generate_transition_relation(problem):
    #static_fluents = problem.get_static_fluents()
    all_literals = problem.initial_values.keys()
    all_objects = problem.all_objects

    fluent_literals = [l for l in all_literals if l.fluent()]
    tuples = product([True,False], repeat=len(fluent_literals))


    transitions = []
    for tup in tuples:
        for i in range(len(fluent_literals)):       
            problem.set_initial_value(fluent_literals[i],tup[i])
        for a in problem.actions:
            matching_objects = [[o for o in all_objects if o.type == a.parameters[i].type] for i in range(len(a.parameters))]
            args_list = product(*matching_objects)
            for args in args_list:
                if len(set(args)) == len(args):
                    with SequentialSimulator(problem=problem) as simulator:
                        pre_state = simulator.get_initial_state()
                        if simulator.is_applicable(pre_state, a, args):
                            post_state = simulator.apply(pre_state, a, args)
                            transitions += [({(fluent.fluent().name, tuple([arg._content.payload.name for arg in fluent.args]),get_fluent_value(fluent,pre_state)) for fluent in all_literals},(a.name,args),{(fluent.fluent().name, tuple([arg._content.payload.name for arg in fluent.args]),get_fluent_value(fluent,post_state)) for fluent in all_literals})]
                        else:
                            transitions += [({(fluent.fluent().name, tuple([arg._content.payload.name for arg in fluent.args]),get_fluent_value(fluent,pre_state)) for fluent in all_literals},(a.name,args),None)]  

    return transitions

def generate_transitions_from_problem(problem, generate_failures=True):
    # Compute Plan
    transitions = []
    failures = []

    all_literals = problem.initial_values.keys()
    all_objects = problem.all_objects

    with OneshotPlanner(name='fast-downward') as planner:
        result = planner.solve(problem)
        if result.status == unified_planning.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
            plan = result.plan
            print(plan)

    # Generate transitions following the plan
    with SequentialSimulator(problem=problem) as simulator:
        pre_state = simulator.get_initial_state()
        for action_instance in result.plan.actions:

            if generate_failures:
                for a in problem.actions:
                    # matching_objects = [[o for o in all_objects if o.type == a.parameters[i].type] for i in range(len(a.parameters))]
                    matching_objects = [[o for o in all_objects if o.type.is_subtype(a.parameters[i].type)] for i in range(len(a.parameters))]
                    args_list = product(*matching_objects)
                    for args in args_list:
                        if len(set(args)) == len(args):
                            if not simulator.is_applicable(pre_state, a, args):
                                failures += [({(fluent.fluent().name, tuple([arg._content.payload.name for arg in fluent.args]),get_fluent_value(fluent,pre_state)) for fluent in all_literals},(a.name,args),None)]
                                break
            
            post_state = simulator.apply(pre_state, action_instance)
            if post_state is None:
                print(f'Error in applying: {action_instance}')
                break
            transitions += [({(fluent.fluent().name, tuple([arg._content.payload.name for arg in fluent.args]),get_fluent_value(fluent,pre_state)) for fluent in all_literals},(action_instance.action.name,tuple([par.object() for par in action_instance.actual_parameters])),{(fluent.fluent().name, tuple([arg._content.payload.name for arg in fluent.args]),get_fluent_value(fluent,post_state)) for fluent in all_literals})]
            pre_state = post_state

    return transitions, failures

def lift_transitions(transitions, all_actions):
    action_pars_dict = {a.name:tuple([par.name for par in a.parameters]) for a in all_actions}

    lifted_transitions = set()
    for t in transitions:
        pre_state = t[0] # set of tuples (fluent_name, args, valuation)
        action = t[1] # (action_name, args)
        post_state = t[2] # set of tuples (fluent_name, args, valuation)
        
        action_name = action[0]
        action_pars = action_pars_dict[action_name]
        action_args = [arg.name for arg in t[1][1]]
        map_arg_to_par = {action_args[i]:action_pars[i] for i in range(len(action_args))}

        lifted_pre_state = set()
        for l in list(pre_state):
            literal_args = l[1]
            NARG = len(literal_args)
            if set(literal_args).issubset(action_args) and len(set(literal_args)) == len(literal_args):
            # if set(literal_args).issubset(action_args):
                lifted_args = tuple([map_arg_to_par[literal_args[i]] for i in range(NARG)])
                lifted_pre_state.add((l[0], lifted_args, l[2]))
        lifted_pre_state = tuple(sorted(lifted_pre_state))
        
        if post_state is not None:
            lifted_post_state = set()
            for l in list(post_state):
                literal_args = l[1]
                NARG = len(literal_args)
                if set(literal_args).issubset(action_args) and len(set(literal_args)) == len(literal_args):
                # if set(literal_args).issubset(action_args):
                    lifted_args = tuple([map_arg_to_par[literal_args[i]] for i in range(NARG)])
                    lifted_post_state.add((l[0], lifted_args, l[2]))
            lifted_post_state = tuple(sorted(lifted_post_state))
        else:
            lifted_post_state = None

        lifted_transitions.add((lifted_pre_state, (action_name, action_pars), lifted_post_state))

    print("From {} transitions to {} lifted transitions".format(len(transitions), len(lifted_transitions)))

    return lifted_transitions

def generate_all_lifted_literals(action, all_fluents):

    action_types = set()
    for par in action.parameters:
        new_types = set(par.type.ancestors)
        action_types.update(new_types)
    # action_types = set([par.type for par in action.parameters])
    # type_to_par = {t:set([par.name for par in action.parameters if par.type == t]) for t in action_types}
    type_to_par = {t:set([par.name for par in action.parameters if par.type.is_subtype(t)]) for t in action_types}

    # action_signature = [par.type for par in action.parameters]

    generated_literals = set()
    for fluent in all_fluents:        
        fluent_types = set([par.type for par in fluent.signature])
        # fluent_signature = [par.type for par in fluent.signature]
        if fluent_types.issubset(action_types):
            matching_pars = [type_to_par[fpar.type] for fpar in fluent.signature]
            matches = list(product(*matching_pars))

            matches = [match for match in matches if len(set(match)) == len(match)]

            generated_literals = generated_literals.union(set(product([fluent.name],matches,[True,False])))

    return generated_literals

def generate_all_ground_literals(all_fluents):

    generated_literals = set()
    for fluent in all_fluents:
            literal_args = tuple([arg.constant_value().name for arg in fluent.args])       
            generated_literals.add((fluent.fluent().name, literal_args, True))
            generated_literals.add((fluent.fluent().name, literal_args, False))

    return generated_literals


def is_consistent(hp, he, demonstration):

    pre_state = set(demonstration[0])

    if demonstration[2] is not None:
        post_state = set(demonstration[2])
        delta = post_state.difference(pre_state)

        consistent = hp.issubset(pre_state) and delta.issubset(he) and he.issubset(post_state)
    
    else:
        consistent = not hp.issubset(pre_state)

    return consistent

def is_effect_consistent(he, demonstration):

    pre_state = set(demonstration[0])
    post_state = set(demonstration[2])
    delta = post_state.difference(pre_state)

    consistent = delta.issubset(he) and he.issubset(post_state)

    return consistent

def is_precondition_consistent(hp, demonstration):

    pre_state = set(demonstration[0])

    if demonstration[2] is not None:
        consistent = hp.issubset(pre_state)
    
    else:
        consistent = not hp.issubset(pre_state)

    return consistent


def RUP(U, example):
    return {h for h in U if h.issubset(example[0])}

def RLP(L, example):
    return {h for h in L if not h.issubset(example[0])}

def ULP(L, example):
    return {frozenset(h.intersection(example[0])) for h in L}

def UUP(U, example, L):
    new_U = {h for h in U if not h.issubset(example[0])}
    need_update = {h for h in U if h.issubset(example[0])}
    for h in need_update:
        hL = list(L)[0]
        extensions = hL.difference(example[0])
        for l in extensions:
            updated_h = h.union(set([l]))
            if not any([updated_h.issuperset(h2) for h2 in new_U]):
             new_U.add(updated_h)
    return new_U

def RLE(L, example):
    return {h for h in L if h.issubset(example[1])}

def RUE(U, example):
    delta = example[1].difference(example[0])
    return {h for h in U if delta.issubset(h)}

def ULE(L, example):
    delta = example[1].difference(example[0])
    return {h.union(delta) for h in L}

def UUE(U, example):
    return {h.intersection(example[1]) for h in U}


def run_VSLAM(all_fluents, all_actions, demonstrations):
    
    #initialization
    all_literals = {action.name:generate_all_lifted_literals(action, all_fluents) for action in all_actions}

    L_pre = {action.name:set() for action in all_actions}
    U_pre = {action.name:set() for action in all_actions}
    L_eff = {action.name:set() for action in all_actions}
    U_eff = {action.name:set() for action in all_actions}
    for action in all_actions:
        L_pre[action.name].add(frozenset(deepcopy(all_literals[action.name])))
        U_pre[action.name].add(frozenset())
        L_eff[action.name].add(frozenset())
        U_eff[action.name].add(frozenset(deepcopy(all_literals[action.name])))


    #online loop
    for demonstration in demonstrations:

        pre_state = set(demonstration[0])
        action_name = demonstration[1][0]
        
        # positive demonstration
        if demonstration[2] is not None:
            post_state = set(demonstration[2])

            pre_learning_example = (pre_state, 1)
            eff_learning_example = (pre_state, post_state)

            U_pre[action_name] = RUP(U_pre[action_name], pre_learning_example)
            L_pre[action_name] = ULP(L_pre[action_name], pre_learning_example)
            L_eff[action_name] = RLE(L_eff[action_name], eff_learning_example)
            U_eff[action_name] = RUE(U_eff[action_name], eff_learning_example)
            L_eff[action_name] = ULE(L_eff[action_name], eff_learning_example)
            U_eff[action_name] = UUE(U_eff[action_name], eff_learning_example)
            
        # negative demonstration
        else:
            pre_learning_example = (pre_state, 0)
            L_pre[action_name] = RLP(L_pre[action_name], pre_learning_example)
            U_pre[action_name] = UUP(U_pre[action_name], pre_learning_example, L_pre[action_name])
            
    return L_pre, U_pre, L_eff, U_eff


def VSLAM_initialization(all_fluents, all_actions, static_fluents, ground=False):

    L_pre = {action.name:set() for action in all_actions}
    U_pre = {action.name:set() for action in all_actions}
    L_eff = {action.name:set() for action in all_actions}
    U_eff = {action.name:set() for action in all_actions}

    if ground:
        for action in all_actions:
            all_literals = generate_all_ground_literals(all_fluents)
            L_pre[action.name].add(frozenset(deepcopy(all_literals)))
            U_pre[action.name].add(frozenset())
            L_eff[action.name].add(frozenset())
            U_eff[action.name].add(frozenset(deepcopy(all_literals)))
    else:    
        all_literals = {action.name:generate_all_lifted_literals(action, all_fluents) for action in all_actions}
        static_fluents_names = {fluent.name for fluent in static_fluents}    
        all_nonstatic_literals = {action.name:{literal for literal in all_literals[action.name] if literal[0] not in static_fluents_names} for action in all_actions}

        # L_pre = {action.name:set() for action in all_actions}
        # U_pre = {action.name:set() for action in all_actions}
        # L_eff = {action.name:set() for action in all_actions}
        # U_eff = {action.name:set() for action in all_actions}
        for action in all_actions:
            L_pre[action.name].add(frozenset(deepcopy(all_literals[action.name])))
            U_pre[action.name].add(frozenset())
            L_eff[action.name].add(frozenset())
            U_eff[action.name].add(frozenset(deepcopy(all_nonstatic_literals[action.name])))

    return L_pre, U_pre, L_eff, U_eff


def run_VSLAM_iteration(L_pre, U_pre, L_eff, U_eff, demonstration):

    pre_state = set(demonstration[0])
    action_name = demonstration[1][0]
    
    # positive demonstration
    if demonstration[2] is not None:
        post_state = set(demonstration[2])

        pre_learning_example = (pre_state, 1)
        eff_learning_example = (pre_state, post_state)

        U_pre[action_name] = RUP(U_pre[action_name], pre_learning_example)
        L_pre[action_name] = ULP(L_pre[action_name], pre_learning_example)
        L_eff[action_name] = RLE(L_eff[action_name], eff_learning_example)
        U_eff[action_name] = RUE(U_eff[action_name], eff_learning_example)
        L_eff[action_name] = ULE(L_eff[action_name], eff_learning_example)
        U_eff[action_name] = UUE(U_eff[action_name], eff_learning_example)
        
    # negative demonstration
    else:
        pre_learning_example = (pre_state, 0)
        L_pre[action_name] = RLP(L_pre[action_name], pre_learning_example)
        U_pre[action_name] = UUP(U_pre[action_name], pre_learning_example, L_pre[action_name])
            


def generate_sound_action_model(all_fluents, all_actions, L_pre, L_eff):
    sound_model = Problem("Sound Action Model")

    for fluent in all_fluents:
        sound_model.add_fluent(fluent)

    my_fluents = {fluent.name: fluent for fluent in all_fluents}
    for action in all_actions:
        if len(L_pre[action.name]) == 1 and len(L_eff[action.name]) == 1:
            hp = list(L_pre[action.name])[0]
            he = list(L_eff[action.name])[0]

            chp = get_bitwise_completement(hp)
            if len(hp.intersection(chp)) == 0:
                my_action = InstantaneousAction(action.name, {par.name:par.type for par in action.parameters})
                my_pars = {par.name: my_action.parameter(par.name) for par in action.parameters}

                for pair in combinations(my_action.parameters, 2):
                    # print(pair[0].type, pair[1].type)
                    if pair[0].type == pair[1].type:
                        my_action.add_precondition(Not(Equals(pair[0], pair[1])))
                
                for literal in hp:
                    literal_arguments = [my_pars[lit_par] for lit_par in literal[1]]
                    if literal[2]:
                        my_action.add_precondition(my_fluents[literal[0]](*literal_arguments))
                    else:
                        my_action.add_precondition(Not(my_fluents[literal[0]](*literal_arguments)))
                for literal in he:
                    literal_arguments = [my_pars[lit_par] for lit_par in literal[1]]
                    my_action.add_effect(my_fluents[literal[0]](*literal_arguments), literal[2])

                sound_model.add_action(my_action)

    return sound_model


def generate_sound_ground_action_model(all_fluents, all_actions, all_constants, L_pre, L_eff):
    sound_model = Problem("Sound Action Model")

    for fluent in all_fluents:
        sound_model.add_fluent(fluent)

    my_fluents = {fluent.name: fluent for fluent in all_fluents}
    my_constants = {constant.name: constant for constant in all_constants}
    for action in all_actions:
        if len(L_pre[action.name]) == 1 and len(L_eff[action.name]) == 1:
            hp = list(L_pre[action.name])[0]
            he = list(L_eff[action.name])[0]

            chp = get_bitwise_completement(hp)
            if len(hp.intersection(chp)) == 0:

                my_action = InstantaneousAction(action.name, {par.name:par.type for par in action.parameters})

                
            
                for literal in hp:
                    literal_arguments = [my_constants[lit_par] for lit_par in literal[1]]
                    if literal[2]:
                        my_action.add_precondition(my_fluents[literal[0]](*literal_arguments))
                    else:
                        my_action.add_precondition(Not(my_fluents[literal[0]](*literal_arguments)))

                for literal in he:
                    literal_arguments = [my_constants[lit_par] for lit_par in literal[1]]
                    my_action.add_effect(my_fluents[literal[0]](*literal_arguments), literal[2])

                sound_model.add_action(my_action)

    return sound_model


def get_subsets(fullset):
    listrep = list(fullset)
    n = len(listrep)
    return [[listrep[k] for k in range(n) if i & 1 << k] for i in range(2 ** n)]

def get_bitwise_completement(h):
    ch = frozenset([(e[0], e[1], not(e[2])) for e in h])
    return ch

def generate_version_space_effects(all_actions, L_eff, U_eff):
    V_eff = {action.name: set() for action in all_actions}
    for action in all_actions:
        hL = list(L_eff[action.name])[0]
        hU = list(U_eff[action.name])[0]

        diff = hU.difference(hL)
        for extension in get_subsets(diff):
            V_eff[action.name].add(hL.union(extension))
    
    return V_eff

# NO CONTRADICTORY EFFECTS
def generate_all_version_space_effects_smart(all_actions, L_eff, U_eff):
    V_eff = {action.name: set() for action in all_actions}
    for action in all_actions:
        hL = list(L_eff[action.name])[0]
        hU = list(U_eff[action.name])[0]

        diff = hU.difference(hL)
        for extension in get_subsets(diff):
            h = hL.union(extension)
            ch = get_bitwise_completement(h)
            if len(h.intersection(ch)) == 0:
                V_eff[action.name].add(h)
    
    return V_eff

def generate_version_space_effects(heL, heU):
    V_eff = set()

    diff = heU.difference(heL)
    for extension in get_subsets(diff):
        h = heL.union(extension)
        ch = get_bitwise_completement(h)
        if len(h.intersection(ch)) == 0:
            V_eff.add(h)
    
    return V_eff


def generate_complete_action_model(all_fluents, all_actions, U_pre, L_eff, U_eff):
    complete_model = Problem("Complete Action Model")

    for fluent in all_fluents:
        complete_model.add_fluent(fluent)

    my_fluents = {fluent.name: fluent for fluent in all_fluents}
    for action in all_actions:       
        version_num = 1    
        for hp in U_pre[action.name]:

            heL = list(L_eff[action.name])[0].difference(hp)
            heU = list(U_eff[action.name])[0].difference(hp)
            V_eff = generate_version_space_effects(heL, heU)

            for he in V_eff:
                my_action = InstantaneousAction("{}_version{}".format(action.name, version_num), {par.name:par.type for par in action.parameters})

                for pair in combinations(my_action.parameters, 2):
                    if pair[0].type == pair[1].type:
                        my_action.add_precondition(Not(Equals(pair[0], pair[1])))


                my_pars = {par.name: my_action.parameter(par.name) for par in action.parameters}
                for literal in hp:
                    literal_arguments = [my_pars[lit_par] for lit_par in literal[1]]
                    if literal[2]:
                        my_action.add_precondition(my_fluents[literal[0]](*literal_arguments))
                    else:
                        my_action.add_precondition(Not(my_fluents[literal[0]](*literal_arguments)))
        
            
                for literal in he:
                    literal_arguments = [my_pars[lit_par] for lit_par in literal[1]]
                    my_action.add_effect(my_fluents[literal[0]](*literal_arguments), literal[2])

                complete_model.add_action(my_action)
                version_num += 1

    return complete_model


def generate_unrolled_complete_action_model(all_fluents, all_actions, U_pre, L_eff, U_eff):
    pass


def generate_complete_action_model_smart(all_fluents, all_actions, U_pre, L_eff, U_eff):
    complete_model = Problem("Complete Action Model")

    V_eff = generate_all_version_space_effects_smart(all_actions, L_eff, U_eff)

    for fluent in all_fluents:
        complete_model.add_fluent(fluent)

    my_fluents = {fluent.name: fluent for fluent in all_fluents}
    for action in all_actions:       
        version_num = 1    
        for hp in U_pre[action.name]:

            optimized_V_eff = {he.difference(hp) for he in V_eff[action.name]}

            print(len(optimized_V_eff), len(V_eff[action.name]))

            for he in optimized_V_eff:
                my_action = InstantaneousAction("{}_version{}".format(action.name, version_num), {par.name:par.type for par in action.parameters})
                my_pars = {par.name: my_action.parameter(par.name) for par in action.parameters}
                for literal in hp:
                    literal_arguments = [my_pars[lit_par] for lit_par in literal[1]]
                    my_action.add_precondition(my_fluents[literal[0]](*literal_arguments))
        
            
                for literal in he:
                    literal_arguments = [my_pars[lit_par] for lit_par in literal[1]]
                    my_action.add_effect(my_fluents[literal[0]](*literal_arguments), literal[2])

                complete_model.add_action(my_action)
                version_num += 1

    return complete_model

def generate_complete_ground_action_model(all_fluents, all_actions, all_constants, U_pre, L_eff, U_eff):
    complete_model = Problem("Complete Action Model")

    for fluent in all_fluents:
        complete_model.add_fluent(fluent)

    my_fluents = {fluent.name: fluent for fluent in all_fluents}
    my_constants = {constant.name: constant for constant in all_constants}
    for action in all_actions:       
        version_num = 1    
        for hp in U_pre[action.name]:

            heL = list(L_eff[action.name])[0].difference(hp)
            heU = list(U_eff[action.name])[0].difference(hp)
            V_eff = generate_version_space_effects(heL, heU)

            for he in V_eff:
                my_action = InstantaneousAction("{}_version{}".format(action.name, version_num), {par.name:par.type for par in action.parameters})
                for literal in hp:
                    literal_arguments = [my_constants[lit_par] for lit_par in literal[1]]
                    my_action.add_precondition(my_fluents[literal[0]](*literal_arguments))
        
            
                for literal in he:
                    literal_arguments = [my_constants[lit_par] for lit_par in literal[1]]
                    my_action.add_effect(my_fluents[literal[0]](*literal_arguments), literal[2])

                complete_model.add_action(my_action)
                version_num += 1

    return complete_model


def compute_version_space_size(all_fluents, all_actions, L_pre, U_pre, L_eff, U_eff):

    for action in all_actions:
        hpL = list(L_pre[action.name])[0]
        for hp in U_pre[action.name]:

            hL = list(L_eff[action.name])[0]
            hU = list(U_eff[action.name])[0]

            diff = hU.difference(hL)
            for extension in get_subsets(diff):
                h = hL.union(extension)
                ch = get_bitwise_completement(h)
                if len(h.intersection(ch)) == 0:
                    pass
    pass


def evaluate_f1score(positives, negatives, L_pre, U_pre, L_eff, U_eff):

    tp_sound = 0
    fp_sound = 0
    tn_sound = 0
    fn_sound = 0
    tp_complete = 0 
    fp_complete = 0
    tn_complete = 0
    fn_complete = 0
    
    for demonstration in positives:
        action_name = demonstration[1][0]

        # SOUND
        hpL = list(L_pre[action_name])[0]
        heL = list(L_eff[action_name])[0]

        if is_consistent(hpL, heL, demonstration):
            tp_sound += 1
        else:
            fn_sound += 1

        # COMPLETE
        found = False
        for hp in U_pre[action_name]:
            if found:
                break

            heL = list(L_eff[action_name])[0].difference(hp)
            heU = list(U_eff[action_name])[0].difference(hp)
            V_eff = generate_version_space_effects(heL, heU)

            for he in V_eff:
                if is_consistent(hp, he, demonstration):
                    tp_complete += 1
                    found = True
                    break
        if not found:
            fn_complete += 1

    for demonstration in negatives:
        action_name = demonstration[1][0]

        # SOUND
        hpL = list(L_pre[action_name])[0]
        heL = list(L_eff[action_name])[0]

        if is_consistent(hpL, heL, demonstration):
            tn_sound += 1
        else:
            fp_sound += 1

        # COMPLETE
        version_count = 0
        consistent_count = 0
        inconsistent_count = 0
        for hp in U_pre[action_name]:
                version_count += 1
                if is_precondition_consistent(hp, demonstration):
                    consistent_count += 1
                else:
                    inconsistent_count += 1
            
        fp_complete += (version_count - consistent_count) / version_count
        tn_complete += consistent_count/version_count

    if tp_sound + fp_sound == 0:
        precision_sound = 1
    else:
        precision_sound = tp_sound / (tp_sound + fp_sound)
    recall_sound = tp_sound / (tp_sound + fn_sound)

    precision_complete = tp_complete / (tp_complete + fp_complete)
    recall_complete = tp_complete / (tp_complete + fn_complete)

    print(precision_sound, recall_sound, precision_complete, recall_complete)

    f1_sound = (2 * precision_sound * recall_sound) / (precision_sound + recall_sound)
    f1_complete = (2 * precision_complete * recall_complete) / (precision_complete + recall_complete)

    print(round(f1_sound,2), round(f1_complete,2))

    return f1_sound, f1_complete

def lift_transitions_with_map(transitions, all_actions):
    action_pars_dict = {a.name:tuple([par.name for par in a.parameters]) for a in all_actions}

    lifted_to_grounded = dict()
    lifted_transitions = set()
    for t in transitions:
        pre_state = t[0] # set of tuples (fluent_name, args, valuation)
        action = t[1] # (action_name, args)
        post_state = t[2] # set of tuples (fluent_name, args, valuation)
        
        action_name = action[0]
        action_pars = action_pars_dict[action_name]
        action_args = [arg.name for arg in t[1][1]]
        map_arg_to_par = {action_args[i]:action_pars[i] for i in range(len(action_args))}

        lifted_pre_state = set()
        for l in list(pre_state):
            literal_args = l[1]
            NARG = len(literal_args)
            if set(literal_args).issubset(action_args) and len(set(literal_args)) == len(literal_args):
            # if set(literal_args).issubset(action_args):
                lifted_args = tuple([map_arg_to_par[literal_args[i]] for i in range(NARG)])
                lifted_pre_state.add((l[0], lifted_args, l[2]))
        lifted_pre_state = tuple(sorted(lifted_pre_state))
        
        if post_state is not None:
            lifted_post_state = set()
            for l in list(post_state):
                literal_args = l[1]
                NARG = len(literal_args)
                if set(literal_args).issubset(action_args) and len(set(literal_args)) == len(literal_args):
                # if set(literal_args).issubset(action_args):
                    lifted_args = tuple([map_arg_to_par[literal_args[i]] for i in range(NARG)])
                    lifted_post_state.add((l[0], lifted_args, l[2]))
            lifted_post_state = tuple(sorted(lifted_post_state))
        else:
            lifted_post_state = None

        lifted_transitions.add((lifted_pre_state, (action_name, action_pars), lifted_post_state))
        lifted_to_grounded[(lifted_pre_state, (action_name, action_pars), lifted_post_state)] = t

    print("From {} transitions to {} lifted transitions".format(len(transitions), len(lifted_transitions)))

    return lifted_transitions, lifted_to_grounded