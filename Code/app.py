from flask import Flask, request, jsonify
from models import *
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies
from datetime import datetime, timedelta
from worker import celery_init_app
import flask_excel as excel
from celery import Celery
from task import add, create_csv
from celery.result import AsyncResult



celery_app = None
app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

# Initialize Database
db.init_app(app)
celery_app =celery_init_app(app)
bcrypt = Bcrypt(app)

CORS(app, supports_credentials=True)

with app.app_context():
    db.create_all()

# Homepage route
@app.route("/")
def homepage():
    return "Welcome to Library Management App"

#celery demo route
@app.route("/start_export")
def start_export():
    task = create_csv.delay()
    return jsonify({"task_id": task.id}), 200
@app.route("/start_export/<task_id>")
def get_task_status(task_id):
    task = create_csv.AsyncResult(task_id)
    if task.ready():
        return jsonify({"status": "Completed"}), 200
    else:
        return jsonify({"status": "Processing"}), 202

# @app.route("/celery")
# def celery_demo():
#     task= add.delay(1,2)
#     return jsonify({"task_id":task.id}), 200


# @app.route("/celery/<task_id>")
# def celery_result(task_id):
#     task = add.AsyncResult(task_id)
#     if task.ready():
#         return jsonify({"result":task.get()}), 200
#     else:
#         return jsonify({"status":"Processing"}), 202



# New User Register Route
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"message": "User exists in database"}), 409

    new_user = User(name=name, email=email, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "New User Created Successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error While Creating User"}), 500

# User Login Route
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    user_check = User.query.filter_by(email=email).first()

    if not user_check:
        return jsonify({"error": "User does not exist"}), 404
    if not bcrypt.check_password_hash(user_check.password, password):
        return jsonify({"error": "Incorrect password"}), 401

    access_token = create_access_token(identity={
        "id": user_check.id,
        "role": user_check.role
    })
    return jsonify({"message": "Login Successful", "access_token": access_token}), 200

# User Logout
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"message": "Logout successful"})
    # Removing or invalidating the JWT cookies
    unset_jwt_cookies(response)
    return jsonify({"message": "Logout successful"}), 200

# User info for storage and login
@app.route("/userinfo", methods=["GET"])
@jwt_required()
def userinfo():
    current_user = get_jwt_identity()
    id = current_user["id"]
    user_exists = User.query.filter_by(id=id).first()
    if not user_exists:
        return jsonify({"error": "User does not exist"}), 404
    user = user_schema.dump(user_exists)
    return jsonify(user), 200

# Create Section Route - C of CRUD
@app.route("/section", methods=["POST"])
@jwt_required()
def create_section():
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized"}), 401
    data = request.json
    name = data.get("name")
    content = data.get("content")
    create_id = cur_user["id"]
    current_time = datetime.now()

    section_exists = Section.query.filter_by(name=name).first()
    if section_exists:
        return jsonify({"error": "Section already exists, create a new section"}), 406

    new_section = Section(name=name, content=content, create_id=create_id, create_time=current_time, update_id=create_id, update_time=current_time)
    try:
        db.session.add(new_section)
        db.session.commit()
        return jsonify({"message": "New Section Created Successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error Creating Section"}), 500

# Read all sections - R of CRUD
@app.route("/section", methods=["GET"])
@jwt_required()
def read_section():
    sections = Section.query.all()
    data = {"sections": sections_schema.dump(sections)}
    return jsonify(data)

# Select section by ID - Read
@app.route("/section/<int:section_id>", methods=["GET"])
@jwt_required()
def read_section_by_id(section_id):
    section = Section.query.filter_by(id=section_id).first()
    data = {"section": section_schema.dump(section)}
    return jsonify(data)

# Update section - U of CRUD
@app.route("/section/<int:section_id>", methods=["PUT"])
@jwt_required()
def update_section(section_id):
    section = Section.query.get(section_id)
    if not section:
        return jsonify({"error": "Section not found"}), 404
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to update section"}), 401
    data = request.json
    section.name = data.get("name")
    section.content = data.get("content")
    section.update_id = cur_user["id"]
    section.update_time = datetime.now()
    try:
        db.session.commit()
        return jsonify({"message": "Section updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error while updating Section"}), 500

# Delete section - D of CRUD
@app.route("/section/<int:section_id>", methods=["DELETE"])
@jwt_required()
def delete_section(section_id):
    section = Section.query.get(section_id)
    if not section:
        return jsonify({"error": "Section not found"}), 404
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to delete section"}), 401
    try:
        db.session.delete(section)
        db.session.commit()
        return jsonify({"message": "Section deleted successfully"})
    except Exception as e:
        return jsonify({"error": "Delete section not successful"}), 500

# Create new books - C of CRUD
@app.route("/book/<int:section_id>", methods=["POST"])
@jwt_required()
def create_book(section_id):
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to create book"}), 401
    data = request.json
    data["section_id"] = section_id
    new_book = Book(**data)
    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify({"message": "New Book Created Successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error Creating book"}), 500

# Read all books in a section - R of CRUD
@app.route("/book/section/<int:id>", methods=["GET"])
@jwt_required()
def get_book_from_section(id):
    books = Book.query.filter_by(section_id=id)
    data = {"books": books_schema.dump(books)}
    return jsonify(data)

