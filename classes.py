from queue import PriorityQueue
import initial

class Singleton:
    def __init__(self, total_books, total_libs, total_days, scores, libs, index):
        self.total_books = total_books  # total number of books
        self.total_libs = total_libs  # total number of libraries
        self.total_days = total_days  # total number of days
        self.scores = scores
        self.libs = libs
        self.index = index

    def __str__(self):
        return f"{self.total_books} {self.total_libs} {self.total_days} {self.libs} {self.scores} {self.index}"


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

            pq.put(book)
            library_books_score += book.score
            counter += 1
        

        while not pq.empty():
            self.books.put(pq.get())

        return library_books_score / self.signup_time

        

    def __lt__(self, other):
        spd1 = self.calculate_possible_score(initial.days_left)
        spd2 = other.calculate_possible_score(initial.days_left)

        return spd1 > spd2

class Book:
    def __init__(self, id, score):
        self.id = id
        self.score = score
    
    def __str__(self):
        return f"{self.id} {self.score}" 
    
    def __lt__(self, other):
        return self.score > other.score
       