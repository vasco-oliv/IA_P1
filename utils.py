from initial import calculate_score
import pandas as pd
import os
from queue import Queue
from classes import Book, Library


data = [
    'data/a_example.txt',
    'data/b_read_on.txt',
    'data/c_incunabula.txt',
    'data/d_tough_choices.txt',
    'data/e_so_many_books.txt',
    'data/f_libraries_of_the_world.txt'
]

best_solutions = [
    'solutions/best_solution_a.txt',
    'solutions/best_solution_b.txt',
    'solutions/best_solution_c.txt',
    'solutions/best_solution_d.txt',
    'solutions/best_solution_e.txt',
    'solutions/best_solution_f.txt'
]

algorithms = [
    "Basic Hill Climbing",
    "Steepest Hill Climbing",
    "Simulated Annealing",
    "Simulated Annealing with Tabu Search",
]

def get_algorithm_names():
    return algorithms

def display_data_files():
    display_data = ["All"]
    display_data.extend([file.split('/')[-1] for file in data])

    return display_data

def get_data_files():
    return data

def get_results():
    results = []

    with open("solutions/initial_solutions.txt", 'r') as f:
        for _ in data:
            line = f.readline()
            l = list(line)
            num_libraries = int(line)
            result = []
            for i in range(num_libraries):
                line = f.readline()
                values = [int(x) for x in line.split()]

                line = f.readline()
                books = [int(x) for x in line.split()]

                result.append((values[0], books))

            results.append(result)

    return results

def get_scores_and_days():
    all_book_scores = []
    all_total_days = []
    for file in data:
        with open(file, 'r') as f:
            line = f.readline()
            values = [int(x) for x in line.split()]
            total_days = values[2]

            line = f.readline()
            scores = [int(x) for x in line.split()]

            all_book_scores.append(scores)
            all_total_days.append(total_days)
        

    return all_total_days, all_book_scores

# def get_score_data():
#     results = get_results()
#     all_total_days, all_book_scores = get_scores_and_days()
#     scores=[]
#     for i in range(len(results)):
#         calculated_score = calculate_score(results[i], all_book_scores[i], all_total_days[i], i)
#         scores.append(calculated_score)

#     df = pd.DataFrame(scores, index=display_data_files()[1:], columns=["Initial Score"])
#     df.index.name = "File"
#     return df

def get_score_data():
    scores = []
    with open("solutions/initial_scores.txt", 'r') as f:
        line = f.readline()
        scores = [int(x) for x in line.split()]

    best_scores = []
    for i in range(len(best_solutions)):
        if not os.path.exists(best_solutions[i]):
            best_scores.append(scores[i])
            continue

        with open(best_solutions[i], 'r') as f:
            line = f.readline()
            best_scores.append(int(line))

    df = pd.DataFrame(
        {"Initial Score": scores, "Best Score": best_scores}, 
        index=display_data_files()[1:]
    )

    df.index.name = "File"
    df.loc["Total Score"] = df.sum()

    # add percentage improvement
    df["Improvement (%)"] = (df["Best Score"] - df["Initial Score"]) / df["Initial Score"] * 100

    # transform the Improvement column in a string with the "%" symbol
    df["Improvement (%)"] = df["Improvement (%)"].apply(lambda x: f"{x:.2f}%")

    df = df.style.set_properties(**{
        'text-align': 'center'
    })

    return df

def read_file_for_optimize(filename, index, from_best):
    f = open(filename, "r")

    line = f.readline()

    values = [int(x) for x in line.split()]

    total_days = values[2]

    line = f.readline()
    scores = [int(x) for x in line.split()]

    books_dict = {}
    for i in range(len(scores)):
        books_dict[i] = Book(i, scores[i])

    libs = Queue()
    i = 0
    libs_dict = {}
    while True:
        line = f.readline()    
        values = [int(x) for x in line.split()]

        if len(values) == 0:
            break
        
        line = f.readline()
        books = [int(x) for x in line.split()]

        q = Queue()
        for b in books:
            q.put(books_dict[b])

        lib = Library(i, values[0], values[1], values[2], q)
        
        libs.put(lib)
        libs_dict[i] = lib
        i += 1

    f.close()

    if from_best and os.path.exists(best_solutions[index]):
        f = open(best_solutions[index], "r")
        f.readline()
        line = f.readline()
        num_libraries = int(line)
        result = []
        for i in range(num_libraries):
            line = f.readline()
            values = [int(x) for x in line.split()]

            line = f.readline()
            books = [int(x) for x in line.split()]

            result.append((values[0], books))
    else:
        f = open("solutions/initial_solutions.txt", "r")
        for _ in range(index):
            line = f.readline()
            num_libraries = int(line)
            for i in range(num_libraries):
                f.readline()
                f.readline()

        line = f.readline()
        num_libraries = int(line)
        result = []
        for i in range(num_libraries):
            line = f.readline()
            values = [int(x) for x in line.split()]

            line = f.readline()
            books = [int(x) for x in line.split()]

            result.append((values[0], books))

    return libs_dict, total_days, scores, result

def calculate_score(solution, scores, total_days, libs_dict):
    score = 0
    scanned_books = set()
    for lib in solution:
        library = libs_dict[lib[0]]
        books = lib[1]
        total_days = total_days - library.signup_time
        
        if (total_days <= 0):
            break

        books_left = total_days * library.books_per_day
        for i in range(min(len(books), books_left)):
            if books[i] not in scanned_books:
                score += scores[books[i]]
                scanned_books.add(books[i])

    return score

def get_current_best_score(index):
    if not os.path.exists(best_solutions[index]):
        return -1
    with open(best_solutions[index], 'r') as f:
        line = f.readline()
        best_score = int(line)

    return best_score

def get_current_best(index):
    if not os.path.exists(best_solutions[index]):
        return None, -1

    with open(best_solutions[index], 'r') as f:
        line = f.readline()
        best_score = int(line)

        result = []
        line = f.readline()
        num_libraries = int(line)
        for i in range(num_libraries):
            line = f.readline()
            values = [int(x) for x in line.split()]

            line = f.readline()
            books = [int(x) for x in line.split()]

            result.append((values[0], books))

    return result, best_score

def save_best(index, best_score, best_solution):
    with open(best_solutions[index], 'w') as f:
        f.write(str(best_score) + "\n")
        f.write(str(len(best_solution)) + "\n")
        for lib in best_solution:
            f.write(str(lib[0]) + " " + str(len(lib[1])) + "\n")
            f.write(" ".join([str(x) for x in lib[1]]) + "\n")