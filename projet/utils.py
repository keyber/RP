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
    
    @staticmethod
    def create_instance_h(data):
        return Instance(data,[1]*len(data),range(len(data)), [])
    
    def is_horizontal(self, i):
        return self._modes[i]

def score_transition_data(a, b):
    """le score est le minimum des cardinaux des ensembles :
        A inter B, A privé de B, B privé de A
    """
    inter = len(a & b)
    a_prive_b = len(a) - inter
    b_prive_a = len(b) - inter
    return min(inter, a_prive_b, b_prive_a)


        
def read(file, n):
    """lit les premières images d'une instance de photos"""
    if type(file) == int:
        file = file_names[file]
    
    data, modes, H, V = [], [], [], []
    with open(file) as f:
        tot = int(f.readline())
        if type(n) == float:
            n = int(n * tot)
        elif n==1:
            print("use float for ratio, int for exact number")
        
        for i, line in enumerate(f.readlines()[:n]):
            line = line.split()
            mode, tags = line[0], line[2:]  # saute le nombre de tags
            data.append(set(tags)) # frozenset est 10% moins bien, hash(tags) 5% mieux
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


def _test_data():
    from collections import Counter
    
    ins = read(0, .75)
    assert len(ins.data)==3
    
    ins = read(0, 4)
    assert len(ins.data)==4
    
    for p in ins.data:
        assert 0 < len(p) < 100
    
    for i in range(1, 5):
        ins = read(i, 1.0)
        for p in ins.data:
            assert 0 < len(p) < 100, len(p)
        
        tags = set().union(*ins.data)
        print("nombre de tag différents", len(tags))
        c = Counter([hash(tag) for tag in tags])
        print("nombre de tag de même hash", set(c.values()))
    
    
if __name__ == '__main__':
    _test_data()