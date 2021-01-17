from datetime import date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    birthday = Column('birthday', Integer)

    def __init__(self, name: str, birthday: int):
        self.name = name
        self.birthday = birthday

    def __repr__(self):
        return "<Author(id='%s', name='%s', birthday='%s')>\n" % (
            self.id, self.name, self.birthday)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='cascade'))
    year_of_writing = Column('year_of_writing', Integer)
    pages = Column('pages', Integer)
    title = Column('title', String)
    Author = relationship("Author", cascade="all, delete", backref="books")
    Order = relationship("Order", cascade="all, delete", backref="books")

    def __init__(self, author_id: int, year_of_writing: int,
                 pages: int, title: str):
        self.author_id = author_id
        self.year_of_writing = year_of_writing
        self.pages = pages
        self.title = title

    def __repr__(self):
        return "<Book(id='%s', author_id='%s', year_of_writing='%s', pages='%s', title='%s')>\n" % (
            self.id, self.author_id, self.year_of_writing, self.pages, self.title)


class Reader(Base):
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    address = Column('address', String)
    phone_number = Column('phone_number', String)
    email = Column('email', String)

    def __init__(self, name: str, address: str, phone_number: str,
                 email: str):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email

    def __repr__(self):
        return "<Reader(id='%s', name='%s', address='%s', phone_number='%s', email='%s')>\n" % (
            self.id, self.name, self.address, self.phone_number, self.email)


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    reader_id = Column(Integer, ForeignKey('readers.id'))
    valid_since = Column('valid_since', Date)
    valid_until = Column('valid_until', Date)
    number_of_issues = Column('number_of_issues', Integer)
    Reader = relationship("Reader", cascade="all, delete", backref="subscriptions")
    Order = relationship("Order", cascade="all, delete", backref="subscriptions")

    def __init__(self, reader_id: int, valid_since: date,
                 valid_until: date, number_of_issues: int):
        self.reader_id = reader_id
        self.valid_since = valid_since
        self.valid_until = valid_until
        self.number_of_issues = number_of_issues

    def __repr__(self):
        return "<Subscription(id='%s', reader_id='%s', valid_since='%s', valid_until='%s', number_of_issues='%s')>\n" % (
            self.id, self.reader_id, self.valid_since, self.valid_until, self.number_of_issues)


class Order(Base):
    __tablename__ = 'order_list'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    subscr_id = Column(Integer, ForeignKey('subscriptions.id'))
    time = Column('time', Date)
    t_return = Column('t_return', Date)
    Book = relationship("Book", cascade="all, delete", backref="order_list")
    Subscription = relationship("Subscription", cascade="all, delete", backref="order_list")

    def __init__(self, book_id: int, subscr_id: int, time: date,
                 t_return: date):
        self.book_id = book_id
        self.subscr_id = subscr_id
        self.time = time
        self.t_return = t_return

    def __repr__(self):
        return "<Order(id='%s', book_id='%s', subscr_id='%s', time='%s', t_return='%s')>\n" % (
            self.id, self.book_id, self.subscr_id, self.time, self.t_return)
