import utils
import numpy as np


class Solution:
    def __init__(self, instance):
        self.instance = instance
        self.size = len(instance.H) + len(instance.V) // 2
        self.ordre = np.empty(self.size, dtype=tuple)
        
        # indices des positions contenant des images H
        self.H = set()
        # indices des positions contenant des images V
        self.V = set()
    
    def copy(self):
        sol = Solution(self.instance)
        sol.ordre = self.ordre.copy()
        sol.H = self.H.copy()
        sol.V = self.V.copy()
        sol.size = len(sol.ordre)
        return sol
    
    def setH(self, i, img):
        assert self.instance.is_horizontal(img)
        self.ordre[i] = (img,)
        self.H.add(i)
    
    def setV(self, i, img1, img2):
        assert not self.instance.is_horizontal(img1)
        assert not self.instance.is_horizontal(img2)
        self.ordre[i] = (img1, img2)
        self.V.add(i)
    
    def score(self, verbose=False):
        assert len(self.H) + len(self.V) == self.size, "solution non complétée"
        score = 0
        d = self.instance.data
        
        current_tags = d[self.ordre[0][0]]
        if len(self.ordre[0]) == 2:
            current_tags |= d[self.ordre[0][1]]
        
        for i, tup in enumerate(self.ordre[1:]):
            new_tags = d[tup[0]]
            if len(tup) == 2:
                new_tags |= d[tup[1]]
            
            s = utils.score_transition_data(current_tags, new_tags)
            
            if verbose:
                print(s, end=" ")
            
            score += s
            current_tags = new_tags
        
        if verbose:
            print()
        return score
    
    def score_transition_ind(self, a, b):
        a = set().union(*[self.instance.data[x] for x in self.ordre[a]])
        b = set().union(*[self.instance.data[x] for x in self.ordre[b]])
        return utils.score_transition_data(a, b)
    
    def _local_score_2(self, i1, i2):
        s = 0
        
        # on prend i1 < i2
        if i1 > i2:
            i1, i2 = i2, i1
        
        if i1 > 0:
            s += self.score_transition_ind(i1 - 1, i1)
        if i2 < self.size - 1:
            s += self.score_transition_ind(i2, i2 + 1)
        
        # ne compte la transition i1 i2 qu'une fois si les images sont adjacentes
        if abs(i1 - i2) == 1:
            assert i1 + 1 == i2
            s += self.score_transition_ind(i1, i2)
        else:
            s += self.score_transition_ind(i1, i1 + 1)
            s += self.score_transition_ind(i2, i2 - 1)
        
        return s
    
    _default_accept = lambda x: True
    def swap(self, i1, i2, accept_change=_default_accept):
        if i1 == i2:
            return 0
        
        current_local_score = self._local_score_2(i1, i2)
        
        # swap
        self.ordre[i1], self.ordre[i2] = self.ordre[i2], self.ordre[i1]
        
        new_local_score = self._local_score_2(i1, i2)
        
        diff = new_local_score - current_local_score
        
        if not accept_change(diff):
            # swap back
            self.ordre[i1], self.ordre[i2] = self.ordre[i2], self.ordre[i1]
            return 0
        
        # màj H et V
        i_hor = i1 in self.H
        j_hor = i2 in self.H
        
        # rien à màj si on échange deux images de même type
        if i_hor != j_hor:
            if i_hor:
                self.H.remove(i1)
                self.V.add(i1)
                self.V.remove(i2)
                self.H.add(i2)
            else:
                self.V.remove(i1)
                self.H.add(i1)
                self.H.remove(i2)
                self.V.add(i2)
        
        return diff
    
    def swapV(self, i1, side1, i2, side2, accept_change=_default_accept):
        assert i1 in self.V and i2 in self.V
        if self.ordre[i1] == self.ordre[i2]:
            return 0
        
        current_local_score = self._local_score_2(i1, i2)
        
        # passe par des listes car les tuples sont immutables
        new_i1 = list(self.ordre[i1])
        new_i2 = list(self.ordre[i2])
        
        # swap
        new_i1[side1], new_i2[side2] = new_i2[side2], new_i1[side1]
        self.ordre[i1] = tuple(new_i1)
        self.ordre[i2] = tuple(new_i2)
        
        new_local_score = self._local_score_2(i1, i2)
        diff = new_local_score - current_local_score
        
        if not accept_change(diff):
            # swap back
            new_i1[side1], new_i2[side2] = new_i2[side2], new_i1[side1]
            self.ordre[i1] = tuple(new_i1)
            self.ordre[i2] = tuple(new_i2)
            return 0
        
        return diff


def _test_score():
    ins = utils.read(0, 1.0)
    sol = Solution(ins)
    sol.setH(0, 0)
    sol.setH(1, 3)
    sol.setV(2, 1, 2)
    assert sol.score() == 2
    utils.write("output/test", sol.ordre)
    
    print("tests passés")


if __name__ == '__main__':
    _test_score()
