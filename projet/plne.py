from gurobipy import *
import utils
import solution
from time import time
import numpy as np


# noinspection PyArgumentList
def _ins_to_plne(first, ins: utils.Instance, relaxation_lin, verbose=False):
    # rajoute un sommet fictif pour lequel tous les coûts entrants et sortants sont nuls
    # on obtient alors facilement la chaîne optimale en enlevant le sommet fictif
    n = len(ins.data) + 1
    V = range(n)
    m = Model()
    m.setParam('OutputFlag', False)
    t = time()

    # coefficients de la fonction objectif
    c = np.empty((n, n), dtype=int)
    for i in V[:-1]:
        for j in V[i + 1 : -1]:
            s = utils.score_transition_data(ins.data[i], ins.data[j])
            c[i, j] = s
            c[j, i] = s
    
    # coefficients du sommet fictif
    for i in V[:-1]:
        c[n - 1, i] = utils.score_transition_data(first, ins.data[i])
        c[i, n - 1] = 0
        
    if verbose:
        print("score", round(time()-t, 1))
        t = time()
    
    # déclaration des variables de décision
    x = np.empty((n,n), dtype=object)
    for i in V:
        for j in V:
            if relaxation_lin:
                x[i][j] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1)
            else:
                x[i][j] = m.addVar(vtype=GRB.BINARY)
    for i in V:
        m.addConstr(x[i][i]==0)
    
    # sous tours - variables
    z = np.empty((n,n), dtype=object)
    for i in V:
        for j in V:
            z[i][j] = m.addVar(vtype=GRB.CONTINUOUS, lb=0)
            if i == j or j == 0:
                m.addConstr(z[i][j]==0)
    
    if verbose:
        m.update()
        print("vars", round(time()-t, 1))
        t = time()
    
    # définition de l'objectif
    m.setObjective(quicksum(c[i][j] * x[i][j] for i in V for j in V), GRB.MAXIMIZE)
    
    if verbose:
        m.update()
        print("obj", round(time()-t, 1))
        t = time()
    
    # définition des contraintes
    for i in V:
        m.addConstr(quicksum(x[i][j] for j in V), GRB.EQUAL, 1, "ContrainteA%d" % i)
    for j in V:
        m.addConstr(quicksum(x[i][j] for i in V) == 1)
    
    # inutile :
    # for i in V:
    #     for j in V:
    #         if i!=j:
    #             m.addConstr(x[i][j] + x[j][i] <= 1)
                
    # sous tours - contraintes
    m.addConstr(quicksum(z[0][j] for j in V) == n - 1)
    
    for i in V[1:]:
        m.addConstr(quicksum(z[i][j] for j in V) + 1 == quicksum(z[j][i] for j in V))
    
    for i in V:
        for j in V[1:]:
            if i!=j:
                m.addConstr(z[i][j] + z[j][i] <= (n - 1) * (x[i][j] + x[j][i]))
    
    if verbose:
        m.update()
        print("constr", round(time()-t, 1))
        t = time()
    
    # maj du modèle pour intégrer les variables
    m.optimize()
    
    if verbose:
        print("optimize", round(time()-t, 1))

    #todo il faut garder [la référence de m ?] si on veut retourner les variables
    return [[j.x for j in i] for i in x]

def _plne_to_sol(ins, instanciations):
    def find_next(current):
        # noinspection PyTypeChecker
        return instanciations[current].index(1)
    
    curr = find_next(len(ins.data))
    res = [curr]
    
    for _ in range(len(ins.data)-1):
        curr = find_next(curr)
        res.append(curr)
    
    return res

def _plne_to_sol_relaxed(ins, instanciations):
    def find_next(current, used):
        m = -1
        argmax = None
        for ind, val in enumerate(instanciations[current]):
            if val > m and ind not in used:
                m = val
                argmax = ind
        return argmax
    
    curr = len(ins.data)
    ens = {curr}
    
    curr = find_next(len(ins.data), ens)
    ens.add(curr)
    res = [curr]
    
    for _ in range(len(ins.data)-1):
        curr = find_next(curr, ens)
        ens.add(curr)
        res.append(curr)
    
    return res

def _ins_to_sol(previous_tags, ins, relaxation_lin, verbose):
    instanciations = _ins_to_plne(previous_tags, ins, relaxation_lin, verbose=verbose)
    
    t = time()
    if relaxation_lin:
        sol = _plne_to_sol_relaxed(ins, instanciations)
    else:
        sol = _plne_to_sol(ins, instanciations)
    
    if verbose:
        print("traduction", round(time() - t, 1))
    return sol

def plne_h(pb: utils.Instance, n, relaxation_lin, verbose=False):
    sol = solution.Solution(pb)

    previous_tags = set()
    for i in range(0, len(pb.data), n):
        sub_pb = utils.Instance.create_instance_h(pb.data[i: i+n])
        sub_res = _ins_to_sol(previous_tags, sub_pb, relaxation_lin, verbose=verbose)
        for j, x in enumerate(sub_res, i):
            sol.setH(j, i+x)
        
        previous_tags = pb.data[sub_res[-1]]
    return sol

def _test_plne():
    import matplotlib.pyplot as plt
    x = [1, 10, 15, 20]
    times = []
    scores=[]
    for n in x:
        ins = utils.read(1, 5000)
        t = time()
        sol = plne_h(ins, n=n, relaxation_lin=True, verbose=False)
        assert len(set(sol.ordre)) == len(sol.ordre)
        assert len(sol.V) + len(sol.H) == len(sol.ordre)
        print("taille", len(ins.data), "temps", round(time()-t, 1), "score glouton_v2", sol.score())
        times.append(time()-t)
        scores.append(sol.score())
    
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    ax1.plot(x, times)
    ax2.plot(x, scores, color="green")
    plt.show()

if __name__ == '__main__':
    _test_plne()
