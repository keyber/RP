import utils
import time


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
    
    while queue.size:
        bound_max_score = len(current_tags) // 2
        # node_max = None
        score_max = -1
        # node_max_prev = None  # pour pouvoir supprimer l'élément choisi en O(1)
        for j, node in enumerate(queue):
            s = utils.score_transition(current_tags, ins.data[node])
            
            if s > score_max:
                score_max = s
                node_max = node
                node_max_prev = queue.get_iter_prev()
                
                if s >= bound_max_score * sufficient_ratio:
                    break
            
            if j == window_size:
                break
        
        current_tags = ins.data[node_max]
        sol.setH(queue.size - 1, node_max)
        queue.delete_following_node(node_max_prev)
        
    return ins.data[head]


def order_v(ins, sol, queue, window_size, sufficient_ratio, current_tags, shift):
    for i in range(queue.size//2):
        bound_max_score = len(current_tags) // 2
        
        score_max = -1
        for j, node in enumerate(queue):
            s = utils.score_transition(current_tags, ins.data[node])
            if s > score_max:
                score_max = s
                node_max0 = node
                node_max_prev = queue.get_iter_prev()
                if s >= bound_max_score * sufficient_ratio[0]:
                    break
            if j == window_size[0]:
                break
        
        queue.delete_following_node(node_max_prev)
        
        score_max = -1
        for j, node in enumerate(queue):
            s = utils.score_transition(current_tags, ins.data[node_max0] | ins.data[node])
            if s > score_max:
                score_max = s
                node_max1 = node
                node_max_prev = queue.get_iter_prev()
                if s >= bound_max_score * sufficient_ratio[1]:
                    break
            if j == window_size[1]:
                break
        
        queue.delete_following_node(node_max_prev)
        sol.setV(i + shift, node_max0, node_max1)
        current_tags = ins.data[node_max0] | ins.data[node_max1]
    
    assert queue.size <= 1


def glouton_v2(ins: utils.Instance, wh, wv1, wv2, rh, rv1, rv2):
    sol = utils.Solution(ins)
    if len(ins.H):
        # trie les images par nb de tag décroissant
        # on les placera par ordre CROISSANT pour finir par une grande image
        h = sorted(ins.H, key=lambda x: len(ins.data[x]), reverse=True)
        h = LinkedList(h)
        tags_after_h_order = order_h(ins, sol, h, window_size=wh, sufficient_ratio=rh)
    else:
        tags_after_h_order = set()
    
    if len(ins.V):
        # trie les images par nb de tag décroissant
        # on les placera par ordre DECROISSANT pour mettre une grande image à côté de la grande horizontale
        v = sorted(ins.V, key=lambda x: len(ins.data[x]), reverse=True)
        v = LinkedList(v)
        order_v(ins, sol, v, window_size=[wv1, wv2], sufficient_ratio=[rv1, rv2], current_tags=tags_after_h_order, shift=len(ins.H))
    
    return sol


def _test_glouton_v2():
    for i in range(1,5):
        ins = utils.read(i, .02)
        t = time.time()
        sol = glouton_v2(ins, wh=100, wv1=50, wv2=100, rh=.75, rv1=.5, rv2=.75)
        print("taille", len(ins.data), "temps", time.time()-t, "score glouton_v2", sol.score())



if __name__ == '__main__':
    _test_glouton_v2()