from app import db 
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash  
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return f"<User: {self.id} | {self.email}>"

    def from_dict(self, data):
        self.first = data['first_name']
        self.last = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password']) # hashes the password 
        self.save() # saves the user info

        
    def hash_password(self, original_password):
        return generate_password_hash(original_password) # used to hash the login password

    def check_hashed_password(self, login_password): # used to check the hashed password against the login password
        return check_password_hash(self.password,login_password)

    def save(self):
        db.session.add(self) # adds the user to the db session
        db.session.commit() # saves all changes to the db 


@login.user_loader
def load_user(id):
    return User.query.get(int(id)) # Select * from user Where id=id and make sure its an int