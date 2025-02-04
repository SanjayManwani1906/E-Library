import datetime, jwt
from datetime import datetime,timedelta
from time import sleep
from flask import render_template, request, redirect, flash, url_for, session, jsonify
from main import db, app, Tz, token_required, Users, Books, Sections, MyBooks, Feedback
from flask_cors import CORS

CORS(app)


@app.route('/createaccount', methods=["POST"])
def createaccount():
    
    uname = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    cpass = request.form["cpassword"]


    user = Users.query.filter_by(Name=uname).all()

    if len(user) > 0:
        return jsonify({"Alert": "Username already taken"})

    if password == cpass and len(uname.split(" ")) == 1:

        user = Users(Name=uname,
                     Password=password, 
                     Email=email,
                     Authorisation="user", 
                     LastLogin = str(datetime.now(Tz).date()))
        db.session.add(user)
        db.session.commit()

        token = jwt.encode({"uid": user.Id},
                           app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({"token": token})
    else:
        return jsonify({"Alert": "Passwords do not match/Username cannot have spaces"})
    



@app.route('/', methods=["POST"])
def login():

    uname = request.json["username"]
    password = request.json["password"]

    userlist = Users.query.filter_by(Name=uname).all()
    user = Users.query.filter_by(Name=uname).first()

    if len(userlist) == 0:
        return jsonify({"Alert": "User not found"})

    if user.Password == password:
        authorisation = user.Authorisation
        uid = user.Id

        token = jwt.encode(
            {"uid": uid}, app.config['SECRET_KEY'], algorithm="HS256")
        
        user.LastLogin = str(datetime.now(Tz).date())

        db.session.add(user)
        db.session.commit()

        my_books = MyBooks.query.filter_by(UserId=uid).all()

        today = datetime.now(Tz).date()
        for book in my_books:
            revoke_date = datetime.strptime(book.RevokeDate, '%Y-%m-%d').date()
            if revoke_date < today :
                book.Revoked = True
                db.session.add(book)
                db.session.commit()            
        
        return jsonify({"token": token, "authorisation": authorisation})

    else:
        return jsonify({"Alert": "Incorrect Username or Password"})
    

@app.route('/updateaccount', methods=["GET", "POST"])
@token_required
def updateaccount(uid,authorisation):
    if authorisation == "user":
        user = Users.query.filter_by(Id=uid).first()
        
        if request.method == "GET":
            return jsonify({"user":user})
        
        if request.method == "POST":
            
            newname = request.form["newname"]
            newemail = request.form["newemail"] 
            
            existing_users = Users.query.filter_by(Name=newname).all()

            if len(existing_users) > 0: 
                if existing_users[0].Id != user.Id:
                    return jsonify({
                        "Alert":"Username already taken"
                        })
                    
            if len(newname.split(" ")) != 1:
                return jsonify({
                    "Alert":"Username cannot have spaces"
                    })
                
            if newname != user.Name:
                user.Name = newname
                user.Email = newemail
                db.session.add(user)
                db.session.commit()


            return jsonify({"Alert":"Account Updated"})
    else:
        return jsonify({"Alert":" user not authorised"}) 

@app.route('/userhome', methods=["GET"])
@token_required
def userhome(uid,authorisation):
    if authorisation == "user":
        if request.method == "GET":

            user = Users.query.filter_by(Id = uid).first()
            sections = Sections.query.all()

            sections_dict = {}

            for section in sections:
                book_list = Books.query.filter_by(SectionId=section.Id).all()
                sections_dict[section.Name] = book_list 

            return jsonify({
                "user":user,
                "sections":sections,
                "sections_dict":sections_dict
            })
    else:
            return jsonify({"alert":" user not authorised"})     


@app.route('/buybook/<int:bid>', methods=["GET"])
@token_required
def buybook(uid,authorisation,bid):
    if authorisation == "user":
        if request.method == "GET":

            mybooks = MyBooks.query.filter_by(UserId=uid).all()
            value = False
            
            if value == False:
                for i in mybooks:
                    if i.UserId == uid & i.BookId == bid :
                        value = True

            if value == True:
                return jsonify({"Alert":"You have already purchased the book. Kindly wait."})            


            if len(mybooks) >= 5 :
                return jsonify({"Alert":"Books limit reaches. You can rent a maximum of 5 books at once."})
            else:
                book_price = Books.query.filter_by(Id=bid).first().Price

                mybook =  MyBooks(UserId=uid,
                                BookId=bid,
                                DateIssued=str(datetime.now(Tz).date()) ,
                                RevokeDate= str(datetime.now(Tz).date()+timedelta(days=7)),
                                Revoked=False,
                                Total=book_price)
                
                db.session.add(mybook)
                db.session.commit()
                return jsonify({"Alert" : "Book purchased for 7 days" })
    else:
            return jsonify({"Alert":" user not authorised"})  
    

@app.route('/readbook/<int:bid>', methods=["GET"])
@token_required
def readbook(uid,authorisation,bid):
    if authorisation == "user":

        mybook = MyBooks.query.filter_by(UserId=uid,BookId=bid,Revoked=False).first()

        if mybook == None:
            return jsonify({"Alert":"Access revoked. Purchase again to read the book for 7 days."})
        else:
            book = Books.query.filter_by(Id=bid).first()
            return jsonify({"book" : book })
        
    else:
            return jsonify({"Alert":" user not authorised"}) 
    



@app.route('/feedback/<int:bid>', methods=["GET", "POST"])
@token_required
def feedback(uid,authorisation,bid):
    if authorisation == "user":
        user = Users.query.filter_by(Id=uid).first()
        book = Books.query.filter_by(Id=bid).first()
        
        if request.method == "GET":
            feedbacks = Feedback.query.filter_by(BookId=bid).all()

            return jsonify({"user":user,
                            "book" : book,
                            "feedbacks" : feedbacks})
        
        if request.method == "POST":
            
            feedback_comment = request.form["feedback"]

            mybook = MyBooks.query.filter_by(UserId=uid,BookId=bid).first()
            if mybook == None:
                verified = False
            else:
                verified = True    

                

            feedback = Feedback(BookId=bid,UserId=uid,Feedback=feedback_comment,Verified=verified)

            db.session.add(feedback)
            db.session.commit()

            return jsonify({"Alert":"Feedback given"})
    else:
        return jsonify({"alert":" user not authorised"})    


@app.route('/search/<string:level>/<string:section_id>/<string:keyword>', methods=["GET"])
@token_required
def search(uid,authorisation,level,section_id,keyword):
    if authorisation == "user":
        if level == 'sections':
            booklist = Sections.query.filter(Sections.Name.like("%"+keyword+"%")).all()
        if level == 'books':
            booklist = Books.query.filter(Books.SectionId == int(section_id)).filter(Books.Name.like("%"+keyword+"%") | Books.Author.like("%"+keyword+"%")).all()

        response = {
            "booklist":booklist
        }

        return jsonify(response)
    else:
        return jsonify({"alert":" user not authorised"})   


@app.route('/mybooks', methods=["GET"])
@token_required
def mybooks(uid,authorisation):
    if authorisation == "user":
        
        user = Users.query.filter_by(Id = uid).first()
        my_books = MyBooks.query.filter_by(UserId=uid,Revoked=False).all()

        booklist = Books.query.join(MyBooks, Books.Id == MyBooks.BookId).filter(MyBooks.UserId==uid,MyBooks.Revoked==False).all()


        return jsonify({
            "user":user,
            "mybooks":booklist
        })
    else:
            return jsonify({"alert":" user not authorised"})   


@app.route('/usergetbooks/<int:sid>', methods=["GET"])
@token_required
def usergetbooks(uid,authorisation,sid):
    if authorisation == "user":
        books = Books.query.filter_by(SectionId=sid).all()

        return jsonify({
            "books":books
        })
    else:
        return jsonify({"Alert":"not authorised"})   
    
       
