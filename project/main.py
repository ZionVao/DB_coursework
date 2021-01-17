from database import Database
from view import View

database = Database()
database.connect()
database.print_pg_version()

view = View()
choice = '0'

while choice != '44':
    choice = view.menu()
    view.separator()
    if choice == '1':
        view.print_books(database.get_books_by_reader_email_and_author_birthday(view.get_string('email'),
                                                                                view.get_number('year 1'),
                                                                                view.get_number('year 2')))
    elif choice == '2':
        view.print_books(database.get_books_by_subsc_valid_until_and_order_time_return(view.get_date('valid until date 1'),
                                                                                       view.get_date('valid until date 2'),
                                                                                       view.get_date('time return date 1'),
                                                                                       view.get_date('time return date 2')))
    elif choice == '3':
        view.print_authors(database.get_authors_by_book_pages_and_subscr_valid_since(view.get_number('pages 1'),
                                                                                     view.get_number('pages 2'),
                                                                                     view.get_date('valid since date1'),
                                                                                     view.get_date('valid since date2')))
    elif choice == '4':
        view.print_books(database.get_books_by_author_birthday_and_order_time(view.get_number('year 1'),
                                                                              view.get_number('year 2'),
                                                                              view.get_date('date1'),
                                                                              view.get_date('date2')))
    elif choice == '6':
        view.print_readers(database.get_reders_by_author_name(view.get_string('name')))
    elif choice == '7':
        view.print_subscriptions(database.get_subscriptions_by_reader_phone_and_book_title(view.get_string('phone'),
                                                                                           view.get_string('title')))
    elif choice == '8':
        view.print_readers(database.get_readers_by_book_title(view.get_string('title')))
    elif choice == '9':
        view.print_authors(database.get_authors_by_book_title(view.get_string('title')))
    elif choice == '10':
        view.print_books(database.get_books_by_id(view.get_number('id 1'),
                                                  view.get_number('id 2')))
    elif choice == '11':
        view.print_authors(database.get_authors_by_name(view.get_string('name')))
    elif choice == '12':
        view.print_books(database.get_books_by_pages(view.get_number('pages 1'),
                                                     view.get_number('pages 2')))
    elif choice == '13':
        view.print_readers(database.get_readers_by_address(view.get_string('address')))
    elif choice == '14':
        view.print_subscriptions(database.get_subscriptions_by_reader_id(view.get_number('reader_id 1'),
                                                                         view.get_number('reader_id 2')))
    elif choice == '15':
        view.print_readers(database.get_readers_by_id(view.get_number('id 1'),
                                                      view.get_number('id 2')))
    elif choice == '16':
        subscr = view.update_subscriptions()
        print(database.update_subscription_by_id(subscr["id"],
                                                 subscr["valid_since"],
                                                 subscr["valid_until"],
                                                 subscr["number_of_issues"]))
    elif choice == '17':
        author = view.update_author()
        print(database.update_author_by_id(author["id"],
                                           author["name"],
                                           author["birthday"]))
    elif choice == '18':
        book = view.update_book()
        print(database.update_book_by_id(book["id"],
                                         book["year_of_writing"],
                                         book["pages"],
                                         book["title"]))
    elif choice == '19':
        order = view.update_orders()
        print(database.update_order_by_id(order["id"],
                                          order["time"],
                                          order["t_return"]))
    elif choice == '20':
        reader = view.update_reader()
        print(database.update_reader_by_id(reader["id"],
                                           reader["name"],
                                           reader["address"],
                                           reader["phone_number"],
                                           reader["email"]))
    elif choice == '21':
        print(database.delete_author_by_id(view.get_string('id')))
    elif choice == '22':
        print(database.delete_subscription_by_id(view.get_string('id')))
    elif choice == '23':
        print(database.delete_order_by_id(view.get_string('id')))
    elif choice == '24':
        print(database.delete_book_by_id(view.get_string('id')))
    elif choice == '25':
        print(database.delete_reader_by_id(view.get_string('id')))
    elif choice == '26':
        print(database.generate_authors(view.get_number('count')))
    elif choice == '27':
        print(database.generate_readers(view.get_number('count')))
    elif choice == '28':
        print(database.generate_books(view.get_number('count')))
    elif choice == '29':
        print(database.generate_subscriptions(view.get_number('count')))
    elif choice == '30':
        print(database.generate_orders(view.get_number('count')))
    elif choice == '31':
        view.print_readers(database.get_all_readers())
    elif choice == '32':
        view.print_authors(database.get_all_authors())
    elif choice == '33':
        view.print_books(database.get_all_books())
    elif choice == '34':
        view.print_subscriptions(database.get_all_subscriptions())
    elif choice == '35':
        view.print_orders(database.get_all_orders())
    elif choice == '36':
        reader = view.add_reader()
        print(database.add_reader(reader["name"],
                                  reader["address"],
                                  reader["phone_number"],
                                  reader["email"]))
    elif choice == '37':
        author = view.add_author()
        print(database.add_author(author["name"],
                                  author["birthday"]))
    elif choice == '38':
        book = view.add_book()
        print(database.add_book(book["author_id"],
                                book["year_of_writing"],
                                book["pages"],
                                book["title"]))
    elif choice == '39':
        subscr = view.add_subscription()
        print(database.add_subscription(subscr["reader_id"],
                                        subscr["valid_since"],
                                        subscr["valid_until"],
                                        subscr["number_of_issues"]))
    elif choice == '40':
        order = view.add_order()
        print(database.add_order(order["subscr_id"],
                                 order["book_id"],
                                 order["time"],
                                 order["t_return"]))
    elif choice == '41':
        database.getTop15Books()
    elif choice == '42':
        database.get_years_stat()
    elif choice == '43':
        database.get_top_readers()
    elif choice == '44':
        break
    else:
        print("incorrect input")
    view.separator()
database.close()