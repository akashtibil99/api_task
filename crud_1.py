import os
from flask import Flask, request, jsonify

app = Flask(__name__)

books = {
    1: {"title": "The Alchemist", "author": "Paulo Coelho", "year": 1988, "genre": "Fiction"},
    2: {"title": "Atomic Habits", "author": "James Clear", "year": 2018, "genre": "Self-help"},
    3: {"title": "Python Crash Course", "author": "Eric Matthes", "year": 2019, "genre": "Programming"}
}

# GET - fetch all books
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

# GET - fetch single book by id
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = books.get(book_id)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# POST - add new book
@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    book_id = max(books.keys()) + 1 if books else 1
    books[book_id] = data
    return jsonify({"id": book_id, "data": data}), 201

# PUT - update book by id
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    if book_id in books:
        books[book_id] = request.json
        return jsonify({"id": book_id, "data": books[book_id]})
    return jsonify({"error": "Book not found"}), 404

# DELETE - remove book by id
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    if book_id in books:
        deleted = books.pop(book_id)
        return jsonify({"deleted": deleted})
    return jsonify({"error": "Book not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
