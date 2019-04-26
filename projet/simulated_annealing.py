import utils
import solution
import random
import numpy as np
from time import time


def simulated_annealing(sol: solution.Solution, n_iter, temperature, ratioHV=None, verbose=False):
    if ratioHV is None:
        ratioHV = 1 - len(sol.V) / sol.size
    if len(sol.V) <= 1:
        ratioHV = 1
    
    if temperature < 1e-9:
        accept_change = lambda diff: True
    else:
        # la référence de i définie après est capturée
        accept_change = lambda diff: diff>=0 or np.exp(diff/temperature * i/n_iter) > random.random()
    
    curr_score = sol.score()
    sol_max = sol.copy()
    score_max = curr_score

    if verbose:
        print("Stochastic descent ini", score_max)
    
    for i in range(1, n_iter + 1):
        if random.random() < ratioHV:
            i1, i2 = random.sample(range(sol.size), 2)
            score_change = sol.swap(i1, i2, accept_change=accept_change)
        else:
            i1, i2 = random.sample(sol.V, 2)
            side1, side2 = random.randint(0, 1), random.randint(0, 1)
            score_change = sol.swapV(i1, side1, i2, side2, accept_change=accept_change)
            
        if score_change and verbose:
            print("score_change", score_change, np.exp(score_change/temperature * i/n_iter))
            
        curr_score += score_change
        if curr_score > score_max:
            score_max = curr_score
            if verbose:
                print("Stochastic descent", score_max)
            sol_max = sol.copy()
    
    if verbose:
        print()
    assert sol_max.score() == score_max, str(sol_max.score()) + " " + str(score_max)
    return sol_max, score_max

def _test_descent():
    ins = utils.read("./data/test.txt", 10)
    sol = solution.Solution(ins)
    i = 0
    for x in ins.H:
        sol.setH(i, x)
        i += 1
    for x in range(0, len(ins.V), 2):
        sol.setV(i, ins.V[x], ins.V[x + 1])
        i += 1
    assert sol.score() == 6
    sol.swap(0, 2)
    
    assert sol.score() == 7
    sol.swap(0, 2, accept_change=lambda diff: diff > 0)
    assert sol.score() == 7
    
    sol.swap(0, 2)
    assert sol.score() == 6
    sol.swap(0, 3)
    assert sol.score() == 4
    
    for i in range(10):
        working_sol = sol.copy()
        best_sol, best_score = simulated_annealing(working_sol, 1000, temperature=i)
        print("température", i, "optimum trouvé", best_score)
        assert best_score>=6, "score found=" + str(best_score) + " retry ?"
    
def _plot():
    import matplotlib.pyplot as plt
    from glouton_v2 import glouton_v2
    ins = utils.read(1, 1000)
    sol = glouton_v2(ins, 100, 100, 100)
    
    x = range(0, int(1e5+1), int(1e4))
    times = []
    scores = []
    for n in x:
        t = time()
        solmax, score = simulated_annealing(sol, n, temperature=.0001)
        print("descente temps", time() - t, "score", score)
        times.append(time() - t)
        scores.append(score)
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    ax1.plot(x, times)
    ax2.plot(x, scores, color="green")
    plt.show()


if __name__ == '__main__':
    # _test_descent()
    _plot()
