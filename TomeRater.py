class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}
        self.worth = 0

    def get_email(self):
        return self.email

    def change_email(self, address):
        old_email = self.email
        self.email = address
        print("{name}'s email address ({old_email}) was changed for '{new_email}'".format(name = self.name, old_email = old_email, new_email = self.email))
        

    def __repr__(self):
        return "User {name}, email: {email}, books read: {books_amount}".format(name = self.name, email = self.email, books_amount = len(self.books))

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating
        self.worth += book.get_price()

    def get_average_rating(self):
        rating_sum = 0
        rating_quant = 0
        for v in self.books.values():
            if v != None:
                rating_sum += v
                rating_quant += 1
        return rating_sum / len(self.books)

class Book():
    def __init__(self, title, isbn, price):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        self.price = price

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        old_isbn = self.isbn
        self.isbn = isbn
        print("ISBN {old} was changed for {new}".format(old = old_isbn, new = self.isbn))

    def add_rating(self, rating):
        if rating != None:
            if rating >= 0 and rating <= 4:
                self.ratings.append(rating)
            else:
                print("Invalid Rating")

    def get_average_rating(self):
        sum = 0
        for rating in self.ratings:
            sum += rating
        return sum / len(self.ratings)

    def get_price(self):
        return self.price

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return """Title: {title};
        ISBN: {isbn};
        Ratings: {ratings}""".format(title = self.title, isbn = self.isbn, ratings = self.ratings)
    
class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)

class NonFiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        #super(title, isbn, price)
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title = self.title, level = self.level, subject = self.subject)

class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn, price):
        return Book(title, isbn, price)

    def create_novel(self, title, author, isbn, price):
        return Fiction(title, author, isbn, price)

    def create_non_fiction(self, title, subject, level, isbn, price):
        return NonFiction(title, subject, level, isbn, price)

    def add_book_to_user(self, book, email, rating = None):        
        if email in self.users.keys():
            self.users[email].read_book(book, rating)
            book.add_rating(rating)
            if book in self.books.keys():
                self.books[book] += 1
            else:
                self.books[book] = 1
            
        else:
            print("No user with email {email}".format(email = email))        
    
    def add_user(self, name, email, books = None):
        user = User(name, email)
        self.users[email] = user
        if books != None:
            for book in books:
                self.add_book_to_user(book, email)

    def print_catalog(self):
        print("Book Catalog:")
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def get_most_read_book(self):
        most_reads = 0
        book = None
        for k, v in self.books.items():
            if v > most_reads:
                most_reads = v
                book = k
        return book

    def highest_rated_book(self):
        high_rate = 0
        high_book = None
        for book in self.books.keys():
            if book.get_average_rating() > high_rate:
                high_rate = book.get_average_rating()
                high_book = book
        return high_book

    def most_positive_user(self):
        rating = 0
        positive_user = None
        for user in self.users.values():
            if user.get_average_rating() > rating:
                rating = user.get_average_rating()
                positive_user = user
        return positive_user

    def get_n_most_expensive_books(self, n):
        price_list = sorted(self.books, key = lambda book: book.price, reverse = True)
        return price_list[:n] 

    def get_worth_of_user(self, user_email):
        if user_email in self.users.keys():
            for email, user in self.users.items():
                if email == user_email:
                    return user.worth
        else:
            return "User email not found"