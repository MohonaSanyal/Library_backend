from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, jsonify
from .models import User, Section, Book
from . import db
from datetime import datetime
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

# #Get book
@main.route('/books', methods=['GET'])
def get_section():
    response = {"sections": []}
    sections = Section.query.all()
    for section in sections:
        this_section = {"items": [], "id": section.id, "name": section.name}
        items = Book.query.filter(Book.section_id == section.id)
        for item in items:
            this_item = {"id": item.id, "ebook_price": item.ebook_price, "name": item.name, "authors": item.authors, "content": item.content}
            this_section["items"].append(this_item)
        response["sections"].append(this_section)
    return make_response(jsonify(response), 200)

#request book
#return book
#feedback book
#issue book
#revoke access
#book to user mapping
#search
#monthly activity report
#daily reminder