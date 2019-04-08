import utils
import solution
import random


def stochastic_descent(sol: solution.Solution, n_iter, only_if_better=True, ratioHV=None, verbose=False):
    if ratioHV is None:
        ratioHV = 1 - len(sol.V) / sol.size
    if len(sol.V) == 0:
        ratioHV = 1
    
    curr_score = sol.score()
    sol_max = sol.copy()
    score_max = curr_score

    if verbose:
        print("Stochastic descent ini", score_max)
    
    for _ in range(n_iter):
        if random.random() < ratioHV:
            i1, i2 = random.sample(range(sol.size), 2)
            diff = sol.swap(i1, i2, only_if_better=only_if_better)
        else:
            i1, i2 = random.sample(sol.V, 2)
            side1, side2 = random.randint(0, 1), random.randint(0, 1)
            diff = sol.swapV(i1, side1, i2, side2, only_if_better=only_if_better)
        
        curr_score += diff
        if curr_score > score_max:
            score_max = curr_score
            if verbose:
                print("Stochastic descent", score_max)
            sol_max = sol.copy()
    
    if verbose:
        print()
    assert sol_max.score() == score_max, str(sol_max.score()) + " " + str(score_max)
    return sol_max, score_max

def _test_swap():
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
    sol.swap(0, 2, only_if_better=True)
    assert sol.score() == 7
    
    sol.swap(0, 2)
    assert sol.score() == 6
    sol.swap(0, 3)
    assert sol.score() == 4
    
    for _ in range(10):
        working_sol = sol.copy()
        best_sol, best_score = stochastic_descent(working_sol, 10000)
        print("optimum trouvé", best_score)
        assert best_score>=6, "score found=" + str(best_score) + " retry ?"
    
    working_sol = sol.copy()
    best_sol, best_score = stochastic_descent(working_sol, 10000, only_if_better=False)
    assert best_score==8, "score found=" + str(best_score) + " retry ?"
    

if __name__ == '__main__':
    _test_swap()



