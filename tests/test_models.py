import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base, Book, Author, Subject, Bookshelf

# Test database URL
DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope='module')
def setup_database():
    # Setup the database
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Populate the database with some test data
    author = Author(name="Test Author")
    book = Book(
        title="Test Book",
        author=author,
        genre="Fiction",
        language="en",
        downloads=100,
        download_links="http://example.com/testbook"
    )
    subject = Subject(name="Test Subject")
    bookshelf = Bookshelf(name="Test Bookshelf")
    
    book.subjects.append(subject)
    book.bookshelves.append(bookshelf)
    
    session.add(book)
    session.commit()
    
    yield session
    
    # Teardown the database
    Base.metadata.drop_all(engine)
    session.close()

def test_author(setup_database):
    session = setup_database
    author = session.query(Author).filter_by(name="Test Author").first()
    assert author is not None
    assert author.name == "Test Author"

def test_book(setup_database):
    session = setup_database
    book = session.query(Book).filter_by(title="Test Book").first()
    assert book is not None
    assert book.title == "Test Book"
    assert book.author.name == "Test Author"
    assert book.genre == "Fiction"
    assert book.language == "en"
    assert book.downloads == 100
    assert "http://example.com/testbook" in book.download_links

def test_subject(setup_database):
    session = setup_database
    subject = session.query(Subject).filter_by(name="Test Subject").first()
    assert subject is not None
    assert subject.name == "Test Subject"
    assert len(subject.books) == 1
    assert subject.books[0].title == "Test Book"

def test_bookshelf(setup_database):
    session = setup_database
    bookshelf = session.query(Bookshelf).filter_by(name="Test Bookshelf").first()
    assert bookshelf is not None
    assert bookshelf.name == "Test Bookshelf"
    assert len(bookshelf.books) == 1
    assert bookshelf.books[0].title == "Test Book"
