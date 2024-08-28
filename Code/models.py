from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()

# User table
class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True,primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False) 
    role = Column(Text, nullable=False, default="user") # librarian or user   
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','password', 'role',)
user_schema = UserSchema()
        

# Section table
class Section(db.Model):
    __tablename__ = "section"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    create_id = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False)
    update_id = Column(Integer, nullable=False)
    update_time = Column(DateTime, nullable=False)
    def __init__(self, name, content, create_time, update_time, create_id, update_id):
        self.name = name
        self.content = content
        self.create_id = create_id
        self.create_time = create_time
        self.update_id = update_id
        self.update_time = update_time    
class SectionSchema(ma.Schema):
    class Meta:
        fields = ('id','name','content','create_id','create_time','update_id','update_time')
section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)


# Books table
class Book(db.Model):
    __tablename__ = "book"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    authors = Column(Text, nullable=False)
    book_link = Column(Text, nullable=False)
    section_id = Column(Integer, ForeignKey("section.id"), nullable=False)
    # section = relationship("Section",back_populates="books")
    def __init__(self, name, content, authors, book_link, section_id):
        self.name = name
        self.content = content
        self.authors = authors
        self.book_link = book_link
        self.section_id = section_id
class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "content", "authors","book_link","section_id")
book_schema = BookSchema()
books_schema = BookSchema(many=True)


# UserBook table
class UserBook(db.Model):
    __tablename__ = "user_book"
    id = Column(Integer, primary_key = True, autoincrement = True )    
    request = Column(DateTime, nullable = False)
    issue = Column(DateTime)
    due = Column(DateTime)
    return_date = Column(DateTime)
    revoke_date = Column(DateTime)
    status = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"), nullable = False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable = False)    
    def __init__(self, request, issue, due, return_date, revoke_date, status, user_id, book_id):
        self.request = request
        self.issue = issue
        self.due = due
        self.return_date = return_date
        self.revoke_date = revoke_date
        self.status = status
        self.user_id = user_id
        self.book_id = book_id
class UserBookSchema(ma.Schema):
    class Meta:
        fields = ("id", "issue", "request","due","return_date", "revoke_date","status","user_id", "book_id")
user_book_schema = UserBookSchema()
user_books_schema = UserBookSchema(many=True)