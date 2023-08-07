import shelve
from wtforms import (
    Form, StringField, EmailField, PasswordField,
    DateField, IntegerField, SelectField, validators,
    ValidationError
)


class UpdateUserForm(Form):
    name = StringField('Name')
    password = PasswordField('Password', [validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired()])
    birth_date = DateField('Birth Date', [validators.DataRequired()])


class LoginForm(Form):
    email = EmailField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


class RegisterForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    email = EmailField('Email', [validators.DataRequired()])
    birth_date = DateField('Birth Date', [validators.DataRequired()])


def validate_email(form, field):
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    user_emails = [user.get_email() for user in users_dict.values()]

    if field.data not in user_emails:
        raise ValidationError('User account with email does not exist.')


class PasswordResetForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validate_email])


class CheckoutForm(Form):
    card_number = IntegerField(validators=[validators.DataRequired()])
    cvv = IntegerField("CVV", validators=[validators.DataRequired()])
    expire_month = IntegerField("Expiration Date", validators=[validators.DataRequired(),
                                                               validators.NumberRange(min=1, max=12)])
    expire_year = IntegerField("", validators=[validators.DataRequired(),
                                               validators.NumberRange(min=20, max=30)])
    name = StringField("Name on Card", validators=[validators.DataRequired()])
    address_1 = StringField("Address Line 1", validators=[validators.DataRequired()])
    address_2 = StringField("Address Line 2", validators=[validators.Optional()])
    country = SelectField('Country', choices=[('SG', 'Singapore'), ('US', 'United States'), ('UK', 'United Kingdom')],
                          validators=[validators.DataRequired()])
    city = StringField(validators=[validators.DataRequired()])
    zip_code = IntegerField(validators=[validators.DataRequired()])
