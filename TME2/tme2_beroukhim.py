import tsp
import random
import numpy as np

def gen_pop(taille_pop, taille_ind):
    return [solve_rand(taille_ind) for _ in range(taille_pop)]

def solve_rand(taille_ind):
    return random.sample(range(1, taille_ind + 1), taille_ind)
    
def solve_genetic(taille_ind, len_pop, n_gen, p_mut, gen_ini, evaluation, selection, croisement, mutation):
    p = gen_ini(len_pop, taille_ind)
    fitness = np.empty(len_pop)
    indiv_max = None
    fitness_max = float("-inf")
    for _ in range(n_gen):
        # évaluations
        for i in range(len_pop):
            fitness[i] = evaluation(p[i])
            if fitness[i] > fitness_max:
                indiv_max = p[i]
                fitness_max = fitness[i]
        
        fitness /= fitness.sum()
        
        # nouvelle génération
        p_tmp = []
        for i in range(1, len_pop//2 + 1):
            i1, i2 = selection(p, fitness)
            
            i1, i2 = croisement(i1, i2)
            
            if random.random() < p_mut:
                mutation(i1)
            if random.random() < p_mut:
                mutation(i2)
            
            p_tmp.append(i1)
            p_tmp.append(i2)
            
        p = p_tmp
        
    return indiv_max

def selection_proportionel(pop, proba):
    i1, i2 = np.random.choice(len(pop), 2, p=proba)
    return pop[i1], pop[i2]

def croisement_inverse_fin(i1, i2):
    # point de crossover
    p = random.randrange(len(i1))
    
    # on peut pas: retourner le début de l'un et la fin de l'autre
    # avec rang :
    
    r1 = i1[:p]
    taken = set(r1)
    for x in i2:
        if x not in taken:
            r1.append(x)
            taken.add(x)

    r2 = i2[:p]
    taken = set(r2)
    for x in i1:
        if x not in taken:
            r2.append(x)
            taken.add(x)

    return r1, r2

def mutation_permute_deux(i):
    pos1, pos2 = np.random.randint(0, len(i), 2)
    i[pos1], i[pos2] = i[pos2], i[pos1]
    
def main():
    instance = "instances/kroA100.tsp"
    data = tsp.read_tsp_data(instance)
    cities = tsp.read_tsp(int(tsp.detect_dimension(data)), data)
    print(cities)
    print('Number of cities = ', len(cities))
    
    # individu = solve_rand(cities)
    individu = solve_genetic(
        taille_ind=len(cities),
        len_pop=20,
        n_gen=100,
        p_mut=.5,
        gen_ini=gen_pop,
        evaluation=lambda x:tsp.evaluation(x, cities),
        selection=selection_proportionel,
        croisement=croisement_inverse_fin,
        mutation=mutation_permute_deux)
    
    print(individu)
    print('EvaluationRd = ', tsp.evaluation(individu, cities))
    print('FitnessRd = ', 1 / tsp.evaluation(individu, cities))

    tsp.plottour(instance, individu, cities)
    
    #Optimal solution for KroA100.tsp
    # individuOptimal = [1, 47, 93, 28, 67, 58, 61, 51, 87, 25, 81, 69, 64, 40, 54, 2, 44, 50, 73, 68, 85, 82, 95, 13, 76,
    #                    33,
    #                    37, 5, 52, 78, 96, 39, 30, 48, 100, 41, 71, 14, 3, 43, 46, 29, 34, 83, 55, 7, 9, 57, 20, 12, 27,
    #                    86, 35, 62, 60, 77, 23, 98, 91,
    #                    45, 32, 11, 15, 17, 59, 74, 21, 72, 10, 84, 36, 99, 38, 24, 18, 79, 53, 88, 16, 94, 22, 70, 66,
    #                    26, 65, 4, 97, 56, 80, 31, 89, 42,
    #                    8, 92, 75, 19, 90, 49, 6, 63]
    # print('EvaluationOptimal = ', tsp.evaluation(individuOptimal, cities))
    # print('FitnessOptimal = ', 1 / tsp.evaluation(individuOptimal, cities))
    # tsp.plottour(instance, individuOptimal, cities)
    
if __name__ == '__main__':
    main()