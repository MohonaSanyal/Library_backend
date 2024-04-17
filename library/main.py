from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, jsonify
from .models import User, Section, Book, IssueRequests, Issue, Feedback
from . import db
from datetime import datetime, timedelta
main = Blueprint('main', __name__)

@main.route('/')
def index():
    status = {"Status": "Active"}  
    return make_response(jsonify(status), 200)


#Create Section
@main.route('/create/section', methods=['POST'])
def create_section():
    time = datetime.now()
    datetime_string =time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_time = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    req = request.json
    name = req['name']
    desc = req['desc']
    new_section = Section(name=name, desc=desc, date_created = formatted_time)
    db.session.add(new_section)
    db.session.commit()
    return make_response(jsonify({"name":name, "desc":desc, "created": formatted_time}), 200)

#Edit Section
@main.route('/edit/section/<section_id>', methods=['PATCH'])
def edit_session(section_id):
    req = request.json
    this_section = Section.query.get_or_404(section_id)
    if "name" in req:
        this_section.name = req["name"]
    if "desc" in req:
        this_section.desc = req["desc"]
    db.session.commit()
    return make_response(jsonify({"name": this_section.name, "desc": this_section.desc, "id": this_section.id}), 200)

#Delete Section
@main.route('/delete/section/<section_id>', methods=['DELETE'])
def delete_section(section_id):
    this_section = Section.query.get_or_404(section_id)
    db.session.delete(this_section)
    db.session.commit()
    return make_response(jsonify({"delete": "successful"}))

#Create Books
@main.route('/create/book', methods=['POST'])
def create_book():
    req = request.json
    name = req['name']
    ebook_price = req['ebook_price']
    section_id = req['section_id']
    authors = req['authors']
    content = req['content']
    new_book = Book(name=name, content=content, ebook_price=ebook_price, authors=authors, section_id=section_id)
    db.session.add(new_book)
    db.session.commit()
    return make_response(jsonify({"name":name, "ebook_price":ebook_price, "authors":authors, "content":content, "section_id":section_id}), 200)

# #Edit book
@main.route('/edit/book/<book_id>', methods=['PATCH'])
def edit_book(book_id):
    req = request.json
    this_book = Book.query.get_or_404(book_id)
    if "name" in req:
        this_book.name = req["name"]
    if "ebook_price" in req:
        this_book.ebook_price = req["ebook_price"]
    if "section_id" in req:
        this_book.section_id = req["section_id"]
    if "authors" in req:
        this_book.authors = req["authors"]
    if "content" in req:
        this_book.content = req["content"]
    db.session.commit()
    return make_response(jsonify({"name":this_book.name, "ebook_price":this_book.ebook_price, "authors":this_book.authors, "content":this_book.content, "section_id":this_book.section_id}), 200)

