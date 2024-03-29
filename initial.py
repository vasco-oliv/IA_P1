from classes import *


all_libs_dict = []
all_books_dict = []

data_files = [
    'data/a_example.txt',
    'data/b_read_on.txt',
    'data/c_incunabula.txt',
    'data/d_tough_choices.txt',
    'data/e_so_many_books.txt',
    'data/f_libraries_of_the_world.txt'
]

def initialize_days_left(index):
    global days_left
    days_left = read_total_days(data_files[index])

def solve(att):
    global days_left
    solution = []
    days = 0
    scanned_books = set()
    libs_signed_up = set()
    while (not att.libs.empty()):
        lib = att.libs.get()
        days += lib.signup_time
        if (days >= att.total_days):
            break
        days_left = att.total_days - days
        books_left = days_left * lib.books_per_day
        books = []
        while (not lib.books.empty()):
            book = lib.books.get()
            books.append(book.id)
            if (len(books) <= books_left):
                scanned_books.add(book.id)
        
        solution.append((lib.id, books))
        libs_signed_up.add(lib.id)

    score = 0
    books_dict = all_books_dict[att.index]
    for book in scanned_books:
        score += books_dict[book].score

    return solution, score

def read_file(filename ,index):

    f = open(filename, "r")

    line = f.readline()

    values = [int(x) for x in line.split()]

    total_books = values[0]
    total_libs = values[1]
    total_days = values[2]

    line = f.readline()
    scores = [int(x) for x in line.split()]

    books_dict = {}
    for i in range(len(scores)):
        books_dict[i] = Book(i, scores[i])
    all_books_dict.append(books_dict)

    libs = PriorityQueue()
    i = 0
    libs_dict = {}
    initialize_days_left(index)
    while True:
        line = f.readline()    
        values = [int(x) for x in line.split()]

        if len(values) == 0:
            break
        
        line = f.readline()
        books = [int(x) for x in line.split()]

        q = PriorityQueue()
        for b in books:
            q.put(books_dict[b])

        lib = Library(i, values[0], values[1], values[2], q)
        
        libs.put(lib)
        libs_dict[i] = lib
        i += 1

    all_libs_dict.append(libs_dict)
    f.close()

    return total_books, total_libs, total_days, scores, libs

def read_total_days(filename):

    f = open(filename, "r")
    line = f.readline()

    values = [int(x) for x in line.split()]
    return values[2]

def calculate_score(solution, scores, total_days, index):
    score = 0
    scanned_books = set()
    for lib in solution:
        library = all_libs_dict[index][lib[0]]
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


def write_solution(solution, filename):
    with open(filename, "a") as f:
        f.write(f"{len(solution)}\n")
        for lib in solution:
            f.write(f"{lib[0]} {len(lib[1])}\n")
            f.write(" ".join([str(x) for x in lib[1]]) + "\n")
        
def initial_script():
    f = open("initial_solutions.txt", "w")
    f.close()

    for i in range(len(data_files)):
        days_left = read_total_days(data_files[i])
        total_books, total_libs, total_days, scores, libs = read_file(data_files[i], i)
        att = Singleton(total_books, total_libs, total_days, scores, libs, i)

        solution, _ = solve(att)

        write_solution(solution, "initial_solutions.txt")

