from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))

    def __repr__(self):

        return f"{self.book_name}, {self.author}, {self.publisher}"


@app.route('/')
def index():
    return "Hello"


@app.route('/books')
def get_books():
    books = Books.query.all()

    output = []
    for book in books:
        book_data = {'Book': book.book_name, 'Author': book.author, 'Publisher': book.publisher}

        output.append(book_data)

    return {"books": output}


@app.route('/books/<id>')
def get_book(id):
    book = Books.query.get_or_404(id)
    return {'Book': book.book_name, 'Author': book.author, 'Publisher': book.publisher}


@app.route('/books', methods=['POST'])
def add_book():
    book = Books(book_name=request.json['Book'], author=request.json['Author'], publisher=request.json['Publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}


@app.route('/books/<id>', methods=['DELETE'])
def delete_book():
    book = Books.query.get(id)
    if book is None:
        return {'error': 'not found'}
    db.session.delete(book)
    db.session.commit()
    return {"message": "deleted"}


if __name__ == "__main__":
    app.run(debug=True)
