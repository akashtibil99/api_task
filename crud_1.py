from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# In-memory store (resets when server restarts)
books = {}
next_id = 1

# Helper for errors
def error(message, code):
    return jsonify({"error": message}), code

# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# Get all books (optional filter by author or genre)
@app.route("/books", methods=["GET"])
def list_books():
    author = request.args.get("author")
    genre = request.args.get("genre")
    data = list(books.values())

    if author:
        data = [b for b in data if b.get("author") == author]
    if genre:
        data = [b for b in data if b.get("genre") == genre]

    return jsonify(data), 200

# Get a single book by ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = books.get(book_id)
    if not book:
        return error("Book not found", 404)
    return jsonify(book), 200

# Add a new book
@app.route("/books", methods=["POST"])
def create_book():
    global next_id
    if not request.is_json:
        return error("Expected JSON body", 415)

    payload = request.get_json()
    required = ["title", "author", "genre", "year"]
    missing = [k for k in required if k not in payload]
    if missing:
        return error(f"Missing fields: {', '.join(missing)}", 400)

    book = {
        "id": next_id,
        "title": str(payload["title"]).strip(),
        "author": str(payload["author"]).strip(),
        "genre": str(payload["genre"]).strip(),
        "year": int(payload["year"])
    }
    books[next_id] = book
    next_id += 1
    return jsonify(book), 201

# Update an existing book
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    if not request.is_json:
        return error("Expected JSON body", 415)
    if book_id not in books:
        return error("Book not found", 404)

    payload = request.get_json()
    book = books[book_id]

    for field in ["title", "author", "genre", "year"]:
        if field in payload and payload[field] is not None:
            if field == "year":
                book[field] = int(payload[field])
            else:
                book[field] = str(payload[field]).strip()

    books[book_id] = book
    return jsonify(book), 200

# Delete a book
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    if book_id not in books:
        return error("Book not found", 404)
    del books[book_id]
    return jsonify({"message": "Deleted"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
