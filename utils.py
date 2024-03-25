from queue import PriorityQueue

data = [
    'data/a_example.txt',
    'data/b_read_on.txt',
    'data/c_incunabula.txt',
    'data/d_tough_choices.txt',
    'data/e_so_many_books.txt',
    'data/f_libraries_of_the_world.txt'
]

class Library:
    def __init__(self, id, n_books, signup_time, books_per_day, books):
        self.id = id
        self.n_books = n_books                  # number of books
        self.signup_time = signup_time          # signup time
        self.books_per_day = books_per_day      # books per day
        self.books = books
    
    def __str__(self):
        return f"{self.id} {self.n_books} {self.signup_time} {self.books_per_day} {self.books}"
    
    def calculate_possible_score(self, days_left):
        library_available_days = days_left - self.signup_time
        if (library_available_days <= 0):
            return 0
    
        books_to_scan = library_available_days * self.books_per_day

        library_books_score = 0

        pq = PriorityQueue()

        counter = 0

        while not self.books.empty():
            if (counter == books_to_scan):
                break

            book = self.books.get()
            
            if (book.status == 0):
                pq.put(book)
                library_books_score += book.score
                counter += 1
            else:
                break

        while not pq.empty():
            self.books.put(pq.get())

        return (library_books_score / self.signup_time, counter)

        

    def __lt__(self, other):
        global days_left
        spd1 = self.calculate_possible_score(days_left)
        spd2 = other.calculate_possible_score(days_left)

        if (spd1[0] == spd2[0]):
            return spd1[1] > spd2[1]
        return spd1[0] > spd2[0]

class Book:
    def __init__(self, id, score):
        self.id = id
        self.score = score
        self.status = 0
    
    def __str__(self):
        return f"{self.id} {self.score}" 
    
    def __lt__(self, other):
        if (self.status == other.status):
            return self.score > other.score
        return self.status < other.status

def display_data_files():
    display_data = ["All"]
    display_data.extend([file.split('/')[-1] for file in data])

    return display_data

def get_data_files():
    return data

def get_results():
    results = []

    with open("initial_solutions.txt", 'r') as f:
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

def calculate_score(solution, scores, total_days):
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

libs_dict = {}
books_dict = {}

def read_file(filename):

    f = open(filename, "r")

    line = f.readline()

    values = [int(x) for x in line.split()]

    total_books = values[0]
    total_libs = values[1]
    total_days = values[2]

    line = f.readline()
    scores = [int(x) for x in line.split()]

    for i in range(len(scores)):
        books_dict[i] = Book(i, scores[i])

    libs = PriorityQueue()
    i = 0
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

    f.close()

    return total_books, total_libs, total_days, scores, libs

def read_total_days(filename):

    f = open(filename, "r")
    line = f.readline()

    values = [int(x) for x in line.split()]
    return values[2]