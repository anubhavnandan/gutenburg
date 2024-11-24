from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Association table for many-to-many relationship between books and subjects
book_subject_association = Table('book_subject', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)

# Association table for many-to-many relationship between books and bookshelves
book_bookshelf_association = Table('book_bookshelf', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('bookshelf_id', Integer, ForeignKey('bookshelves.id'))
)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    genre = Column(String)
    language = Column(String, nullable=False)
    downloads = Column(Integer, default=0)
    download_links = Column(Text)
    
    author = relationship("Author", back_populates="books")
    subjects = relationship("Subject", secondary=book_subject_association, back_populates="books")
    bookshelves = relationship("Bookshelf", secondary=book_bookshelf_association, back_populates="books")

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship("Book", back_populates="author")

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship("Book", secondary=book_subject_association, back_populates="subjects")

class Bookshelf(Base):
    __tablename__ = 'bookshelves'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship("Book", secondary=book_bookshelf_association, back_populates="books")

# Database connection
DATABASE_URL = "postgresql://user:password@localhost/books_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    # Create all tables
    Base.metadata.create_all(engine)
