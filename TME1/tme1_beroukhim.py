import constraint
import numpy as np

def q1():
    n = 4
    p = constraint.Problem()
    var_names = list(range(1, n + 1))
    var_domaines = [["rouge", "bleu"], ["bleu", "vert"], ["bleu", "vert"], ["rouge"]]
    for name, dom in zip(var_names, var_domaines):
        p.addVariable(name, dom)
    adjacences = [(1, 2), (1, 3), (1, 4),
                  (2, 3),
                  (3, 4)]
    
    for x, y in adjacences:
        p.addConstraint(constraint.AllDifferentConstraint(), [x, y])
    
    return p.getSolutions()


assert q1() == []


def q2():
    n = 4
    p = constraint.Problem()
    var_names = list(range(1, n + 1))
    
    var_domaines = ["rouge", "vert", "bleu"]
    p.addVariables(var_names, var_domaines)
    adjacences = [(1, 2), (1, 3), (1, 4),
                  (2, 3),
                  (3, 4)]
    
    for x, y in adjacences:
        p.addConstraint(constraint.AllDifferentConstraint(), [x, y])
    
    return p.getSolutions()


assert len(q2()) == 6



def construct_tree(solutions):
    tree = {}
    if len(solutions) == 0:
        return tree
    
    n = len(solutions[0].keys())
    
    def rec(depth, curr_sols):
        if depth==n:
            return curr_sols
        
        valeurs_possibles = [s[depth] for s in curr_sols]
        res = {}
        for val in valeurs_possibles:
            solutions_restantes = [s for s in curr_sols if s[depth]==val]
            res[val] = rec(depth+1, solutions_restantes)
        return res
    
    return rec(0, solutions)

def branchAndBound():
    n = 4
    vars_id_to_name = ["Z1", "Z2", "Z3", "Z4"]
    vars_id = list(range(4))
    dom_id_to_name = ["rouge", "vert", "bleu"]
    doms_id = list(range(3))
    utilites = np.array([
        [1.0,.3, .8],
        [.2, .6,  1],
        [1,  .7, .4],
        [.5,  1, .9]])
    
    p = constraint.Problem()
    p.addVariables(vars_id, doms_id)

    adjacences = [(1, 2), (1, 3), (1, 4),
                  (2, 3),
                  (3, 4)]

    for x, y in adjacences:
        p.addConstraint(constraint.AllDifferentConstraint(), [x-1, y-1])

    solutions = p.getSolutions()
    #ecrit les solutions sous forme d'arbre
    arbre = construct_tree(solutions)
    def rec_aff(depth, arbre):
        if depth==n:
            return
        for k, branche in arbre.items():
            print("\t"*depth + str(k))
            rec_aff(depth+1, branche)
        
    #rec_aff(0, arbre)

    def utilite1(affectation):
        #min
        return min((utilites[i][affectation[i]] for i in range(len(affectation)))
                    , default=float("+inf"))
    
    def utilite2(affectation):
        #softmin
        return np.prod([utilites[i][affectation[i]] for i in range(len(affectation))])
    
    moins_inf = float("-inf")
    def rec(depth, curr_affectations, arbre_poss, alpha=moins_inf):
        if depth==n:
            return curr_affectations, utilite2(curr_affectations)
        
        if utilite2(curr_affectations) < alpha:
            return curr_affectations, moins_inf
        
        sol_max = None
        
        for aff, branche in arbre_poss.items():
            sol, val = rec(depth+1, curr_affectations+[aff], branche, alpha)
            if val > alpha:
                alpha = val
                sol_max = sol
            
        
        return sol_max, alpha
        
    return rec(0, [], arbre)
    
print(branchAndBound())