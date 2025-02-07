from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from app import app

db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  #creates a relationship field to get the user's todos
  todos = db.relationship('Todo', backref='user', lazy=True, cascade="all, delete-orphan")

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.set_password(password)

  def set_password(self, password):
      """Create hashed password."""
      self.password = generate_password_hash(password, method='sha256')

  def __repr__(self):
      return f'<User {self.id} {self.username} - {self.email}>'

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  text = db.Column(db.String(255), nullable=False)
  done = db.Column(db.Boolean, default=False)

  def toggle(self):
    self.done = not self.done
    db.session.add(self)
    db.session.commit()

  def __init__(self, text):
      self.text = text

  def __repr__(self):
    return f'<Todo: {self.id} | {self.user.username} | {self.text} | { "done" if self.done else "not done" }>'

