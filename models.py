from database import db

class user(db.Model):
    id = db.column("id", db.Integer, primary_key=True)
    password = db.column("password", db.String(100))
    fName = db.column("fName", db.String(20))
    lName = db.column("lName", db.String(30))

    def __init__(self, password, fName, lName):
        self.password = password
        self.fName - fName
        self.lName = lName

class event(db.Model):
    id = db.column("id", db.Integer, primary_key=True)
    event_name = db.column("event_name", db.String(100))
    start_date = db.column("start_date", db.String(100))
    end_date = db.column("end_date", db.String(100))
    event_details = db.column("event_details", db.String(100))

    def __init__(self, event_name, start_date, end_date, event_details):
        self.event_name = event_name
        self.start_date = start_date
        self.end_date = end_date
        self.event_details = event_details

class RSVP(db.Model):
    id = db.column("id", db.Integer, primary_key=True)
    event_id = db.column("event_id", db.Integer)
    date_registered =  db.column("date_registered", db.String(100))
    status = db.column("status", db.Boolean, default=False, nullable=False)

    def __init__(self, event_id, date_registered, status):
        self.event_id = event_id
        self.date_registered = date_registered
        self.status = status

class rating(db.Model):
    id = db.column("id", db.Integer, primary_key=True)
    user_id = db.column("user_id", db.Integer)
    event_id = db.column("event_id", db.Integer)
    like_status = db.column("like_status", db.Boolean)

    def __init__(self, user_id, event_id, like_status):
        self.user_id = user_id
        self.event_id = event_id
        self.like_status = like_status