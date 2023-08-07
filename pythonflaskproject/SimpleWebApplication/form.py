from wtforms import Form, StringField, validators, RadioField, SubmitField, TextAreaField
from flask import url_for

class Feedbackform(Form):
    rating = RadioField('rating', [validators.optional()], choices=['verybad.png', 'bad.png', 'normal.png', 'good.png', 'verygood.png'])
    name = StringField('Name:', [validators.Length(min=1, max=150), validators.DataRequired(), validators.Regexp(r'^[^0-9]*$', message="Name cannot contain numbers")])
    email = StringField('Email:', [validators.Length(min=1, max=150), validators.DataRequired(), validators.Email(message="Invalid email format"), validators.Regexp(r'^.*@gmail\.com$', message="Email must end with @gmail.com")])
    subject = StringField('Subject:', [validators.Length(min=1, max=100), validators.DataRequired()])
    details = StringField('Details:', [validators.Length(min=1, max=300), validators.DataRequired()])
    submit = SubmitField('Submit')

class Reply(Form):
    reply = TextAreaField('', [validators.DataRequired()])
    submit = SubmitField()

