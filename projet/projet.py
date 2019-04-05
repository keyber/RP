import numpy as np
import utils


def glouton(data, modes, H, V):
    """complexité : n^2"""
    ordre = np.empty(len(H) + len(V), dtype=int)
    
    # commence par la première photo horizontale
    ordre[0] = H[0]
    current_tags = data[ordre[0]]
    
    set_V = set(V)
    set_HV = set(H) | set_V
    set_HV.remove(ordre[0])
    
    for i in range(1, len(ordre)):
        # meilleure transition directe
        ordre[i] = max(set_HV, key=lambda x: utils.score_transition(current_tags, data[x]))
        
        set_HV.remove(ordre[i])
        new_tags = data[ordre[i]]
        
        if not modes[ordre[i]]:
            set_V.remove(ordre[i])
            
            # ajoute la deuxième image verticale
            ordre[i + 1] = max(set_V, key=lambda x: utils.score_transition(current_tags, new_tags | data[x]))
            
            set_HV.remove(ordre[i + 1])
            set_V.remove(ordre[i + 1])
            new_tags |= data[ordre[i + 1]]
            
            if len(set_V) == 1:
                # si il ne reste plus qu'une image verticale on la supprime car on ne peut pas l'insérer
                # enlever de set_V ne sert à rien car plus utilisé
                set_HV.remove(iter(set_V))
            i += 1
        
        current_tags = new_tags
        i += 1
    
    return ordre


def glouton_v2(data, modes, H, V, window_size, score_factor):
    pass

