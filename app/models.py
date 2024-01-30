from .extension import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True)
    is_completed = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'is_completed': self.is_completed
        }

    def __repr__(self):
        return f"<Task ID: {self.id}, Task Title: {self.title}, Completed: {self.is_completed}>"
