import os
from datetime import date

class View:

    def __init__(self):
        self.clear = lambda: os.system('cls')
        self.separator = lambda: print("_________________________")

    def print_menu(self):
        print("1 - get BOOKS by READER->email and AUTHOR->birthday\n"
              "2 - get BOOKS by SUBSCRIPTION->valid_until and ORDER_LIST->time_return\n"
              "3 - get AUTHORS by BOOK->pages and SUBSCRIPTION->valid_since\n"
              "4 - get BOOKS by AUTHOR->birthday and ORDER_LIST->time\n"
              "6 - get READERS by AUTHOR->name\n"
              "7 - get SUBSCRIPTIONS by READER->phone_number and BOOK->title\n"
              "8 - get READERS by BOOK->title\n"
              "9 - get AUTHORS by BOOK->title\n"
              "10 - get BOOKS by id\n"
              "11 - get AUTHORS by name\n"
              "12 - get BOOKS by pages\n"
              "13 - get READERS by address\n"
              "14 - get SUBSCRIPTIONS by reader_id\n"
              "15 - get READERS by id\n"
              "16 - update SUBSCRIPTION\n"
              "17 - update AUTHOR\n"
              "18 - update BOOK\n"
              "19 - update ORDER_LIST\n"
              "20 - update READER\n"
              "21 - delete AUTHOR\n"
              "22 - delete SUBSCRIPTION\n"
              "23 - delete ORDER_LIST\n"
              "24 - delete BOOK\n"
              "25 - delete READER\n"
              "26 - set random AUTHORS\n"
              "27 - set random READERS\n"
              "28 - set random BOOKS\n"
              "29 - set random SUBSCRIPTIONS\n"
              "30 - set random ORDER_LIST\n"
              "31 - get all READERS\n"
              "32 - get all AUTHORS\n"
              "33 - get all BOOKS\n"
              "34 - get all SUBSCRIPTIONS\n"
              "35 - get all ORDER_LIST\n"
              "36 - add READER\n"
              "37 - add AUTHOR\n"
              "38 - add BOOK\n"
              "39 - add SUBSCRIPTION\n"
              "40 - add ORDER_LIST\n"
              "41 - get top 15 books stat\n"
              "42 - get years stat\n"
              "43 - get top readers\n"
              "44 - exit\n")

    def menu(self):
        self.print_menu()
        choice = input(">>>>>>Enter your choice: ")
        return choice

    def print_readers(self, readers):
        for reader in readers:
            print(f"|id - {reader[0]}| name - {reader[1]}| address - {reader[2]}| phone_number - {reader[3]}| email - {reader[4]}|")

    def print_books(self, books):
        for book in books:
            print(f"|id - {book[0]}| author_id - {book[1]}| year_of_writing - {book[2]}| pages - {book[3]}| title - {book[4]}|")

    def print_orders(self, orders):
        for order in orders:
            print(f"|id - {order[0]}| subscr_id - {order[1]}| book_id - {order[2]}| time - {order[3]}| t_return - {order[4]}|")

    def print_subscriptions(self, subscr):
        for sss in subscr:
            print(f"|id - {sss[0]}| reader_id - {sss[1]}| valid_since - {sss[2]}| valid_until - {sss[3]}| number_of_issues - {sss[4]}|")

    def print_authors(self, authors):
        for author in authors:
            print("id", author[0])
            print("name", author[1])
            print("birthday", author[2])
            print(f"|id - {author[0]}| name - {author[1]}| birthday - {author[2]}|")

    def add_reader(self):
        reader = {}
        reader["name"] = self.get_string('name')
        reader["address"] = self.get_string('address')
        reader["phone_number"] = self.get_string('phone_number')
        reader["email"] = self.get_string('email')
        return reader

    def add_book(self):
        book = {}
        book["author_id"] = self.get_number('author_id')
        book["year_of_writing"] = self.get_number('year_of_writing')
        book["pages"] = self.get_string('pages')
        book["title"] = self.get_string('title')
        return book

    def add_order(self):
        order = {}
        order["subscr_id"] = self.get_number('subscr_id')
        order["book_id"] = self.get_number('book_id')
        order["time"] = self.get_date('time')
        order["t_return"] = self.get_date('t_return')
        return order

    def add_subscription(self):
        subscr = {}
        subscr["reader_id"] = self.get_number('reader_id')
        subscr["valid_since"] = self.get_date('valid_since')
        subscr["valid_until"] = self.get_date('valid_until')
        subscr["number_of_issues"] = self.get_number('number_of_issues')
        return subscr

    def add_author(self):
        author = {}
        author["name"] = self.get_string('name')
        author["birthday"] = self.get_number('birthday')
        return author

    def update_reader(self):
        reader = {}
        reader["id"] = self.get_number('id')
        reader["name"] = self.get_string('name')
        reader["address"] = self.get_string('address')
        reader["phone_number"] = self.get_string('phone_number')
        reader["email"] = self.get_string('email')
        return reader

    def update_book(self):
        book = {}
        book["id"] = self.get_number('id')
        book["year_of_writing"] = self.get_number('year_of_writing')
        book["pages"] = self.get_string('pages')
        book["title"] = self.get_string('title')
        return book

    def update_orders(self):
        order = {}
        order["id"] = self.get_number('id')
        order["time"] = self.get_date('time')
        order["t_return"] = self.get_date('t_return')
        return order

    def update_subscriptions(self):
        subscr = {}
        subscr["id"] = self.get_number('id')
        subscr["valid_since"] = self.get_date('valid_since')
        subscr["valid_until"] = self.get_date('valid_until')
        subscr["number_of_issues"] = self.get_number('number_of_issues')
        return subscr

    def update_author(self):
        author = {}
        author["id"] = self.get_number('id')
        author["name"] = self.get_string('name')
        author["birthday"] = self.get_number('birthday')
        return author

    def get_number(self, str):
        while True:
            try:
                num = int(input('Enter '+ str +': '))
                if num < 0:
                    print("enter positive value ")
                    continue
            except ValueError:

                print("you should enter integer value ")
                continue
            break
        return num

    def get_date(self, str):
        while True:
            try:
                print('Enter ' + str)
                year1 = int(input("Enter year: "))
                month1 = int(input("Enter month: "))
                day1 = int(input("Enter day: "))
                if year1 < 0 or month1 < 0 or day1 < 0:
                    print("enter positive values ")
                    continue
            except ValueError:
                print("you should enter integer value ")
                continue
            break
        return date(year1, month1, day1)

    def get_string(self, str):
        return input('Enter '+ str +': ')
