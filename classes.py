from queue import PriorityQueue
import initial

# Singleton class to store the problem data
class Singleton:
    def __init__(self, total_books, total_libs, total_days, scores, libs, index):
        self.total_books = total_books  # total number of books
        self.total_libs = total_libs    # total number of libraries
        self.total_days = total_days    # total number of days
        self.scores = scores            # book scores
        self.libs = libs                # libraries
        self.index = index          

    def __str__(self):
        return f"{self.total_books} {self.total_libs} {self.total_days} {self.libs} {self.scores} {self.index}"

# Library class that represents a library
class Library:
    def __init__(self, id, n_books, signup_time, books_per_day, books):
        self.id = id
        self.n_books = n_books                  # number of books
        self.signup_time = signup_time          # signup time
        self.books_per_day = books_per_day      # books per day
        self.books = books                      # books in the library
    
    def __str__(self):
        return f"{self.id} {self.n_books} {self.signup_time} {self.books_per_day} {self.books}"
    
    # greedy way to calculate the possible score of a library given the days left
    def calculate_possible_score(self, days_left):
        # if the library takes more days to signup than the days left, return 0
        library_available_days = days_left - self.signup_time
        if (library_available_days <= 0):
            return 0

        # calculate the number of books that can be scanned
        books_to_scan = library_available_days * self.books_per_day

        # create the necessary variables
        library_books_score = 0
        pq = PriorityQueue()
        counter = 0

        # iterate through the books in the library
        while not self.books.empty():
            # if the number of books to scan is reached, break the loop
            if (counter == books_to_scan):
                break
            
            book = self.books.get()
            pq.put(book)
            # add the book score to the library score
            library_books_score += book.score
            # increment the counter
            counter += 1
        
        # put the books back in the library queue
        while not pq.empty():
            self.books.put(pq.get())

        # return the library score divided by the signup time 
        return library_books_score / self.signup_time

    # less than operator to compare libraries
    def __lt__(self, other):
        # calculate the possible score of each of the libraries
        spd1 = self.calculate_possible_score(initial.days_left)
        spd2 = other.calculate_possible_score(initial.days_left)

        # return the comparison
        return spd1 > spd2

# Book class that represents a book
class Book:
    def __init__(self, id, score):
        self.id = id            # book id
        self.score = score      # book score
    
    def __str__(self):
        return f"{self.id} {self.score}" 
    
    # less than operator to compare books
    def __lt__(self, other):
        # return the comparison
        return self.score > other.score
       