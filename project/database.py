import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date

class Database:

    def __init__(self):
        self.connection = None
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(user="postgres",
                                               password="qwerty",
                                               host="127.0.0.1",
                                               port="5432",
                                               database="book_db")
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgresSQL connection is closed")

    def print_pg_version(self):
        self.cursor.execute("select version();")
        record = self.cursor.fetchone()
        print("You are connected to - ", record, "\n")

    def getTop15Books(self):
        try:
            self.cursor.execute("with tab1 as( "
                                "select count(order_list.book_id), order_list.book_id "
                                "from order_list "
                                "group by order_list.book_id) "
                                "select books.title, tab1.count "
                                "from tab1, books "
                                "where books.id = tab1.book_id "
                                "order by tab1.count DESC LIMIT 15")
            self.connection.commit()
            data = self.cursor.fetchall()
            df = pd.DataFrame([[xy for xy in x] for x in data])

            x = df[0]
            y = df[1]

            group_data = y
            group_names = x
            plt.rcParams.update({'figure.autolayout': True})
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(group_names, group_data)
            labels = ax.get_xticklabels()
            plt.setp(labels, rotation=45, horizontalalignment='right')
            ax.set(xlabel='Total Count', ylabel='Title',
                   title='Books Stat')
            plt.savefig("mygraph.png")
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_years_stat(self):
        try:
            self.cursor.execute("with tab1 as( "
                                "select extract(year from time)::int ext "
                                "from order_list) "
                                "select count(ext), ext "
                                "from tab1 group by ext order by ext")
            self.connection.commit()
            data = self.cursor.fetchall()
            df = pd.DataFrame([[xy for xy in x] for x in data])

            x = df[0]
            y = df[1]

            group_data = x
            group_names = y
            plt.rcParams.update({'figure.autolayout': True})
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(group_names, group_data)
            labels = ax.get_xticklabels()
            plt.setp(labels, rotation=45, horizontalalignment='right')
            ax.set(xlabel='Total Count', ylabel='Years',
                   title='Years Stat')
            plt.savefig("mygraph.png")
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_top_readers(self):
        try:
            self.cursor.execute("with tab1 as( "
                                 "select count(reader_id), reader_id "
                                 "from subscriptions "
                                 "group by reader_id "
                                 "order by count DESC LIMIT 15) "
                                 "select tab1.count, readers.name "
                                 "from readers, tab1 "
                                 "where readers.id = tab1.reader_id")
            self.connection.commit()
            data = self.cursor.fetchall()
            df = pd.DataFrame([[xy for xy in x] for x in data])

            x = df[0]
            y = df[1]

            group_data = x
            group_names = y
            plt.rcParams.update({'figure.autolayout': True})
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(group_names, group_data)
            labels = ax.get_xticklabels()
            plt.setp(labels, rotation=45, horizontalalignment='right')
            ax.set(xlabel='Total Subscriptions Count', ylabel='Names',
                   title='Readers Stat')
            plt.savefig("mygraph.png")
        except Exception as err:
            print(err)
            exit(1)

    def get_authors_by_name(self, the_name: str):
        """11 - get AUTHORS by name"""
        try:
            self.cursor.execute("select * from authors where name like '%s'", ('%' + the_name + '%',))
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_books_by_id(self, id_f: int, id_t: int):
        """10 - get BOOKS by id"""
        try:
            self.cursor.execute("select * from books where id between '%s' and '%s'" % (id_f, id_t))
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_books_by_pages(self, pages_f: int, pages_t: int):
        """12 - get BOOKS by pages"""
        try:
            self.cursor.execute("select * from books where pages between '%s' and '%s'" % (pages_f, pages_t))
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_readers_by_address(self, the_address: str):
        """13 - get READERS by address"""
        try:
            self.cursor.execute("select * from readers where address like '%s'", ('%' + the_address + '%',))
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_readers_by_id(self, id_f: int, id_t: int):
        """15 - get READERS by id"""
        try:
            self.cursor.execute("select * from readers where id between '%s' and '%s'" % (id_f, id_t))
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_subscriptions_by_reader_id(self, rid_f: int, rid_t: int):
        """14 - get SUBSCRIPTIONS by reader_id"""
        try:
            self.cursor.execute("select * from subscriptions where reader_id between '%s' and '%s'" % (rid_f, rid_t))
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_books_by_reader_email_and_author_birthday(self, the_email: str, data1: date, data2: date):
        """1 - get BOOKS by READER->email and AUTHOR->birthday"""
        try:
            self.cursor.execute("with tab1 as( "
                                "select id from readers " 
                                f"where email like '%{the_email}%'), "
                                "tab2 as( "
                                "select subscriptions.id from subscriptions "
                                "inner join tab1 "
                                "on subscriptions.reader_id = tab1.id), "
                                "tab3 as( "
                                "select distinct book_id from order_list "
                                "inner join tab2 on order_list.subscr_id = tab2.id), "
                                "tab4 as( "
                                "select id from authors "
                                f"where birthday between {data1} and {data2}) "
                                "select distinct books.* from books, tab3, tab4 "
                                "where books.author_id = tab4.id  "
                                "and books.id = tab3.book_id "
                                "order by books.id")
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_books_by_subsc_valid_until_and_order_time_return(self, data1: date, data2: date, datao1: date, datao2: date):
        """2 - get BOOKS by SUBSCRIPTION->valid_until and ORDER_LIST->time_return"""
        try:
            self.cursor.execute("with tab1 as( "
                                "select id from subscriptions " 
                                f"where valid_until between '{data1}'::date and '{data2}'::date), "
                                "tab2 as( "
                                "select distinct order_list.book_id from order_list "
                                "inner join tab1 on order_list.subscr_id = tab1.id "
                                f"where order_list.t_return between '{datao1}'::date and '{datao2}'::date) "
                                "select distinct books.* from books, tab2 where books.id = tab2.book_id "
                                "order by books.id ")
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_authors_by_book_pages_and_subscr_valid_since(self, n1: int, n2: int, data1: date, data2: date):
        """3 - get AUTHORS by BOOK->number_of_pages and SUBSCRIPTION->valid_since"""
        try:
            self.cursor.execute("with tab1 as( "
                                "select subscriptions.id from subscriptions "
                                f"where valid_since between '{data1}'::date and '{data2}'::date), "
                                "tab2 as( "
                                "select distinct order_list.book_id from order_list "
                                "inner join tab1 on order_list.subscr_id = tab1.id), "
                                "tab3 as( "
                                "select distinct books.author_id from books "
                                "inner join tab2 on books.id = tab2.book_id "
                                f"where books.pages between {n1} and {n2}) "
                                "select distinct authors.* from authors, tab3 "
                                "where authors.id in (select tab3.author_id from tab3) "
                                "order by authors.id ")
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_books_by_author_birthday_and_order_time(self, data1: int, data2: int, datat1: date, datat2: date):
        """4 - get BOOKS by AUTHOR->birthday and ORDER_LIST->time"""
        try:
            self.cursor.execute("with tab1 as( "
                                "select distinct order_list.book_id from order_list "
                                f"where time between '{datat1}'::date and '{datat2}'::date), "
                                "tab2 as( "
                                "select authors.id from authors "
                                f"where birthday between {data1} and {data2}) "
                                "select distinct books.* from books, tab1, tab2 "
                                "where books.id = tab1.book_id  "
                                "and books.author_id = tab2.id "
                                "order by books.id")
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_reders_by_author_name(self, the_name: str):
        """6 - get READERS by AUTHOR->name"""
        try:
            self.cursor.execute("with tab1 as( "
                                "select authors.id from authors "
                                f"where authors.name like '%{the_name}%'), "
                                "tab2 as( "
                                "select books.id from books "
                                "where author_id in (select tab1.id from tab1)), "
                                "tab3 as( "
                                "select order_list.subscr_id from order_list "
                                "where order_list.book_id in (select tab2.id from tab2)), "
                                "tab4 as( "
                                "select subscriptions.reader_id from subscriptions "
                                "where subscriptions.id in (select tab3.subscr_id from tab3)) "
                                "select distinct readers.* from readers, tab4 "
                                "where readers.id = tab4.reader_id "
                                "order by readers.id")
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_subscriptions_by_reader_phone_and_book_title(self, phone: str, title: str):
        """7 - get SUBSCRIPTIONS by READER->phone_number and BOOK->title"""
        try:
            self.cursor.execute("with tab1 as( "
                                "select id from books "
                                f"where title like '%{title}%'), "
                                "tab2 as( "
                                "select distinct order_list.subscr_id from order_list "
                                "where book_id in (select tab1.id from tab1)), "
                                "tab3 as( "
                                "select  readers.id from readers "
                                f"where phone_number like '%{phone}%') "
                                "select distinct subscriptions.* from subscriptions, tab3, tab2 "
                                "where subscriptions.reader_id = tab3.id "
                                "and subscriptions.id = tab2.subscr_id "
                                "order by subscriptions.id")
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_readers_by_book_title(self, title: str):
        """8 - get READERS by BOOK->title"""
        try:
            self.cursor.execute("with tab1 as( "
                                "select id from books "
                                f"where title like '%{title}%'), "
                                "tab2 as( "
                                "select distinct order_list.subscr_id from order_list "
                                "where book_id in (select tab1.id from tab1)), "
                                "tab3 as( "
                                "select distinct subscriptions.reader_id from subscriptions "
                                "where subscriptions.id in (select tab2.subscr_id from tab2)) "
                                "select readers.* from readers, tab3 "
                                "where readers.id = tab3.reader_id "
                                "order by readers.id")
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def get_authors_by_book_title(self, title: str):
        """9 - get AUTHORS by BOOK->title"""
        try:
            self.cursor.execute("with tab1 as( "
                                "select author_id from books "
                                f"where title like '%{title}%') "
                                "select distinct authors.* from authors, tab1 "
                                "where authors.id = tab1.author_id ")
            self.connection.commit()
            result = self.cursor.fetchall()
            return result
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error", error)

    def generate_authors(self, num: int):
        """26 - set random AUTHORS"""
        try:
            self.cursor.execute("insert into authors (name, birthday) "
                                "select rand.name, rand.birthday "
                                "from (SELECT trunc(1020* Random() + 1000) as birthday, "
                                "(md5(random()::text)) as name "
                                f"from generate_series(1,{num})) as rand")
            self.connection.commit()
            if self.cursor.rowcount:
                return "generated authors"
            else:
                return "NULL"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in generate", error)

    def generate_readers(self, num: int):
        """27 - set random READERS"""
        try:
            self.cursor.execute("insert into readers (phone_number, email, name, address) "
                                "select rand.phone_number, rand.email, rand.name, rand.address "
                                "from (SELECT trunc(9000000000* Random() + 1000000000)::text as phone_number, "
                                "(md5(random()::text) || '@' || (array['gmail','hotmail','yahoo'])[floor(random()*3+1)] || '.com') as email, "
                                "(md5(random()::text)) as name, "
                                "(md5(random()::text) || ' ' || trunc(random()*100)::text) as address "
                                f"from generate_series(1,{num})) as rand")
            self.connection.commit()
            if self.cursor.rowcount:
                return "generated readers"
            else:
                return "NULL"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in generate", error)

    def generate_books(self, num: int):
        """28 - set random BOOKS"""
        try:
            self.cursor.execute("insert into  books (author_id, year_of_writing, pages, title) "
                                "select rand.author_id, rand.year_of_writing, rand.pages, rand.title "
                                "from (select authors.id as author_id, "
                                "2020 - trunc(Random()*1000)::integer as year_of_writing, "
                                "trunc(Random()*5000)::integer + 20 as pages, "
                                "md5(random()::text) as title "
                                f"from  generate_series(1, 1000), authors ORDER BY random() limit {num}) as rand")
            self.connection.commit()
            if self.cursor.rowcount:
                return "generated books"
            else:
                return "NULL"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in generate", error)

    def generate_subscriptions(self, num: int):
        """29 - set random SUBSCRIPTIONS"""
        try:
            self.cursor.execute("insert into  subscriptions(reader_id, valid_since, valid_until, number_of_issues) "
                                "select rand.reader_id, rand.valid_since, rand.valid_until, rand.number_of_issues "
                                "from (select readers.id as reader_id, "
                                "((current_date - '6 years'::interval) + trunc(random() * 365) * '1 day'::interval + trunc(random() * 3) * '1 year'::interval ) as valid_since, "
                                "((current_date - '3 years'::interval) + trunc(random() * 365) * '1 day'::interval + trunc(random() * 2) * '1 year'::interval ) as valid_until, "
                                "trunc(random()*10)+1::integer as number_of_issues "
                                f"from  generate_series(1, 100), readers ORDER BY random() limit {num}) as rand")
            self.connection.commit()
            if self.cursor.rowcount:
                return "generated subscriptions"
            else:
                return "NULL"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in generate", error)

    def generate_orders(self, num: int):
        """30 - set random ORDER_LIST"""
        try:
            self.cursor.execute("insert into order_list (subscr_id, book_id, time, t_return) "
                                "select rand.subscr_id, rand.book_id, rand.time, rand.t_return "
                                "from (select ((current_date - '6 years'::interval) + trunc(random() * 365) * '1 day'::interval + trunc(random() * 3) * '1 year'::interval ) as time, "
                                "((current_date - '3 years'::interval) + trunc(random() * 365) * '1 day'::interval + trunc(random() * 2) * '1 year'::interval ) as t_return, "
                                "books.id as book_id, "
                                "subscriptions.id as subscr_id "
                                f"from generate_series(1, 1), books, subscriptions ORDER BY random() limit {num}) as rand ")
            self.connection.commit()
            if self.cursor.rowcount:
                return "generated orders"
            else:
                return "NULL"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in generate", error)

    def delete_author_by_id(self, id: int):
        """21 - delete AUTHOR"""
        try:
            self.cursor.execute(
                f"delete from order_list where book_id in (select books.id where author_id={id})")
            self.connection.commit()
            if self.cursor.rowcount:
                return "delete"
            else:
                return "Cant find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in delete 1", error)
        try:
            self.cursor.execute(
                f"delete from books where author_id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "delete"
            else:
                return "Cant find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in delete 2", error)
        try:
            self.cursor.execute(
                f"delete from authors where id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "delete"
            else:
                return "Cant find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in delete 3", error)

    def delete_subscription_by_id(self, id: int):
        """22 - delete SUBSCRIPTION"""
        try:
            self.cursor.execute(
                f"delete from order_list where subscr_id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "delete"
            else:
                return "Cant find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in delete 1", error)
        try:
            self.cursor.execute(
                f"delete from subscriptions where id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "delete"
            else:
                return "Cant find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in delete 2", error)

    def delete_order_by_id(self, id: int):
        """23 - delete ORDER_LIST"""
        try:
            self.cursor.execute(
                f"delete from order_list where id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "delete"
            else:
                return "Cant find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in delete", error)

    def delete_book_by_id(self, id: int):
        """24 - delete BOOK"""
        try:
            self.cursor.execute(
                f"delete from order_list where book_id in (select books.id where id={id})")
            self.connection.commit()
            if self.cursor.rowcount:
                return "delete"
            else:
                return "Cant find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in delete 1", error)
        try:
            self.cursor.execute(
                f"delete from books where id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "delete"
            else:
                return "Cant find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in delete 2", error)

    def delete_reader_by_id(self, id: int):
        """25 - delete READER"""
        try:
            self.cursor.execute(
                f"delete from order_list where subscr_id in (select subscriptions.id from subscriptions where reader_id={id})")
            self.connection.commit()
            if self.cursor.rowcount:
                return "delete"
            else:
                return "Cant find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in delete 1", error)
        try:
            self.cursor.execute(
                f"delete from subscriptions where reader_id ={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "delete"
            else:
                return "Cant find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in delete 2", error)
        try:
            self.cursor.execute(
                f"delete from readers where id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "delete"
            else:
                return "Cant find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in delete 3", error)

    def update_author_by_id(self, id: int, name: str, birthday: int):
        """17 - update AUTHOR"""
        try:
            self.cursor.execute(
                f"update authors set name='{name}',birthday={birthday} where id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "update"
            else:
                return "Can't find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in update", error)

    def update_book_by_id(self, id: int, year_of_writing: int, pages: int, title: str):
        """18 - update BOOK"""
        try:
            self.cursor.execute(
                f"update books set year_of_writing={year_of_writing},pages={pages}, title='{title}' where id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "update"
            else:
                return "Can't find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in update", error)

    def update_order_by_id(self, id: int, time: date, t_return: date):
        """19 - update ORDER_LIST"""
        try:
            self.cursor.execute(
                f"update order_list set time={time},t_return={t_return} where id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "update"
            else:
                return "Can't find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in update", error)

    def update_reader_by_id(self, id: int, name: str, address: str, phone_number: str, email: str):
        """20 - update READER"""
        try:
            self.cursor.execute(
                f"update readers set name='{name}', address='{address}', phone_number='{phone_number}', email='{email}' where id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "update"
            else:
                return "Can't find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in update", error)

    def update_subscription_by_id(self, id: int, valid_since: date, valid_until: date, number_of_issues: int):
        """16 - update SUBSCRIPTION"""
        try:
            self.cursor.execute(
                f"update subscriptions set valid_since={valid_since}, valid_until={valid_until}, number_of_issues={number_of_issues} where id={id}")
            self.connection.commit()
            if self.cursor.rowcount:
                return "update"
            else:
                return "Can't find entity by id"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in update", error)

    def get_all_readers(self):
        """31 - get all READERS"""
        self.cursor.execute("select * from readers")
        self.connection.commit()
        return self.cursor.fetchall()

    def get_all_authors(self):
        """32 - get all AUTHORS"""
        self.cursor.execute("select * from authors")
        self.connection.commit()
        return self.cursor.fetchall()

    def get_all_books(self):
        """33 - get all BOOKS"""
        self.cursor.execute("select * from books")
        self.connection.commit()
        return self.cursor.fetchall()

    def get_all_subscriptions(self):
        """34 - get all SUBSCRIPTIONS"""
        self.cursor.execute("select * from subscriptions")
        self.connection.commit()
        return self.cursor.fetchall()

    def get_all_orders(self):
        """35 - get all ORDER_LIST"""
        self.cursor.execute("select * from order_list")
        self.connection.commit()
        return self.cursor.fetchall()

    def add_reader(self, name: str, address: str, phone: str, email: str):
        """36 - add READER"""
        try:
            self.cursor.execute(
                f"insert into readers (name, address, phone_number, email) values ('{name}', '{address}', '{phone}', '{email}')")
            self.connection.commit()
            return "add"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in add", error)
            return "Cant add place error row or place or type or empty"

    def add_author(self, name: str, birthday: date):
        """37 - add AUTHOR"""
        try:
            self.cursor.execute(
                f"insert into authors (name, birthday) values ('{name}',{birthday})")
            self.connection.commit()
            return "add"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in add", error)
            return "Cant add place error row or place or type or empty"

    def add_book(self, auth_id: int, year: int, pages: int, title: str):
        """38 - add BOOK"""
        try:
            self.cursor.execute(
                f"insert into boooks (author_id, year_of_writing, pages, title) values ({auth_id}, {year}, {pages}, '{title}')")
            self.connection.commit()
            return "add"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in add", error)
            return "Cant add place error row or place or type or empty"

    def add_subscription(self, reader_id: int, since: date, until: date, issues: int):
        """39 - add SUBSCRIPTION"""
        try:
            self.cursor.execute(
                f"insert into subscriptions (reader_id, valid_since, valid_until, number_of_issues) values ({reader_id}, {since}, {until}, {issues})")
            self.connection.commit()
            return "add"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in add", error)
            return "Cant add place error row or place or type or empty"

    def add_order(self, subscr_id: int, book_id: int, time: date, t_return: date):
        """40 - add ORDER_LIST"""
        try:
            self.cursor.execute(
                f"insert into order_list (subscr_id, book_id, time, t_return) values ({subscr_id}, {book_id}, {time}, {t_return})")
            self.connection.commit()
            return "add"
        except(Exception, psycopg2.Error) as error:
            self.cursor.rollback()
            print("error in add", error)
            return "Cant add place error row or place or type or empty"