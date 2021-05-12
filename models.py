from database import db

class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    password = db.Column("password", db.String(100))
    fName = db.Column("fName", db.String(20))
    lName = db.Column("lName", db.String(30))
    email = db.Column("email", db.String(50))

    def __init__(self, email, fName, lName, password):
        self.password = password
        self.fName = fName
        self.lName = lName
        self.email = email

class Event(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, foreign_key=True)
    event_name = db.Column("event_name", db.String(100))
    start_date = db.Column("start_date", db.String(100))
    end_date = db.Column("end_date", db.String(100))
    event_details = db.Column("event_details", db.String(100))
    public = db.Column("public", db.Boolean)

    def __init__(self, user_id, event_name, event_details, start_date, end_date, public):
        self.user_id = user_id
        self.event_name = event_name
        self.start_date = start_date
        self.end_date = end_date
        self.event_details = event_details
        self.public = public

class RSVP(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer)
    user_name = db.Column("user_name", db.String(51))
    event_id = db.Column("event_id", db.Integer)
    date_registered = db.Column("date_registered", db.String(100))
    status = db.Column("status", db.Boolean, default=False, nullable=False)

    def __init__(self, user_id, user_name, event_id, date_registered, status):
        self.event_id = event_id
        self.user_id = user_id
        self.user_name = user_name
        self.date_registered = date_registered
        self.status = status

class Rating(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_name = db.Column("user_name", db.String(51))
    user_id = db.Column("user_id", db.Integer)
    event_id = db.Column("event_id", db.Integer)
    rating_no = db.Column("rating", db.Integer)

    def __init__(self, user_name, user_id, event_id, rating_no):
        self.user_name = user_name
        self.user_id = user_id
        self.event_id = event_id
        self.rating_no = rating_no

class Invite(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_email = db.Column("user_email", db.String(50))
    user_id = db.Column("user_id", db.Integer())
    event_id = db.Column("event_id", db.Integer())

    def __init__(self, user_email, user_id, event_id):
        self.user_id = user_id
        self.user_email = user_email
        self.event_id = event_id


class Friend(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    user_id = db.Column("user_id", db.Integer)
    friend_id = db.Column("friend_id", db.Integer)

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id


