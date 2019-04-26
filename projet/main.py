import utils
from glouton_v2 import glouton_v2
from simulated_annealing import simulated_annealing
import time


def main():
    score_tot = 0
    for i in range(5):
        t = time.time()
        ins = utils.read(i, 1.0)
        print("taille instance", len(ins.data))
        
        # faire varier la taille des fenêtres pour de meilleurs perf
        sol = glouton_v2(ins, wh=100, wv1=50, wv2=100)
        score = sol.score()
        print("glouton v2 temps", time.time() - t, "score", score)
        t = time.time()
        
        # augmenter le nombre d'itérations et faire varier la température pour de meilleurs perf
        solmax, score = simulated_annealing(sol, 10000, temperature=score/sol.size*.001)
        print("descente temps", time.time() - t, "score", score)
        score_tot += score
        print()
        
        utils.write("output/sol" + str(i), solmax.ordre)
    print("score final ", score_tot)

main()
