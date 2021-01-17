import models
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import pandas as pd
from sqlalchemy import func, Integer

class Database:

    def __init__(self):
        self.engine = create_engine('postgres+psycopg2://postgres:qwerty@localhost:5432/book_db', echo=True)
        self.session = sessionmaker(bind=self.engine)()

    def close(self):
        self.session.close()

    def getTop15Books(self):
        try:
            data = self.session.execute("with tab1 as( "
                                        "select count(order_list.book_id), order_list.book_id "
                                        "from order_list "
                                        "group by order_list.book_id) "
                                        "select books.title, tab1.count "
                                        "from tab1, books "
                                        "where books.id = tab1.book_id "
                                        "order by tab1.count DESC LIMIT 15")
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
            ax.set(xlabel='Total Revenue', ylabel='Company',
                   title='Company Revenue')
            plt.savefig("mygraph.png")
        except Exception as err:
            print(err)
            exit(1)


        """ def getTop15Books(self):
        try:
            results = self.session.query(models.Book.id, func.count(models.Book.id).label('count')) \
                .join(models.Order, models.Book.Order) \
                .group_by(models.Book.id) \
                .order_by(func.count('count').desc()) \
                .limit(15).all()
            results = self.session.query(models.Book.id).limit(15)

            listed = list(zip(*results))

            series = pd.Series(np.array(listed[1]), index=listed[0], name='')

            series.plot.pie(figsize=(9, 7), title="Top 15 books:")

            plt.plot(series)
            plt.show()
        except Exception as err:
            print(err)
            exit(1)

        def getSubscriptionOrderStat(self):
        results = self.session.query(
            func.extract('subscr_id', models.Order.subscr_id).cast(Integer).label('subscr_id'),
            func.count('subscr_id')) \
            .group_by('subscr_id') \
            .order_by('subscr_id').all()

        listed = list(zip(*results))

        ts = pd.DataFrame(np.array(listed[1]), listed[0])

        ts.plot(kind='bar', figsize=(9, 7), title="Orders by subscriptions")
        plt.plot(ts)
        plt.show()

        def getBooksAuthor(self):
        results = self.session.query(
            func.extract('author_id', models.Book.author_id).cast(Integer).label('author_id'),
            func.count('author_id')) \
            .group_by('author_id') \
            .order_by('author_id').all()

        listed = list(zip(*results))

        ts = pd.DataFrame(np.array(listed[1]), listed[0])

        ts.plot(kind='bar', figsize=(9, 7), title="Books Statistic by authors")
        plt.plot(ts)
        plt.show()

        def getTotalSubscriptionsInReaders(self):
        results = self.session.query(func.count(models.Subscription.reader_id).label('reader_id'),
                                         func.extract('id', models.Reader.id).cast(Integer).label('id')) \
            .join(models.Subscription.Reader) \
            .group_by('id') \
            .order_by('id').all()

        listed = list(zip(*results))
        series = pd.DataFrame(np.array([int(num) for num in listed[0]]), index=listed[1])
        series.plot(figsize=(9, 7), title="Total subscriptions")
        plt.plot(series)
        plt.show()"""


    def get_author_by_id(self, itemId):
        '''11 - get AUTHOR by id'''
        try:
            return self.session.query(models.Author).get(itemId)
        except Exception as err:
            print("Get by id error! ", err)
            raise err

    def get_book_by_id(self, itemId):
        '''10 - get BOOK by id'''
        try:
            return self.session.query(models.Book).get(itemId)
        except Exception as err:
            print("Get by id error! ", err)
            raise err

    def get_order_by_id(self, itemId):
        '''12 - get ORDER by id'''
        try:
            return self.session.query(models.Order).get(itemId)
        except Exception as err:
            print("Get by id error! ", err)
            raise err

    def get_reader_by_id(self, itemId):
        '''13 - get READER by id'''
        try:
            return self.session.query(models.Reader).get(itemId)
        except Exception as err:
            print("Get by id error! ", err)
            raise err

    def get_subscription_by_id(self, itemId):
        '''14 - get SUBSCRIPTION by id'''
        try:
            return self.session.query(models.Subscription).get(itemId)
        except Exception as err:
            print("Get by id error! ", err)
            raise err

    def get_books_by_reader_email_and_author_birthday(self, the_email, data1, data2):
        """1 - get BOOKS by READER->email and AUTHOR->birthday"""
        try:
            result = self.session.execute("with tab1 as( "
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
                            "and books.id = tab3.book_id ")
            self.session.commit()
            return result
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def get_books_by_subsc_valid_until_and_order_time_return(self, data1, data2, datao1, datao2):
        """2 - get BOOKS by SUBSCRIPTION->valid_until and ORDER_LIST->time_return"""
        try:
            result = self.session.execute("with tab1 as( "
                            "select id from subscriptions " 
	                        f"where valid_until between '{data1}'::date and '{data2}'::date), "
                            "tab2 as( "
                            "select distinct order_list.book_id from order_list "
	                        "inner join tab1 on order_list.subscr_id = tab1.id "
	                        f"where order_list.t_return between '{datao1}'::date and '{datao2}'::date) "
                            "select distinct books.* from books, tab2 where books.id = tab2.book_id ")
            self.session.commit()
            return result
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def get_authors_by_book_pages_and_subscr_valid_since(self, n1, n2, data1, data2):
        """3 - get AUTHORS by BOOK->number_of_pages and SUBSCRIPTION->valid_since"""
        try:
            result = self.session.execute("with tab1 as( "
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
                            "where authors.id in (select tab3.author_id from tab3)")
            self.session.commit()
            return result
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def get_books_by_author_birthday_and_order_time(self, data1, data2, datat1, datat2):
        """4 - get BOOKS by AUTHOR->birthday and ORDER_LIST->time"""
        try:
            result = self.session.execute("with tab1 as( "
                            "select distinct order_list.book_id from order_list "
                            f"where time between '{datat1}'::date and '{datat2}'::date), "
                            "tab2 as( "
                            "select authors.id from authors "
                            f"where birthday between {data1} and {data2}) "
                            "select distinct books.* from books, tab1, tab2 "
                            "where books.id = tab1.book_id  "
                            "and books.author_id = tab2.id")
            self.session.commit()
            return result
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def get_reders_by_author_name(self, the_name):
        """6 - get READERS by AUTHOR->name"""
        try:
            result = self.session.execute("with tab1 as( "
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
                            "where readers.id = tab4.reader_id ")
            self.session.commit()
            return result
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def get_subscriptions_by_reader_phone_and_book_title(self, phone, title):
        '''7 - get SUBSCRIPTIONS by READER->phone_number and BOOK->title'''
        try:
            result = self.session.execute("with tab1 as( "
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
                                "and subscriptions.id = tab2.subscr_id")
            self.session.commit()
            return result
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def get_readers_by_book_title(self, title):
        '''8 - get READERS by BOOK->title'''
        try:
            result = self.session.execute("with tab1 as( "
                                "select id from books "
                                f"where title like '%{title}%'), "
                                "tab2 as( "
                                "select distinct order_list.subscr_id from order_list "
                                "where book_id in (select tab1.id from tab1)), "
                                "tab3 as( "
                                "select distinct subscriptions.reader_id from subscriptions "
                                "where subscriptions.id in (select tab2.subscr_id from tab2)) "
                                "select readers.* from readers, tab3 "
                                "where readers.id = tab3.reader_id ")
            self.session.commit()
            return result
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def get_authors_by_book_title(self, title):
        '''9 - get AUTHORS by BOOK->title'''
        try:
            result = self.session.execute("with tab1 as( "
                                "select author_id from books "
                                f"where title like '%{title}%') "
                                "select distinct authors.* from authors, tab1 "
                                "where authors.id = tab1.author_id ")
            self.session.commit()
            return result
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def generate_authors(self, num):
        '''26 - set random AUTHORS'''
        try:
            self.session.execute("insert into authors (name, birthday) "
                                "select rand.name, rand.birthday "
                                "from (SELECT trunc(1020* Random() + 1000) as birthday, "
                                "(md5(random()::text)) as name "
                                f"from generate_series(1,{num})) as rand")
            self.session.commit()
            if self.session.rowcount:
                return "generated authors"
            else:
                return "NULL"
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def generate_readers(self, num):
        '''27 - set random READERS'''
        try:
            self.session.execute("insert into readers (phone_number, email, name, address) "
                                "select rand.phone_number, rand.email, rand.name, rand.address "
                                "from (SELECT trunc(9000000000* Random() + 1000000000)::text as phone_number, "
                                "(md5(random()::text) || '@' || (array['gmail','hotmail','yahoo'])[floor(random()*3+1)] || '.com') as email, "
                                "(md5(random()::text)) as name, "
                                "(md5(random()::text) || ' ' || trunc(random()*100)::text) as address "
                                f"from generate_series(1,{num})) as rand")
            self.session.commit()
            if self.session.rowcount:
                return "generated readers"
            else:
                return "NULL"
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def generate_books(self, num):
        '''28 - set random BOOKS'''
        try:
            self.session.execute("insert into  books (author_id, year_of_writing, pages, title) "
                                "select rand.author_id, rand.year_of_writing, rand.pages, rand.title "
                                "from (select authors.id as author_id, "
                                "2020 - trunc(Random()*1000)::integer as year_of_writing, "
                                "trunc(Random()*5000)::integer + 20 as pages, "
                                "md5(random()::text) as title "
                                f"from  generate_series(1, 1000), authors ORDER BY random() limit {num}) as rand")
            self.session.commit()
            if self.session.rowcount:
                return "generated books"
            else:
                return "NULL"
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def generate_subscriptions(self, num):
        '''29 - set random SUBSCRIPTIONS'''
        try:
            self.session.execute("insert into  subscriptions(reader_id, valid_since, valid_until, number_of_issues) "
                                "select rand.reader_id, rand.valid_since, rand.valid_until, rand.number_of_issues "
                                "from (select readers.id as reader_id, "
                                "((current_date - '6 years'::interval) + trunc(random() * 365) * '1 day'::interval + trunc(random() * 3) * '1 year'::interval ) as valid_since, "
                                "((current_date - '3 years'::interval) + trunc(random() * 365) * '1 day'::interval + trunc(random() * 2) * '1 year'::interval ) as valid_until, "
                                "trunc(random()*10)+1::integer as number_of_issues "
                                f"from  generate_series(1, 100), readers ORDER BY random() limit {num}) as rand")
            self.session.commit()
            if self.session.rowcount:
                return "generated subscriptions"
            else:
                return "NULL"
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def generate_orders(self, num):
        '''30 - set random ORDER_LIST'''
        try:
            self.session.execute("insert into order_list (subscr_id, book_id, time, t_return) "
                                "select rand.subscr_id, rand.book_id, rand.time, rand.t_return "
                                "from (select ((current_date - '6 years'::interval) + trunc(random() * 365) * '1 day'::interval + trunc(random() * 3) * '1 year'::interval ) as time, "
                                "((current_date - '3 years'::interval) + trunc(random() * 365) * '1 day'::interval + trunc(random() * 2) * '1 year'::interval ) as t_return, "
                                "books.id as book_id, "
                                "subscriptions.id as subscr_id "
                                f"from generate_series(1, 1), books, subscriptions ORDER BY random() limit {num}) as rand")
            self.session.commit()
            if self.session.rowcount:
                return "generated orders"
            else:
                return "NULL"
        except Exception as err:
            print("Get error! ", err)
            self.session.rollback()
            raise err

    def delete_author_by_id(self, id):
        '''21 - delete AUTHOR'''
        try:
            item = self.get_author_by_id(id)
            if type(item) is not models.Author:
                return "can't find id"
            c = self.session.delete(item)
            self.session.commit()
            return "delete"
        except(Exception, SQLAlchemyError) as error:
            self.session.rollback()
            print("error in delete", error)

    def delete_subscription_by_id(self, id):
        '''22 - delete SUBSCRIPTION'''
        try:
            item = self.get_subscription_by_id(id)
            if type(item) is not models.Subscription:
                return "can't find id"
            c = self.session.delete(item)
            self.session.commit()
            return "delete"
        except(Exception, SQLAlchemyError) as error:
            self.session.rollback()
            print("error in delete", error)

    def delete_order_by_id(self, id):
        '''23 - delete ORDER_LIST'''
        try:
            item = self.get_order_by_id(id)
            if type(item) is not models.Order:
                return "can't find id"
            c = self.session.delete(item)
            self.session.commit()
            return "delete"
        except(Exception, SQLAlchemyError) as error:
            self.session.rollback()
            print("error in delete", error)

    def delete_book_by_id(self, id):
        '''24 - delete BOOK'''
        try:
            item = self.get_book_by_id(id)
            if type(item) is not models.Book:
                return "can't find id"
            c = self.session.delete(item)
            self.session.commit()
            return "delete"
        except(Exception, SQLAlchemyError) as error:
            self.session.rollback()
            print("error in delete", error)

    def delete_reader_by_id(self, id):
        '''25 - delete READER'''
        try:
            item = self.get_reader_by_id(id)
            if type(item) is not models.Reader:
                return "can't find id"
            c = self.session.delete(item)
            self.session.commit()
            return "delete"
        except(Exception, SQLAlchemyError) as error:
            self.session.rollback()
            print("error in delete", error)

    def update_author_by_id(self, id, name, birthday):
        '''17 - update AUTHOR'''
        try:
            item = self.session.query(models.Author).filter_by(id=id).update(
                {models.Author.name: name, models.Author.birthday: birthday})
            self.session.commit()
            if item:
                return "success"
            else:
                return "fail"
        except (Exception, SQLAlchemyError) as err:
            self.session.rollback()
            print("error in update", err)

    def update_book_by_id(self, id, year_of_writing, pages, title):
        '''18 - update BOOK'''
        try:
            item = self.session.query(models.Book).filter_by(id=id).update(
                {models.Book.year_of_writing: year_of_writing, models.Book.pages: pages,
                 models.Book.title: title})
            self.session.commit()
            if item:
                return "success"
            else:
                return "fail"
        except (Exception, SQLAlchemyError) as err:
            self.session.rollback()
            print("error in update", err)

    def update_order_by_id(self, id, time, t_return):
        '''19 - update ORDER_LIST'''
        try:
            item = self.session.query(models.Order).filter_by(id=id).update(
                {models.Order.name: time, models.Order.birthday: t_return})
            self.session.commit()
            if item:
                return "success"
            else:
                return "fail"
        except (Exception, SQLAlchemyError) as err:
            self.session.rollback()
            print("error in update", err)

    def update_reader_by_id(self, id, name, address, phone_number, email):
        '''20 - update READER'''
        try:
            item = self.session.query(models.Reader).filter_by(id=id).update(
                {models.Reader.name: name, models.Reader.address: address,
                 models.Reader.phone_number: phone_number, models.Reader.email: email})
            self.session.commit()
            if item:
                return "success"
            else:
                return "fail"
        except (Exception, SQLAlchemyError) as err:
            self.session.rollback()
            print("error in update", err)

    def update_subscription_by_id(self, id, valid_since, valid_until, number_of_issues):
        '''16 - update SUBSCRIPTION'''
        try:
            item = self.session.query(models.Subscription).filter_by(id=id).update(
                {models.Subscription.valid_since: valid_since, models.Subscription.valid_until: valid_until,
                 models.Subscription.number_of_issues: number_of_issues})
            self.session.commit()
            if item:
                return "success"
            else:
                return "fail"
        except (Exception, SQLAlchemyError) as err:
            self.session.rollback()
            print("error in update", err)

    def get_all_readers(self):
        '''31 - get all READERS'''
        try:
            items = self.session.query(models.Author).all()
            return items
        except Exception as err:
            print("Get error! ", err)
            raise err

    def get_all_authors(self):
        '''32 - get all AUTHORS'''
        try:
            items = self.session.query(models.Author).all()
            return items
        except Exception as err:
            print("Get error! ", err)
            raise err

    def get_all_books(self):
        '''33 - get all BOOKS'''
        try:
            items = self.session.query(models.Book).all()
            return items
        except Exception as err:
            print("Get error! ", err)
            raise err


    def get_all_subscriptions(self):
        '''34 - get all SUBSCRIPTIONS'''
        try:
            items = self.session.query(models.Subscription).all()
        except Exception as err:
            print("Get error! ", err)
            raise err
        return items

    def get_all_orders(self):
        '''35 - get all ORDER_LIST'''
        try:
            items = self.session.query(models.Order).all()
        except Exception as err:
            print("Get error! ", err)
            raise err
        return items

    def add_reader(self, name, address, phone, email):
        '''36 - add READER'''
        item = models.Reader(name, address, phone, email)
        try:
            if not isinstance(item, models.Reader):
                raise Exception('Invalid arguments')

            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
            return item.id
        except Exception as err:
            print("Add error! ", err)
            raise err

    def add_author(self, name, birthday):
        '''37 - add AUTHOR'''
        item = models.Author(name, birthday)
        try:
            if not isinstance(item, models.Author):
                raise Exception('Invalid arguments')

            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
            return item.id
        except Exception as err:
            print("Add error! ", err)
            raise err

    def add_book(self, auth_id, year, pages, title):
        '''38 - add BOOK'''
        item = models.Book(auth_id, year, pages, title)
        try:
            if not isinstance(item, models.Book):
                raise Exception('Invalid arguments')

            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
            return item.id
        except Exception as err:
            print("Add error! ", err)
            raise err

    def add_subscription(self, reader_id, since, until, issues):
        '''39 - add SUBSCRIPTION'''
        item = models.Subscription(reader_id, since, until, issues)
        try:
            if not isinstance(item, models.Subscription):
                raise Exception('Invalid arguments')

            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
            return item.id
        except Exception as err:
            print("Add error! ", err)
            raise err

    def add_order(self, subscr_id, book_id, time, t_return):
        '''40 - add ORDER_LIST'''
        item = models.Order(book_id, subscr_id, time, t_return)
        try:
            if not isinstance(item, models.Order):
                raise Exception('Invalid arguments')

            self.session.add(item)
            self.session.commit()
            self.session.refresh(item)
            return item.id
        except Exception as err:
            print("Add error! ", err)
            raise err