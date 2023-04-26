""""Provides Form definitions for all forms."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class LoginForm(FlaskForm):

    """Form fields for logging in a user.

    Keyword Arguments:
    -----------------
        FlaskForm (FlaskForm): Form from flask_wtf
    """

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):

    """Form fields for registering a new user.

    Keyword Arguments:
    -----------------
        FlaskForm (FlaskForm): Form from flask_wtf
    """

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password",
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Register")

    def validate_username(self: "RegistrationForm", username: StringField) -> None:
        """Validate username by checking for duplicates in the database.

        Keyword Arguments:
        -----------------
            username (StringField): username to check for duplicates

        Raises:
        ------
            ValidationError: The username is already in use
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            err_msg = "Please use a different username."
            raise ValidationError(err_msg)

    def validate_email(self: "RegistrationForm", email: StringField) -> None:
        """Validate email by checking for duplicates in the database.

        Keyword Arguments:
        -----------------
        email (StringField): email to check for duplicates

        Raises:
        ------
        ValidationError: The email is already in use
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            err_msg = "Please use a different email address."
            raise ValidationError(err_msg)


class EditProfileForm(FlaskForm):

    """Form fields for editing a user profile.

    Keyword Arguments:
    -----------------
        FlaskForm (FlaskForm): Form from flask_wtf
    """

    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About Me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")
