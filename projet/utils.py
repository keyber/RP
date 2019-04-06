import numpy as np


file_names = ["./data/a_example.txt",
              "./data/b_lovely_landscapes.txt",
              "./data/c_memorable_moments.txt",
              "./data/d_pet_pictures.txt",
              "./data/e_shiny_selfies.txt"]


class Instance:
    def __init__(self, data, modes, H, V):
        # tags de chaque image
        self.data = data
        
        # mode de chaque image (1 si H, 0 si V)
        self._modes = modes
        
        # liste des indices H
        self.H = H
        
        # liste des indices V
        self.V = V
        
    def is_horizontal(self, i):
        return self._modes[i]

def score_transition(a, b):
    """le score est le minimum des cardinaux des ensembles :
        A inter B, A privé de B, B privé de A
    """
    inter = len(a & b)
    a_prive_b = len(a) - inter
    b_prive_a = len(b) - inter
    return min(inter, a_prive_b, b_prive_a)


class Solution:
    def __init__(self, instance):
        self.instance = instance
        self._ordre = np.empty(len(instance.H) + len(instance.V) // 2, dtype=tuple)
        
        # indices des positions contenant des images H
        self.H = set()
        # indices des positions contenant des images V
        self.V = set()
        
        self.size = len(self._ordre)
    
    def setH(self, i, img):
        self._ordre[i] = (img,)
        self.H.add(i)
    
    def setV(self, i, img1, img2):
        self._ordre[i] = (img1, img2)
        self.V.add(i)
    
    def swap(self, i1, i2):
        self._ordre[i1], self._ordre[i2] = self._ordre[i2], self._ordre[i1]
        
        # màj H et V
        i_hor = i1 in self.H
        j_hor = i2 in self.H
        
        # rien à faire si on échange deux images du même type
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
    
    def swapV(self, i1, side1, i2, side2):
        assert i1 in self.V and i2 in self.V
        
        new_i1 = list(self._ordre[i1])
        new_i2 = list(self._ordre[i2])
        
        new_i1[side1], new_i2[side2] = new_i2[side2], new_i1[side1]
        
        self._ordre[i1] = tuple(*new_i1)
        self._ordre[i2] = tuple(*new_i2)
    
    def score(self):
        score = 0
        d = self.instance.data
        current_tags = d[self._ordre[0][0]]
        if len(self._ordre[0]) == 2:
            current_tags |= d[self._ordre[0][1]]
        
        for tup in self._ordre[1:]:
            new_tags = d[tup[0]]
            if len(tup) == 2:
                new_tags |= d[tup[1]]
        
            score += score_transition(current_tags, new_tags)
            current_tags = new_tags
    
        return score
    
        
def read(file, ratio):
    """lit les premières images d'une instance de photos"""
    if type(file) == int:
        file = file_names[file]
    
    data, modes, H, V = [], [], [], []
    with open(file) as f:
        tot = int(f.readline())
        n = int(ratio * tot)
        print(ratio, "*", tot, "=", n, "images chargées")
        
        for i, line in enumerate(f.readlines()[:n]):
            line = line.split()
            mode, tags = line[0], line[2:]  # saute le nombre de tags
            data.append(frozenset(tags))
            modes.append(mode == 'H')
            
            if mode == 'H':
                H.append(i)
            else:
                V.append(i)
        
    return Instance(np.array(data, dtype=object), np.array(modes, dtype=bool), np.array(H, dtype=int), np.array(V, dtype=int))
    

def write(name, ordre):
    file = name + ".sol"
    with open(file, "w") as f:
        f.write(str(len(ordre)) + '\n')
        for x in ordre:
            f.write(" ".join(map(str, x)) + "\n")


def _test():
    from collections import Counter
    
    ins = read(0, 1)
    assert len(ins.data)==4
    for p in ins.data:
        assert 1 < len(p) < 100
    
    sol = Solution(ins)
    sol.setH(0,0)
    sol.setH(1,3)
    sol.setV(2,1,2)
    assert sol.score() == 2
    write("output/test", sol._ordre)
    
    for i in range(1, 5):
        ins = read(i, 1.0)
        for p in ins.data:
            assert 0 < len(p) < 100, len(p)
        
        tags = set().union(*ins.data)
        print("nombre de tag différents", len(tags))
        c = Counter([hash(tag) for tag in tags])
        print("nombre de tag de même hash", set(c.values()))
    
    print("tests passés")


if __name__ == '__main__':
    _test()