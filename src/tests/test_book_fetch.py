
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import _fetch_writer_name


@pytest.mark.parametrize(
    "book_input, expected_writer",
    [
        ("The Great Gatsby", "F. Scott Fitzgerald"),
        ("To Kill a Mockingbird", "Harper Lee"),
        ("1984", "George Orwell"),
        ("Moby Dick", "Book not found"),  # Testing the fallback/else case
    ]
)
def test_fetch_writer_name(book_input, expected_writer):
    assert _fetch_writer_name(book_input) == expected_writer
