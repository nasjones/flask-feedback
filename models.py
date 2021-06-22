from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users table definition"""
    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True,
                         nullable=False)

    password = db.Column(db.String(), nullable=False)

    first_name = db.Column(db.String(20), nullable=False)

    last_name = db.Column(db.String(20), nullable=False)

    email = db.Column(db.String(50), nullable=False)

    feedback = db.relationship(
        'Feedback', backref='User', cascade="all,delete")

    def __repr__(self):
        return f'name="{self.first_name} {self.last_name}" username="{self.username}" email="{self.email}" password="{self.password}"'

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        hashed = bcrypt.generate_password_hash(password)

        return cls(username=username, password=hashed.decode('utf8'), first_name=first_name, last_name=last_name, email=email)

    @classmethod
    def authenticate(cls, username, password):
        user = User.query.get(username)

        if bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Feedback(db.Model):
    """Feedback table definition"""
    __tablename__ = "feedback"

    id = db.Column(db.Integer(), auto_increment=True,
                   primary_key=True, nullable=False)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text(), nullable=False)

    username = db.Column(db.String(), db.ForeignKey('users.username'))
