from flask import session

from app import app, db , login_manager

@login_manager.user_loader
def load_user(id):
    try:
        return User.query.get(User.query.filter_by(id=session['_user_id']).first().id)
    except:
        return None


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.is_authenticated

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.admin

    def get_id(self):
        return self.id

    def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()