# #Delete book
@main.route('/delete/book/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    this_book = Book.query.get_or_404(book_id)
    db.session.delete(this_book)
    db.session.commit()
    return make_response(jsonify({"delete": "successful"}))

#Get book
@main.route('/books', methods=['GET'])
def get_section():
    response = {"sections": []}
    sections = Section.query.all()
    for section in sections:
        this_section = {"items": [], "id": section.id, "name": section.name, "desc": section.desc}
        items = Book.query.filter(Book.section_id == section.id)
        for item in items:
            this_item = {"id": item.id, "ebook_price": item.ebook_price, "name": item.name, "authors": item.authors, "content": item.content}
            this_section["items"].append(this_item)
        response["sections"].append(this_section)
    return make_response(jsonify(response), 200)

#Request book
@main.route('/books/req/<book_id>', methods=['POST'])
def request_book(book_id):
    req = request.json
    user = req["user_id"]
    new_req = IssueRequests(user_id = user, book_id = book_id)
    db.session.add(new_req)
    db.session.commit()
    return make_response(jsonify({"user_id":user, "book_id":book_id}), 200)

#Return book
@main.route('/books/return/<issue_id>', methods=['POST'])
def return_book(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    return make_response(jsonify({"issue_id":issue_id, "status":"return"}), 200)

#Feedback book
@main.route('/feedback/<book_id>', methods=['POST'])
def give_feedback(book_id):
    req = request.json
    user = req["user_id"]
    feedback = req["feedback"]
    new_feedback = Feedback(user_id = user, book_id = book_id, feedback = feedback)
    db.session.add(new_feedback)
    db.session.commit()
    return make_response(jsonify({"user_id":user, "book_id":book_id, "feedback":feedback}), 200)

#Issue book
@main.route('/books/req/accept/<book_id>', methods=['POST'])
def accept_req_book(book_id):
    req = request.json
    user = req["user_id"]
    req_id = req["req_id"]
    req = IssueRequests.query.get_or_404(req_id)
    db.session.delete(req)
    db.session.commit()
    time = datetime.now()
    datetime_string =time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_time = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    return_date = formatted_time + timedelta(days=7)
    new_accept_req_book = Issue(user_id = user, book_id = book_id, date_issued = formatted_time, return_date = return_date)
    db.session.add(new_accept_req_book)
    db.session.commit()
    return make_response(jsonify({"user_id":user, "book_id":book_id, "Id":new_accept_req_book.id, "date_issued":formatted_time, "return_date":return_date}), 200)


#Revoke access
@main.route('/books/revoke/<issue_id>', methods=['POST'])
def revoke_access(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    return make_response(jsonify({"issue_id":issue_id, "status":"revoke"}), 200)


#Book to user mapping
@main.route('/books/all', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    book_mapping = []
    for book in books:
        users_list = []
        issues = Issue.query.all()
        for issue in issues:
            if issue.book_id == book.id:
                users_list.append({"user":issue.user_id, "issue_id":issue.id})
        book_mapping.append({"book_id":book.id, "users_list":users_list, "name": book.name})
    return make_response(jsonify({"books":book_mapping}))

#Book to user mapping requests
@main.route('/books/all/req', methods=['GET'])
def get_all_books_req():
    books = Book.query.all()
    book_mapping = []
    for book in books:
        users_list = []
        issues = IssueRequests.query.all()
        for issue in issues:
            if issue.book_id == book.id:
                users_list.append({"user":issue.user_id, "issue_id":issue.id})
        book_mapping.append({"book_id":book.id, "users_list":users_list, "name": book.name})
    return make_response(jsonify({"books":book_mapping}))

#Search
@main.route('/search/books', methods=['POST'])
def search():
    req = request.json
    search_text = req["search"]
    search = "%{}%".format(search_text)
    booklist = Book.query.filter(Book.name.like(search)).all()
    output = []
    for book in booklist:
        this_book = {'name':book.name, 'price':book.ebook_price, 'authors':book.authors, 'content':book.content}
        output.append(this_book)
    return make_response(jsonify({"books":output}))


#Monthly activity report
@main.route('/report/<email>', methods=['GET'])
def report(email):
    this_user = User.query.filter_by(email=email).first()
    issues = Issue.query.filter_by(user_id = this_user.id)
    output = []
    for issue in issues:
        this_book = Book.query.filter_by(id = issue.book_id).first()
        this_output = {'name':this_book.name, 'price':this_book.ebook_price, 'authors':this_book.authors, 'content':this_book.content}
        output.append(this_output)
    return make_response(jsonify({"books":output}))


#Daily reminder
@main.route('/reminder', methods=['GET'])
def reminder():
    output = []
    users = User.query.all()
    for user in users:
        user_time = user.last_visited
        updated_time = user_time + timedelta(days = 1)
        time = datetime.now()
        datetime_string =time.strftime("%Y-%m-%d %H:%M:%S")
        formatted_time = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
        if formatted_time > updated_time:
            output.append(user.email)
    return make_response(jsonify({"users":output}))
