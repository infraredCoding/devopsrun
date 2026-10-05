from flask import Flask

app = Flask(__name__)


def _fetch_writer_name(book_name):
    d = {
            "The Great Gatsby": "F. Scott Fitzgerald",
            "To Kill a Mockingbird": "Harper Lee",
            "1984": "George Orwell",
        }
    if book_name in d:
        writer_name = d[book_name]
    else:
        writer_name = "Book not found"

    return writer_name


@app.route('/<string:book_name>')
def get_writer_name(book_name):
    writer_name = _fetch_writer_name(book_name)
    return f"Writer Name: {writer_name}"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)