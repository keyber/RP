import re
import numpy as np
import random
import matplotlib.pyplot as plt


#Function to read the content of a .tsp file from the tsplib library

def read_tsp_data(tsp_name):
    tsp_name = tsp_name
    with open(tsp_name) as f:
        content = f.read().splitlines()
        cleaned = [x.lstrip() for x in content if x != ""]
        return cleaned


#Function to obtain the number of cities from the instance

def detect_dimension(in_list):
    non_numeric = re.compile(r'[^\d]+')
    for element in in_list:
        if element.startswith("DIMENSION"):
            return non_numeric.sub("", element)


#Function to get the list of cities

def get_cities(list, dimension):
    cities_set = []
    dimension = int(dimension)
    for item in list:
        for num in range(1, dimension + 1):
            if item.startswith(str(num)):
                index, space, rest = item.partition(' ')
                if rest not in cities_set:
                    cities_set.append(rest)
    return cities_set


#Function to brake each coordinate to a tuple

def city_tup(list):
    cities_tups = []
    for item in list:
        first_coord, space, second_coord = item.partition(' ')
        cities_tups.append((float(first_coord.strip()), float(second_coord.strip())))
    return cities_tups


#Function to get the cities as a dictionary

def create_cities_dict(cities_tups):
    return dict(zip((range(1, len(cities_tups) + 1)), cities_tups))


def read_tsp(dimension, data):
    cities_dict = create_cities_dict(city_tup(get_cities(data, dimension)))
    return cities_dict



def evaluation(individu, cities):
    distance = 0.0
    for i in range(0, len(individu)):
        fromCity = individu[i]
        if i + 1 < len(individu):
            toCity = individu[i + 1]
        else:
            toCity = individu[0]
        xDiff = cities.get(fromCity)[0] - cities.get(toCity)[0]
        yDiff = cities.get(fromCity)[1] - cities.get(toCity)[1]
        distance += round(np.sqrt((xDiff ** 2) + (yDiff ** 2)))
    return 1/distance


#Function to a display a tour

def plottour(instance, individu, cities):
    plt.figure(figsize=(8, 10), dpi=100)
    plt.title('Traveling Salesman : ' + instance)
    for point in cities.values():
        plt.plot(point[0], point[1], 'ro')
    x = []
    y = []
    for i in range(0, len(individu)):
        x.append(cities.get(individu[i])[0])
        y.append(cities.get(individu[i])[1])
    
    #retour ville de départ
    x.append(cities.get(individu[0])[0])
    y.append(cities.get(individu[0])[1])
    
    plt.plot(x, y, color='black', lw=1)
    
    #plt.ion()
    plt.show()


#plt.pause(5)

def _main():
    instance = "instances/kroA100.tsp"
    data = read_tsp_data(instance)
    nbCities = int(detect_dimension(data))
    cities = read_tsp(nbCities, data)
    print(cities)
    print('Number of cities = ', nbCities)
    #Random solution
    individu = random.sample(range(1, nbCities + 1), nbCities)
    print(individu)
    print('EvaluationRd = ', evaluation(individu, cities))
    print('FitnessRd = ', 1 / evaluation(individu, cities))
    #Optimal solution for KroA100.tsp
    individuOptimal = [1, 47, 93, 28, 67, 58, 61, 51, 87, 25, 81, 69, 64, 40, 54, 2, 44, 50, 73, 68, 85, 82, 95, 13, 76,
                       33,
                       37, 5, 52, 78, 96, 39, 30, 48, 100, 41, 71, 14, 3, 43, 46, 29, 34, 83, 55, 7, 9, 57, 20, 12, 27,
                       86, 35, 62, 60, 77, 23, 98, 91,
                       45, 32, 11, 15, 17, 59, 74, 21, 72, 10, 84, 36, 99, 38, 24, 18, 79, 53, 88, 16, 94, 22, 70, 66,
                       26, 65, 4, 97, 56, 80, 31, 89, 42,
                       8, 92, 75, 19, 90, 49, 6, 63]
    print('EvaluationOptimal = ', evaluation(individuOptimal, cities))
    print('FitnessOptimal = ', 1 / evaluation(individuOptimal, cities))
    
    plottour(instance, individu, cities)
    plottour(instance, individuOptimal, cities)

if __name__ == '__main__':
    _main()
