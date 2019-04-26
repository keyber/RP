import utils
import solution
from time import time


def glouton(ins: utils.Instance):
    """complexité : n^2"""
    sol = solution.Solution(ins)
    
    # ensemble des images verticales encore non utilisées
    set_V = set(ins.V)
    
    # ensemble des images encore non utilisées
    set_HV = set(ins.H) | set_V
    
    if len(ins.H):
        # commence par la première photo horizontale si il y en a
        sol.setH(0, ins.H[0])
        current_tags = ins.data[ins.H[0]]
        set_HV.remove(ins.H[0])
    else:
        # sinon par les deux premières photos verticales
        assert len(ins.V)>=2
        sol.setV(0, ins.V[0], ins.V[1])
        current_tags = ins.data[ins.V[0]] | ins.data[ins.V[1]]
        set_HV.remove(ins.V[0])
        set_HV.remove(ins.V[1])
        set_V.remove(ins.V[0])
        set_V.remove(ins.V[1])
    
    
    for i in range(1, sol.size):
        # choisit la meilleure transition directe
        greedy = max(set_HV, key=lambda x: utils.score_transition_data(current_tags, ins.data[x]))
        
        set_HV.remove(greedy)
        new_tags = ins.data[greedy]
        
        if ins.is_horizontal(greedy):
            sol.setH(i, greedy)
        else:
            set_V.remove(greedy)
            
            # ajoute une deuxième image verticale
            greedy2 = max(set_V, key=lambda x: utils.score_transition_data(current_tags, new_tags | ins.data[x]))
            
            set_HV.remove(greedy2)
            set_V.remove(greedy2)
            new_tags |= ins.data[greedy2]
            
            if len(set_V) == 1:
                # si il ne reste plus qu'une image verticale on la supprime car on ne peut pas l'insérer
                # enlever de set_V ne sert à rien car plus utilisé
                set_HV.remove(next(iter(set_V)))
            
            sol.setV(i, greedy, greedy2)
        
        current_tags = new_tags
    
    return sol


def _test_glouton():
    for i in range(1,5):
        ins = utils.read(i, .02)
        t = time()
        sol = glouton(ins)
        assert len(set(sol.ordre)) == len(sol.ordre)
        assert len(sol.V) + len(sol.H) == len(sol.ordre)
        print("taille", len(ins.data), "temps", time() - t, "score glouton", sol.score())

def _plot():
    import matplotlib.pyplot as plt
    x = range(10, 5011, 1000)
    times = []
    scores = []
    for n in x:
        ins = utils.read(1, n)
        t = time()
        sol = glouton(ins)
        print("taille", len(ins.data), "temps", round(time()-t, 1), "score glouton_v2", sol.score())
        times.append(time()-t)
        scores.append(sol.score())
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    ax1.plot(x, times)
    ax2.plot(x, scores, color="green")
    plt.show()
    
if __name__ == '__main__':
    # _test_glouton()
    _plot()