# Select of a particular book
@app.route("/book/<int:id>", methods=["GET"])
@jwt_required()
def get_particular_book(id):
    book = Book.query.filter_by(id=id).first()
    data = {"book": book_schema.dump(book)}
    return jsonify(data)

# Select all books
@app.route("/book", methods=["GET"])
@jwt_required()
def get_all_books():
    books = Book.query.all()
    data = {"books": books_schema.dump(books)}
    return jsonify(data)

# Update Book info - U of CRUD
@app.route("/book/<int:book_id>", methods=["PUT"])
@jwt_required()
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to update book"}), 401
    data = request.json
    for key, value in data.items():
        setattr(book, key, value)
    try:
        db.session.commit()
        return jsonify({"message": "Book has been updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error while updating Book"}), 500

# Delete book - D of CRUD
@app.route("/book/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to delete book"}), 401
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book is deleted successfully"})
    except Exception as e:
        return jsonify({"message": "Book was not deleted"})

# Book Request - C of CRUD
@app.route("/bookrequest/<int:user_id>/<int:book_id>", methods=["POST"])
@jwt_required()
def bookrequest(user_id, book_id):
    cur_user = get_jwt_identity()
    if cur_user["role"] != "user":
        return jsonify({"error": "Not a user - can't request book"}), 401
    no_of_books = UserBook.query.filter(UserBook.user_id == user_id, (UserBook.status=='request') | (UserBook.status=='approve')).count()
    if no_of_books == 5:
        return jsonify({"error": "You have exceeded your book issue quota"}), 429
    request = datetime.now()
    status = "request"
    request_exists = UserBook.query.filter_by(user_id=user_id, book_id=book_id, return_date=None).first()
    if request_exists:
        return jsonify({"error": "Duplicate request"}), 406
    new_req = UserBook(user_id=user_id, book_id=book_id, request=request, issue=None, due=None, return_date=None, revoke_date=None, status=status)
    try:
        db.session.add(new_req)
        db.session.commit()
        return jsonify({"message": "New book request created successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating new book request"}), 500

# Read Books Request by status (request, approve, overdue, return, revoke) - R of CRUD for Book Request table
@app.route("/bookrequest/status", methods=["GET"])
@jwt_required()
def get_bookrequest_by_status():
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to view book requests by status"}), 401
    bookreq = UserBook.query.filter((UserBook.status != "approve") & (UserBook.status != "return") & (UserBook.status != "reject")&(UserBook.status!="revoke")).all()
    data = {"bookrequest": user_books_schema.dump(bookreq)}
    return jsonify(data)
@app.route("/bookapprove/status", methods=["GET"])
@jwt_required()
def get_bookapprove_by_status():
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to view book requests by status"}), 401
    bookreq = UserBook.query.filter(UserBook.status == "approve").all()
    data = {"bookrequest": user_books_schema.dump(bookreq)}
    return jsonify(data)

# Read Books Request by user (request, approve, overdue, return, revoke) - R of CRUD for Book Request table
@app.route("/bookrequest/user", methods=["GET"])
@jwt_required()
def get_bookrequest_by_user():
    cur_user = get_jwt_identity()
    if cur_user["role"] != "user":
        return jsonify({"error": "Only users can view their requests"}), 401
    user_id = cur_user["id"]
    bookreq = UserBook.query.filter((UserBook.user_id == user_id) & (UserBook.status != "return")&(UserBook.status!="revoke")).all()
    data = {"bookrequest": user_books_schema.dump(bookreq)}
    return jsonify(data)

# Update User book status (approve, reject, return, revoke, renew) - U of CRUD
@app.route("/bookrequest/status/<int:id>", methods=["PUT"])
@jwt_required()
def update_bookrequest_status(id):
    bookrequest = UserBook.query.filter_by(id=id).first()
    if not bookrequest:
        return jsonify({"error": "Book against user not found, can't fulfill update"}), 404
    cur_user = get_jwt_identity()
    data = request.json
    status = data.get("status")
    if cur_user["role"] == "librarian":
        if status in ["return", "renew"]:
            return jsonify({"error": "Status update request is not possible for librarian"}), 401
        if status == "approve":
            bookrequest.status = "approve"
            bookrequest.issue = datetime.now()
            bookrequest.due = datetime.now() + timedelta(days=7)
        if status == "reject":
            bookrequest.status = "reject"
        if status == "revoke":
            bookrequest.status = "revoke"
            bookrequest.revoke_date = datetime.now()
            bookrequest.return_date = datetime.now()
    if cur_user["role"] == "user":
        if status in ["approve", "reject", "revoke"]:
            return jsonify({"error": "Status update request is not possible for User"}), 401
        if status == "return":
            bookrequest.status = "return"
            bookrequest.return_date = datetime.now()
        if status == "renew":
            bookrequest.status = "renew"
    try:
        db.session.commit()
        return jsonify({"message": "Book request updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error while updating book request status"}), 500

if __name__ == "__main__":
    app.run(debug=True)
    # excel.init_excel(app)
