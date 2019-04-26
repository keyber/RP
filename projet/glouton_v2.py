import utils
import solution
from time import time


class LinkedList:
    """implémentation d'une LinkedList simple car collections.deque ne permet pas
    la suppression d'un élément qcq en O(1)"""
    
    def __init__(self, a):
        self.size = len(a)
        
        curr = None
        for x in reversed(a):
            curr = [x, curr]
        
        self._head = curr
    
    def __iter__(self):
        self._curr = None
        self._prev = None
        return self
    
    def __next__(self):
        if self._curr is None:
            self._prev = None
            self._curr = self._head
        else:
            self._prev = self._curr
            self._curr = self._curr[1]
            
        if self._curr is None:
            raise StopIteration
        return self._curr[0]
    
    def get_iter_prev(self):
        """retourne le noeud précédant le noeud de l'itération actuelle
        permet de supprimer le noeud actuel via delete_following_node"""
        return self._prev
    
    def delete_following_node(self, node):
        if node is None:
            self.pop_head()
        else:
            node[1] = node[1][1]
            self.size -= 1
    
    def pop_head(self):
        self.size -= 1
        res = self._head[0]
        self._head = self._head[1]
        return res


def order_h(ins, sol, queue, window_size, sufficient_ratio):
    """retourne les tags de la dernière image de présentation en cours"""
    head = queue.pop_head()
    sol.setH(queue.size, head)
    current_tags = ins.data[head]
    cpt = 0
    
    while queue.size:
        bound_max_score = len(current_tags) // 2
        node_max = None
        score_max = -1
        node_max_prev = None  # pour pouvoir supprimer l'élément choisi en O(1)
        for j, node in enumerate(queue):
            s = utils.score_transition_data(current_tags, ins.data[node])
            
            if s > score_max:
                score_max = s
                node_max = node
                node_max_prev = queue.get_iter_prev()
                
                if s >= bound_max_score * sufficient_ratio:
                    cpt += 1
                    break
            
            if j == window_size:
                break
        
        current_tags = ins.data[node_max]
        sol.setH(queue.size - 1, node_max)
        queue.delete_following_node(node_max_prev)
        
    return ins.data[head],cpt


def order_v(ins, sol, queue, window_size, sufficient_ratio, current_tags, shift):
    cpt1, cpt2 = 0, 0
    for i in range(queue.size//2):
        bound_max_score = len(current_tags) // 2

        node_max0 = None
        node_max_prev = None  # pour pouvoir supprimer l'élément choisi en O(1)
        score_max = -1
        for j, node in enumerate(queue):
            s = utils.score_transition_data(current_tags, ins.data[node])
            if s > score_max:
                score_max = s
                node_max0 = node
                node_max_prev = queue.get_iter_prev()
                if s >= bound_max_score * sufficient_ratio[0]:
                    cpt1 += 1
                    break
            if j == window_size[0]:
                break
        
        queue.delete_following_node(node_max_prev)

        node_max1 = None
        score_max = -1
        for j, node in enumerate(queue):
            s = utils.score_transition_data(current_tags, ins.data[node_max0] | ins.data[node])
            if s > score_max:
                score_max = s
                node_max1 = node
                node_max_prev = queue.get_iter_prev()
                if s >= bound_max_score * sufficient_ratio[1]:
                    cpt2 += 1
                    break
            if j == window_size[1]:
                break
        
        queue.delete_following_node(node_max_prev)
        sol.setV(i + shift, node_max0, node_max1)
        current_tags = ins.data[node_max0] | ins.data[node_max1]
    
    assert queue.size <= 1
    return cpt1, cpt2


def glouton_v2(ins: utils.Instance, wh, wv1, wv2, rh=1, rv1=1, rv2=1):
    cpt = [0] * 3
    sol = solution.Solution(ins)
    if len(ins.H):
        # trie les images par nb de tag décroissant
        # on les placera par ordre CROISSANT pour finir par une grande image
        h = sorted(ins.H, key=lambda x: len(ins.data[x]), reverse=True)
        h = LinkedList(h)
        tags_after_h_order, n_breaks = order_h(ins, sol, h, window_size=wh, sufficient_ratio=rh)
        cpt[0] += n_breaks
    else:
        tags_after_h_order = set()
    
    if len(ins.V):
        # trie les images par nb de tag décroissant
        # on les placera par ordre DECROISSANT pour mettre une grande image à côté de la grande horizontale
        v = sorted(ins.V, key=lambda x: len(ins.data[x]), reverse=True)
        v = LinkedList(v)
        n_breaks1, n_breaks2 = order_v(ins, sol, v, window_size=[wv1, wv2], sufficient_ratio=[rv1, rv2], current_tags=tags_after_h_order, shift=len(ins.H))
        cpt[1] += n_breaks1
        cpt[2] += n_breaks2
    print("early cuts:", cpt)
    return sol


def _test_glouton_v2():
    for i in range(1,5):
        ins = utils.read(i, .02)
        t = time()
        sol = glouton_v2(ins, wh=100, wv1=50, wv2=100)
        assert len(set(sol.ordre)) == len(sol.ordre)
        assert len(sol.V) + len(sol.H) == len(sol.ordre)
        print("taille", len(ins.data), "temps", time() - t, "score glouton_v2", sol.score())

def _plot():
    import matplotlib.pyplot as plt
    x = range(10, 5011, 1000)
    times = []
    scores = []
    for n in x:
        ins = utils.read(1, n)
        t = time()
        sol = glouton_v2(ins, wh=1000, wv1=1000, wv2=1000)
        print("taille", len(ins.data), "temps", round(time()-t, 1), "score glouton_v2", sol.score())
        times.append(time()-t)
        scores.append(sol.score())
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    ax1.plot(x, times)
    ax2.plot(x, scores, color="green")
    plt.show()

if __name__ == '__main__':
    # _test_glouton_v2()
    _plot()