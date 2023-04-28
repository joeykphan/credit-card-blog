"""Provide model definitions to outline how data is formatted in the database."""
from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):

    """User model with Flask-Login UserMixin.

    Keyword Arguments:
    -----------------
        UserMixin (class): Mixin that provides default implementations for
                            methods that Flask-Login expects for a user object.
        db (class): SQLAlchemy object that handles all database engines, model
                    and table associations, connections, and sessions.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self: "User") -> str:
        """Print user's username.

        Returns:
        -------
            str: User's username.
        """
        return f"<User {self.username}>"

    def set_password(self: "User", password: str) -> None:
        """Store user password hash in databse.

        Keyword Arguments:
            self (User): User object instance.
            password (str): Raw user password chosen by user.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self: "User", password: str) -> bool:
        """Authenticate user password by comparing hashes.

        Keyword Arguments:
        -----------------
            self (User): User object instance.
            password (str): Raw user password typed by user.

        Returns:
        -------
            bool: Whether the typed password matches the chosen password.
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self: "User", size: int) -> str:
        """Generate unique avatar for user profile using Gravatar API.

        Keyword Arguments:
        -----------------
            self (User): User object instance.
            size (int): Size of the avater to be displayed.

        Returns:
        -------
            str: API call to gravatar service.
        """
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


class Post(db.Model):

    """Blog post model.

    Keyword Arguments:
    -----------------
        db (class): SQLAlchemy object that handles all database engines, model
                    and table associations, connections, and sessions.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self: "Post") -> str:
        """Print body of blog post.

        Returns:
        -------
            str: Body of blog post.
        """
        return f"<Post {self.body}>"


#  Loader Functions
@login.user_loader
def load_user(id: int) -> "User":
    """Load User data from database.

    Keyword Arguments:
    -----------------
        id (int): Unique User id

    Returns:
    -------
        User: User object instance pulled from database.
    """
    return User.query.get(int(id))
