import math
import random
from utils import calculate_score

# Basic Hill Climbing
def hill_climbing_basic(solution, scores, total_days, libs_dict):
    # calculate the score of the initial solution
    best_score = calculate_score(solution, scores, total_days, libs_dict)
    # create the necessary variables
    l = len(solution)
    best_solution = solution
    there_is_best = True
    # iterate until there is no better solution
    while there_is_best:
        there_is_best = False
        # iterate through the solution's neighbors
        for i in range(1, l - 1):
            for k in range(i + 1, l):
                # swap two elements in the solution
                n = best_solution[:i] + [best_solution[k]] + best_solution[i + 1:k] + [best_solution[i]] + best_solution[k + 1:]
                # calculate the score of the new solution
                s = calculate_score(n, scores, total_days, libs_dict)
                # if the new solution is better, update the best solution and break the loop
                if s > best_score:
                    best_score = s
                    best_solution = n
                    there_is_best = True
                    break
            # if a better solution is found, break the loop
            if there_is_best:
                break

    return best_solution, best_score

# Hill Climbing with Steepest Ascent    
def hill_climbing_steepest(solution, scores, total_days, libs_dict):
    # calculate the score of the initial solution
    best_score = calculate_score(solution, scores, total_days, libs_dict)
    # create the necessary variables
    l = len(solution)
    best_solution = solution
    there_is_best = True
    # iterate until there is no better solution
    while there_is_best:
        there_is_best = False
        # iterate through the solution's neighbors
        for i in range(1, l - 1):
            for k in range(i + 1, l):
                # swap two elements in the solution
                n = best_solution[:i] + [best_solution[k]] + best_solution[i + 1:k] + [best_solution[i]] + best_solution[k + 1:]
                # calculate the score of the new solution
                s = calculate_score(n, scores, total_days, libs_dict)
                # if the new solution is better, update the best solution
                if s > best_score:
                    best_score = s
                    best_solution = n
                    there_is_best = True

    return best_solution, best_score

# Simulated Annealing
def simulated_annealing(solution, scores, total_days, libs_dict, max_iter, T, alpha):
    # calculate the score of the initial solution
    score = calculate_score(solution, scores, total_days, libs_dict)
    # create the necessary variables
    best_score = score
    best_solution = solution
    current_solution = solution
    current_score = score
    # iterate the number of max iterations
    for _ in range(max_iter):
        # select two random indexes
        i = random.randint(0, len(current_solution) - 2)
        k = random.randint(i + 1, len(current_solution) - 1)
        # swap two elements in the solution
        neighbor = current_solution[:i] + [current_solution[k]] + current_solution[i + 1:k] + [current_solution[i]] + current_solution[k + 1:]
        # calculate the score of the new solution
        new_score = calculate_score(neighbor, scores, total_days, libs_dict)
        # calculate the delta
        delta = new_score - current_score
        # if delta is positive, update the current solution and score
        if delta > 0:
            current_solution = neighbor
            current_score = new_score
            # if the new solution is better than the best solution, update the best solution
            if new_score > best_score:
                best_score = new_score
                best_solution = neighbor
        else:
            # if the new solution is not better, update the current solution with a probability based on the temperature
            if random.random() < math.exp(delta / T):
                current_solution = neighbor
                current_score = new_score
        # anneal the temperature
        T = T * alpha

    return best_solution, best_score

# Tabu Search 
def tabu_search(solution, scores, total_days, libs_dict, max_iter, tenure):
    # calculate the score of the initial solution
    score = calculate_score(solution, scores, total_days, libs_dict)
    # create the necessary variables
    best_score = score
    best_solution = solution
    current_solution = solution
    tabu_list = []
    # iterate the number of max iterations
    for _ in range(max_iter):
        # select two random indexes
        i = random.randint(0, len(current_solution) - 2)
        k = random.randint(i + 1, len(current_solution) - 1)
        # swap two elements in the solution
        neighbor = current_solution[:i] + [current_solution[k]] + current_solution[i + 1:k] + [current_solution[i]] + current_solution[k + 1:]
        # calculate the score of the new solution
        new_score = calculate_score(neighbor, scores, total_days, libs_dict)
        # if the neighbor is in the tabu list, continue
        if neighbor in tabu_list:
            continue
        # if the new solution is better than the best solution, update the best solution
        if new_score > best_score:
            best_score = new_score
            best_solution = neighbor
        # update the current solution to the neighbor
        current_solution = neighbor
        # add the neighbor to the tabu list
        tabu_list.append(neighbor)
        # if the tabu list is full, remove the first element
        if len(tabu_list) > tenure:
            tabu_list.pop(0)

    return best_solution, best_score


# Simulated Annealing with Tabu Search
def simulated_annealing_tabu_search(solution, scores, total_days, libs_dict, max_iter, T, alpha, tenure):
    # calculate the score of the initial solution
    score = calculate_score(solution, scores, total_days, libs_dict)
    # create the necessary variables
    best_score = score
    best_solution = solution
    current_solution = solution
    current_score = score
    tabu_list = []
    # iterate the number of max iterations
    for _ in range(max_iter):
        # select two random indexes
        i = random.randint(0, len(current_solution) - 2)
        k = random.randint(i + 1, len(current_solution) - 1)
        # swap two elements in the solution
        neighbor = current_solution[:i] + [current_solution[k]] + current_solution[i + 1:k] + [current_solution[i]] + current_solution[k + 1:]
        # calculate the score of the new solution
        new_score = calculate_score(neighbor, scores, total_days, libs_dict)
        # if the neighbor is in the tabu list, continue
        if neighbor in tabu_list:
            continue
        # calculate the delta
        delta = new_score - current_score
        # if the delta is positive, update the current solution and score
        if delta > 0:
            current_solution = neighbor
            current_score = new_score
            # if the new solution is better than the best solution, update the best solution
            if new_score > best_score:
                best_score = new_score
                best_solution = neighbor
        else:
            # if the new solution is not better, update the current solution with a probability based on the temperature
            if random.random() < math.exp(delta / T):
                current_solution = neighbor
                current_score = new_score
        # add the neighbor to the tabu list
        tabu_list.append(neighbor)
        # if the tabu list is full, remove the first element
        if len(tabu_list) > tenure:
            tabu_list.pop(0)
        # anneal the temperature
        T = T * alpha

    return best_solution, best_score
