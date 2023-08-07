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


class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],  choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
    remarks = TextAreaField('Remarks', [validators.Optional()])


class CreateCourseForm(Form):
    course_name = StringField('Course Name', [validators.length(min=1, max=100), validators.DataRequired()])
    course_type = SelectField('Course Type', [validators.DataRequired()], choices=[('Information Technology', 'Information Technology'), ('Life Skills', 'Life Skills'), ('Problem Solving', 'Problem Solving')])
    course_rating = RadioField('Rating', [validators.data_required()], choices=[('1', '1-Star'), ('2', '2-Star'), ('3', '3-Star'), ('4', '4-Star'), ('5', '5-Star')])
    course_date = DateTimeField('Available Date', [validators.data_required()], format='%Y-%m-%d')  # planning to change to start and end date
    course_price = IntegerField('Price ($)', [validators.DataRequired(message='Please Enter a Price'), validators.NumberRange(min=1, max=None)])
    course_capacity = IntegerField('Course Capacity', [validators.DataRequired(), validators.NumberRange(min=1, max=None)])
    course_image = FileField('Upload Img')  # cannot put DataRequired
    course_company = StringField('Enter Company Name', [validators.length(min=1, max=100), validators.DataRequired()])
    course_language = SelectField('Languages Available', [validators.DataRequired()], choices=[('English', 'English'), ('Chinese', 'Chinese'), ('Malay', 'Malay'), ('Tamil', 'Tamil')], default='English')
    course_people_in_charge = StringField("Enter People In Charge", [validators.DataRequired()])
    course_commitment = SelectField("Course Commitment", [validators.DataRequired()], choices=[('', 'Select'), ('Full-Time', 'Full-Time'), ('Part-Time', 'Part-time'), ('Short-Term', 'Short-Term')], default='f')
    course_overview = TextAreaField("Course Overview", [validators.length(min=10), validators.DataRequired()])
    course_objective = TextAreaField("Course Objectives", [validators.DataRequired()])
    course_content = TextAreaField("Course Content", [validators.length(min=1, max=100), validators.DataRequired()])
    course_requirement = TextAreaField("Course Requirements", [validators.DataRequired()])
    submit = SubmitField("Upload File")


class UpdateCourseForm(Form):
    course_bookings = IntegerField('Course Bookings: ', [validators.DataRequired(), validators.NumberRange(min=0, max=None)])
    course_name = StringField('Course Name', [validators.length(min=1, max=100), validators.DataRequired()])
    course_type = SelectField('Course Type', [validators.DataRequired()], choices=[('Information Technology', 'Information Technology'), ('Life Skills', 'Life Skills'), ('Problem Solving', 'Problem Solving')])
    course_rating = RadioField('Rating', [validators.data_required()], choices=[('1', '1-Star'), ('2', '2-Star'), ('3', '3-Star'), ('4', '4-Star'), ('5', '5-Star')])
    course_date = DateTimeField('Available Date', [validators.data_required()], format='%Y-%m-%d')  # planning to change to start and end date
    course_price = IntegerField('Price ($)', [validators.DataRequired(message='Please Enter a Price'), validators.NumberRange(min=1, max=None)])
    course_capacity = IntegerField('Course Capacity', [validators.DataRequired(), validators.NumberRange(min=1, max=None)])
    course_image = FileField('Upload Img')
    course_company = StringField('Enter Company Name', [validators.length(min=1, max=100), validators.DataRequired()])
    course_language = SelectField('Languages Available', [validators.DataRequired()], choices=[('English', 'English'), ('Chinese', 'Chinese'), ('Malay', 'Malay'), ('Tamil', 'Tamil')], default='English')
    course_people_in_charge = StringField("Enter People In Charge", [validators.DataRequired()])
    course_commitment = SelectField("Course Commitment", [validators.DataRequired()], choices=[('', 'Select'), ('Full-Time', 'Full-Time'), ('Part-Time', 'Part-time'), ('Short-Term', 'Short-Term')], default='f')
    course_overview = TextAreaField("Course Overview", [validators.length(min=10), validators.DataRequired()])
    course_objective = TextAreaField("Course Objectives", [validators.DataRequired()])
    course_content = TextAreaField("Course Content", [validators.length(min=1, max=100), validators.DataRequired()])
    course_requirement = TextAreaField("Course Requirements", [validators.DataRequired()])
    submit = SubmitField("Upload File")


