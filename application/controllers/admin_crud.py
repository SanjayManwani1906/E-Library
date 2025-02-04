import datetime
from flask import render_template, request, redirect, flash, url_for, session, jsonify
from main import db, app, Tz, token_required, Users, Books, Sections, MyBooks, Feedback
from flask_cors import CORS


CORS(app)

@app.route('/createsection', methods=["POST"])
@token_required
def createsection(uid,authorisation):
    if authorisation == "admin":
        sname = request.json["sectionname"]
        des = request.json["description"]

        section = Sections(Name=sname , Description=des , AdminId=uid)

        db.session.add(section)
        db.session.commit()

        response = {
            "Alert":"Section created"
        }

        return jsonify(response)
    else:
        return jsonify({"alert":"not authorised"})
    

@app.route('/getsection/<int:sid>', methods=["GET"])
@token_required
def getsection(uid,authorisation,sid):
    if authorisation == "admin":
        section = Sections.query.filter_by(Id=sid).first()

        return jsonify({"section":section})
    else:
        return jsonify({"alert":"not authorised"})    

    

@app.route('/updatesection/<sid>', methods=["POST"])
@token_required
def updatesection(uid,authorisation,sid):
    
    if authorisation == "admin":
        sname = request.json['Name']
        des = request.json['Description']
        print(sname,des)
        section = Sections.query.filter_by(Id=int(sid)).first()

        section.Name = sname
        section.Description = des

        db.session.add(section)
        db.session.commit()

        response = {
            "Alert":"Section updated",
        }

        return jsonify(response)
    else:
        return jsonify({"alert":"not authorised"}) 


@app.route('/deletesection/<int:sid>', methods=["GET"])
@token_required
def deletesection(uid,authorisation,sid):
    if authorisation == "admin":

        books = Books.query.filter_by(SectionId = sid).all()

        for i in books:
            db.session.delete(i)
            db.session.commit()

        section = Sections.query.filter_by(Id=sid).first()

        db.session.delete(section)
        db.session.commit()

        response = {
            "Alert":"Section deleted & all the books in this section are also deleted",
        }

        return jsonify(response)
    else:
        return jsonify({"alert":"not authorised"}) 
    

@app.route('/createbook/<int:sid>', methods=["POST"])
@token_required
def createbook(uid,authorisation,sid):
    if authorisation == "admin":

        section = Sections.query.filter_by(Id=sid).first()

        bname = request.json["bookname"]
        sname = section.Name
        author = request.json["author"]
        content = request.json["content"]
        price = request.json["price"]
        date = str(datetime.datetime.now(Tz)).split(" ")[0]

        book = Books(Name = bname,
                     SectionId = sid,
                     SectionName = sname,
                     Author = author, 
                     Content = content, 
                     Price = price, 
                     DateIssued = date)

        db.session.add(book)
        db.session.commit()

        response = {
            "Alert":"Book created"
        }

        return jsonify(response)
    else:
        return jsonify({"Alert":"not authorised"})


@app.route('/getbook/<int:bid>', methods=["GET"])
@token_required
def getbook(uid,authorisation,bid):
    if authorisation == "admin":
        book = Books.query.filter_by(Id=bid).first()

        return jsonify({"book" : book})
    else:
        return jsonify({"Alert":"not authorised"})  
    


@app.route('/updatebook/<int:bid>', methods=["POST"])
@token_required
def updatebook(uid,authorisation,bid):
    if authorisation == "admin":

        book = Books.query.filter_by(Id=bid).first()

        bname = request.json["bookname"]
        sid = book.SectionId
        sname = book.SectionName
        author = request.json["author"]
        content = request.json["content"]
        price = request.json["price"]
        date = book.DateIssued

        book.Name = bname
        book.SectionId = sid
        book.SectionName = sname
        book.Author = author
        book.Content = content
        book.Price = price
        book.DateIssued = date


        db.session.add(book)
        db.session.commit()

        response = {
            "Alert":"Book updated"
        } 

        return jsonify(response)
    else:
        return jsonify({"alert":"not authorised"}) 

@app.route('/deletebook/<int:bid>', methods=["GET"])
@token_required
def deletebook(uid,authorisation,bid):
    if authorisation == "admin":

        book = Books.query.filter_by(Id=bid).first()

        db.session.delete(book)
        db.session.commit()

        response = {
            "Alert":"Book deleted",
        }

        return jsonify(response)
    else:
        return jsonify({"Alert":"not authorised"})   


@app.route('/bookstatus/<int:bid>', methods=["GET"])
@token_required
def bookstatus(uid,authorisation,bid):
    if authorisation == "admin":

        book = Books.query.filter_by(Id=bid).first()
        mybook = MyBooks.query.filter_by(BookId=bid).all()
        feedback = Feedback.query.filter_by(BookId=bid).all()

        print(book)
        print(mybook)
        print(feedback)

        response = {
            "Alert":"This is the book status",
            "book":book,
            "mybook":mybook,
            "feedback":feedback
        }

        return jsonify(response)
    else:
        return jsonify({"Alert":"not authorised"})    


@app.route('/adminhome', methods=["GET"])
@token_required
def adminhome(uid,authorisation):
    if authorisation == "admin":
        if request.method == "GET":

            user = Users.query.filter_by(Id = uid).first()
            sections = Sections.query.all()

            sections_dict = {}

            for section in sections:
                book_list = Books.query.filter_by(SectionId=section.Id).all()
                sections_dict[section.Name] = book_list 

            return jsonify({
                "user":user,
                "sections":sections
            })
    else:
            return jsonify({"Alert":" user not authorised"})  

@app.route('/getbooks/<int:sid>', methods=["GET"])
@token_required
def getbooks(uid,authorisation,sid):
    if authorisation == "admin":
        books = Books.query.filter_by(SectionId=sid).all()

        return jsonify({
            "books":books
        })
    else:
        return jsonify({"Alert":"not authorised"})                      