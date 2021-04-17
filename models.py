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
