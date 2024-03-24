from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    books = db.relationship("Book", backref="category")


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))


@app.route("/")
def index():
    return "Наша родная библиотка"


@app.route("/books_by_category", methods=["GET"])
def get_books_by_category():
    category_name = request.args.get("category")

    if not category_name:
        return "Категории нету такой"

    category = Category.query.filter_by(name=category_name).first()

    if not category:
        return "Категории не найдено"

    books_data = [{"title": book.title, "author": book.author} for book in books]
    return jsonify(books_data)


def fill_database():
    data = [
        {"category": "Autobiography", "title": "Mein Kampf", "author": "Adolf H."},
        {"category": "Autobiography", "title": "Hitlers Zweites Buch", "author": "Adolf H."},
    ]
    for item in data:
        category = Category.query.filter_by(name=item["category"]).first()
        if not category:
            category = Category(name=item["category"])
            db.session.add(category)
            db.session.commit()
        book = Book(title=item["title"], author=item["author"], category=category)
        db.session.add(book)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        fill_database()
    app.run(debug=True)
