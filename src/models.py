from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is active": self.is_active
            # do not serialize the password, its a security breach
        }
    
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Tell python how to print the class object on the console
    def __repr__(self):
        return '<Person %r>' % self.username

    # Tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return { "id": self.id,
            "username": self.username,
                "email": self.email}
    
class Characters(db.Model):
     __tablename__ = 'characters'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(250), unique=True, nullable = False)
     url = db.Column(db.String(600), unique=True, nullable = False)

     def __repr__(self):
        return '<Characters %r>' % self.name
     
     def serialize(self):
        return { "id": self.id,
            "username": self.name,
                "email": self.url}

class Planets(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable = False)
    url = db.Column(db.String(600), unique=True, nullable = False)

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return { "id": self.id,
            "username": self.name,
                "email": self.url}