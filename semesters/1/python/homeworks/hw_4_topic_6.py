"""
Note: Немного модифицировал задание, так как оно показалось очень легким :)
"""

import random
from enum import StrEnum
from functools import wraps
import typing as t
from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    field_validator,
)


"""Errors"""

class LibraryError(Exception):
    pass


class CategoryUnavailable(LibraryError):
    pass


class BookNotFound(LibraryError):
    pass


class BookNotAvailable(LibraryError):
    pass


"""Logging decorator"""

P = t.ParamSpec("P")
T = t.TypeVar("T")


def log_operation(function: t.Callable[P, T]) -> t.Callable[P, T]:
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"LOG: Called `{function.__name__}`")

        res = function(*args, **kwargs)

        print(f"LOG: Finished `{function.__name__}`")
        return res

    return wrapper


"""Models and Filters"""

class BooksFilterField(StrEnum):
    ID = "id"
    TITLE = "title"
    AUTHOR = "author"
    YEAR = "year"


class BooksFilter(BaseModel):
    field: BooksFilterField
    value: t.Any


class User(BaseModel):
    name: StrictStr
    email: StrictStr
    membership_id: StrictInt


class Book(BaseModel):
    _CATEGORIES_BLACKLIST: t.ClassVar[list[str]] = ["romance"]

    id: StrictInt
    title: StrictStr
    author: StrictStr
    year: StrictInt
    available: StrictBool
    categories: list[str]

    def apply_filters(self, filters: list[BooksFilter]) -> bool:
        return all(
            [
                self.__getattribute__(filter_.field) == filter_.value
                for filter_ in filters
            ]
        )

    @field_validator("categories")
    def validate_categories(cls, categories: list[str]) -> list[str]:
        for category in categories:
            if category in cls._CATEGORIES_BLACKLIST:
                msg_exc = f"Category `{category}` unavailable"
                raise CategoryUnavailable(msg_exc)

        return categories


"""Library"""

class Library:
    def __init__(self) -> None:
        self._books: list[Book] = []
        self._users: list[User] = []

        self._last_added_id: int = -1

    @log_operation  # log only `total_books` method to make output clean
    def total_books(self) -> int:
        return len(self._books)

    def add_book(
        self, title: str, author: str, year: int, categories: list[str]
    ) -> None:
        book_id = self._last_added_id + 1
        book = Book(
            id=book_id,
            title=title,
            author=author,
            year=year,
            categories=categories,
            available=True,
        )
        self._books.append(book)

        self._last_added_id += 1

    def borrow_book(self, book_id: int) -> None:
        book = next(
            self.find_books(
                filters=[BooksFilter(field=BooksFilterField.ID, value=book_id)]
            )
        )
        book.available = False

    def find_books(self, filters: list[BooksFilter]) -> t.Generator[Book, None, None]:
        matches = (book for book in self._books if book.apply_filters(filters=filters))
        yield from matches

    def is_book_borrow(self, book_id: int, need_raise: bool = False) -> bool:
        filter_ = BooksFilter(field=BooksFilterField.ID, value=book_id)

        if len(found_books := list(self.find_books(filters=[filter_]))) == 0:
            msg_exc = f"Book with id `{book_id}` not found"
            raise BookNotFound(msg_exc)

        book = found_books[0]

        if need_raise and not book.available:
            msg_exc = f"Book with id `{book_id}` unavailable"
            raise BookNotAvailable(msg_exc)

        return not book.available

"""Initialization and testing"""

def _init_library() -> Library:
    library = Library()

    titles = [f"Title {i}" for i in range(5)]
    authors = [f"Author {i}" for i in range(5)]
    categories = [f"Catetory {i}" for i in range(10)]

    for _ in range(30):
        title = random.choice(titles)
        author = random.choice(authors)
        categories_ = random.choices(categories, k=2)

        library.add_book(
            title=title,
            author=author,
            year=random.randint(1900, 2025),
            categories=categories_,
        )

    return library


def main():
    library = _init_library()

    # Calculate books count
    print(f"Total books: {library.total_books()}")
    """
    Output:
    LOG: Called `total_books`
    LOG: Finished `total_books`
    Total books: 30
    """

    # Add book with unavailable category
    try:
        library.add_book(
            title="Clean Architecture",
            author="Uncle Bob",
            year=2012,
            categories=["romance"],
        )
    except CategoryUnavailable as exc:
        print(str(exc))
    """
    Output:
    Category `romance` unavailable
    """

    # Find books by filter
    filters = [BooksFilter(field=BooksFilterField.AUTHOR, value="Author 1")]
    found_books = library.find_books(filters)
    for book in found_books:
        print(f"Found book: {book}")
    """
    Output:
    Found book: id=2 title='Title 4' author='Author 1' year=2023 available=True categories=['Catetory 3', 'Catetory 5']
    Found book: id=8 title='Title 4' author='Author 1' year=1990 available=True categories=['Catetory 3', 'Catetory 3']
    Found book: id=9 title='Title 1' author='Author 1' year=2005 available=True categories=['Catetory 8', 'Catetory 0']
    Found book: id=11 title='Title 2' author='Author 1' year=1951 available=True categories=['Catetory 3', 'Catetory 7']
    Found book: id=16 title='Title 0' author='Author 1' year=2000 available=True categories=['Catetory 3', 'Catetory 8']
    Found book: id=19 title='Title 2' author='Author 1' year=1916 available=True categories=['Catetory 0', 'Catetory 3']
    Found book: id=26 title='Title 2' author='Author 1' year=1916 available=True categories=['Catetory 5', 'Catetory 1']
    """

    # Borrow book
    is_book_borrow = library.is_book_borrow(book_id=2)
    print(is_book_borrow)
    """
    Output:
    False
    """

    library.borrow_book(book_id=2)

    is_book_borrow = library.is_book_borrow(book_id=2)
    print(is_book_borrow)
    """
    Output:
    True
    """

    try:
        library.is_book_borrow(book_id=2, need_raise=True)
    except BookNotAvailable as exc:
        print(str(exc))
    """
    Output
    Book with id `2` unavailable
    """


if __name__ == "__main__":
    main()
