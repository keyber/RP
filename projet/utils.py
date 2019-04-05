import numpy as np


file_names = ["./data/a_example.txt",
              "./data/b_lovely_landscapes.txt",
              "./data/c_memorable_moments.txt",
              "./data/d_pet_pictures.txt",
              "./data/e_shiny_selfies.txt"]


def score_transition(a, b):
    """le score est le minimum des cardinaux des ensembles :
        A inter B, A privé de B, B privé de A
    """
    inter = len(a & b)
    a_prive_b = len(a) - inter
    b_prive_a = len(b) - inter
    return min(inter, a_prive_b, b_prive_a)


def score_presentation(ordre, data, modes):
    score = 0
    current_tags = data[ordre[0]]
    i=1
    if not modes[ordre[0]]:
        assert not modes[ordre[1]]
        current_tags |= data[ordre[1]]
        i+=1
        
    for i in range(i, len(ordre)):
        new_tags = data[ordre[i]]
        if not modes[ordre[i]]:
            assert not modes[ordre[i+1]]
            new_tags |= data[ordre[i+1]]
        
        score += score_transition(current_tags, new_tags)
        current_tags = new_tags
        
    return score


def read(file, ratio):
    """lit les premières images d'une instance de photos
    retourne :
    tags de chaque image,
    mode de chaque image (1 si H, 0 si V),
    liste des indices H,
    liste des indices V
    """
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
        
    return np.array(data, dtype=object), np.array(modes, dtype=bool), np.array(H, dtype=int), np.array(V, dtype=int)


def write(name, ordre, modes):
    file = name + ".sol"
    with open(file, "w") as f:
        f.write(str(len(ordre)) + '\n')
        i = 0
        while i < len(ordre):
            if modes[ordre[i]]:
                # une photo h
                f.write(str(ordre[i]) + "\n")
            else:
                # deux photos v
                f.write(str(ordre[i]) + " ")
                i += 1
                assert not modes[ordre[i]]
                f.write(str(ordre[i]) + "\n")
            i += 1


def _test():
    from collections import Counter
    
    data, modes, H, V = read(0, .75)
    for p in data:
        assert 1 < len(p) < 100
    
    write("output/test", H + V, modes)
    
    for i in range(1, 5):
        data, modes, H, V = read(i, 1.0)
        for p in data:
            assert 0 < len(p) < 100, len(p)
        
        tags = set().union(*data)
        print("nombre de tag différents", len(tags))
        c = Counter([hash(tag) for tag in tags])
        print("nombre de tag de même hash", set(c.values()))
    
    print("tests passés")


if __name__ == '__main__':
    _test()