import math
import random
from utils import calculate_score

# basic Hill Climbing
def hill_climbing_basic(solution, scores, total_days, libs_dict):
    best_score = calculate_score(solution, scores, total_days, libs_dict)
    l = len(solution)
    best_solution = solution
    there_is_best = True
    while there_is_best:
        there_is_best = False
        for i in range(1, l - 1):
            for k in range(i + 1, l):
                n = best_solution[:i] + [best_solution[k]] + best_solution[i + 1:k] + [best_solution[i]] + best_solution[k + 1:]
                s = calculate_score(n, scores, total_days, libs_dict)
                if s > best_score:
                    best_score = s
                    best_solution = n
                    there_is_best = True
                    break

    return best_solution, best_score

# Hill Climbing with Steepest Ascent    
def hill_climbing_steepest(solution, scores, total_days, libs_dict):
    best_score = calculate_score(solution, scores, total_days, libs_dict)
    l = len(solution)
    best_solution = solution
    there_is_best = True
    while there_is_best:
        there_is_best = False
        for i in range(1, l - 1):
            for k in range(i + 1, l):
                n = best_solution[:i] + [best_solution[k]] + best_solution[i + 1:k] + [best_solution[i]] + best_solution[k + 1:]
                s = calculate_score(n, scores, total_days, libs_dict)
                if s > best_score:
                    best_score = s
                    best_solution = n
                    there_is_best = True

    return best_solution, best_score

# Simulated Annealing
def simulated_annealing(solution, scores, total_days, libs_dict, max_iter, T, alpha):
    score = calculate_score(solution, scores, total_days, libs_dict)
    best_score = score
    best_solution = solution
    current_solution = solution
    current_score = score
    for _ in range(max_iter):
        i = random.randint(0, len(current_solution) - 2)
        k = random.randint(i + 1, len(current_solution) - 1)
        neighbor = current_solution[:i] + [current_solution[k]] + current_solution[i + 1:k] + [current_solution[i]] + current_solution[k + 1:]
        new_score = calculate_score(neighbor, scores, total_days, libs_dict)
        delta = new_score - current_score
        if delta > 0:
            current_solution = neighbor
            current_score = new_score
            if new_score > best_score:
                best_score = new_score
                best_solution = neighbor
        else:
            if random.random() < math.exp(delta / T):
                current_solution = neighbor
                current_score = new_score
        T = T * alpha

    return best_solution, best_score

# Tabu Search 
def tabu_search(solution, scores, total_days, libs_dict, max_iter, tenure):
    score = calculate_score(solution, scores, total_days, libs_dict)
    best_score = score
    best_solution = solution
    current_solution = solution
    current_score = score
    tabu_list = []
    for _ in range(max_iter):
        i = random.randint(0, len(current_solution) - 2)
        k = random.randint(i + 1, len(current_solution) - 1)
        neighbor = current_solution[:i] + [current_solution[k]] + current_solution[i + 1:k] + [current_solution[i]] + current_solution[k + 1:]
        new_score = calculate_score(neighbor, scores, total_days, libs_dict)
        if neighbor in tabu_list or new_score <= current_score*0.9:
            continue
        if new_score > best_score:
            best_score = new_score
            best_solution = neighbor
        current_solution = neighbor
        current_score = new_score
        tabu_list.append(neighbor)
        if len(tabu_list) > tenure:
            tabu_list.pop(0)

    return best_solution, best_score


# Simulated Annealing with Tabu Search
def simulated_annealing_tabu_search(solution, scores, total_days, libs_dict, max_iter, T, alpha, tenure):
    score = calculate_score(solution, scores, total_days, libs_dict)
    best_score = score
    best_solution = solution
    current_solution = solution
    current_score = score
    tabu_list = []
    for _ in range(max_iter):
        i = random.randint(0, len(current_solution) - 2)
        k = random.randint(i + 1, len(current_solution) - 1)
        neighbor = current_solution[:i] + [current_solution[k]] + current_solution[i + 1:k] + [current_solution[i]] + current_solution[k + 1:]
        new_score = calculate_score(neighbor, scores, total_days, libs_dict)
        if neighbor in tabu_list:
            continue
        delta = new_score - current_score
        if delta > 0:
            current_solution = neighbor
            current_score = new_score
            if new_score > best_score:
                best_score = new_score
                best_solution = neighbor
        else:
            if random.random() < math.exp(delta / T):
                current_solution = neighbor
                current_score = new_score
        
        tabu_list.append(neighbor)
        if len(tabu_list) > tenure:
            tabu_list.pop(0)
        T = T * alpha

    return best_solution, best_score
