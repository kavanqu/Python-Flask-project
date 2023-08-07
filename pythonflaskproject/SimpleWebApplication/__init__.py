from flask import Flask, render_template, request, redirect, url_for, session
from form import Feedbackform, Reply, CreateUserForm, CreateCourseForm, UpdateCourseForm
import shelve
import feedback as f
# from feedback import msg



# upload file stuff
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'any_random_string'

# img file stuff
app.config['SECRET_KEY'] = "Testing"  # idk whats this for
app.config['UPLOAD_FOLDER'] = 'static/files'  # setting the file path for file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 *1024 * 1024  # setting limits to file size just in case


@app.route('/')
def home():
    # resetting shopping cart
    cart_db = shelve.open('shopping_cart.db', 'w')
    shopping_lst = []
    cart_db['Cart'] = shopping_lst
    return render_template('home.html')

@app.route('/Feedbackform', methods=['GET', 'POST'])
def create_user():
    feedback_form = Feedbackform(request.form)
    if request.method == 'POST' and feedback_form.validate():
        feedback_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            feedback_dict = db['feedback']
        except:
            print("Error in retrieving Users from storage.db.")

        feedback = f.feedback(feedback_form.rating.data, feedback_form.name.data, feedback_form.email.data, feedback_form.subject.data, feedback_form.details.data)
        feedback_dict[feedback.get_user_id()] = feedback
        db['feedback'] = feedback_dict

        # Test codes
        feedback_dict = db['feedback']
        feedback = feedback_dict[feedback.get_user_id()]
        print(feedback.get_name(), "was stored in storage.db successfully with user_id == ", feedback.get_user_id())
        db.close()

        session['feedback_form_created'] = feedback.get_name()
        return redirect(url_for('home'))

    return render_template('Feedbackform.html', user_list=feedback_form)



@app.route('/update_feedback/<int:id>/', methods=['GET', 'POST'])
def update_feedback(id):
    update_user_form = Feedbackform(request.form)
    feedback_dict = {}
    db = shelve.open('storage.db', 'r')
    feedback_dict = db['feedback']
    db.close()
    feedback_list = []
    for key in feedback_dict:
        feedback_item = feedback_dict.get(key)
        feedback_list.append(feedback_item)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['feedback']
        user = users_dict.get(id)
        user.set_rating(update_user_form.rating.data)
        user.set_name(update_user_form.name.data)
        user.set_email(update_user_form.email.data)
        user.set_subject(update_user_form.subject.data)
        user.set_detail(update_user_form.details.data)
        db['feedback'] = users_dict
        db.close()

        return redirect(url_for('retrieveUsers'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['feedback']
        db.close()
        user = users_dict.get(id)
        update_user_form.rating.data = user.get_rating()
        update_user_form.name.data = user.get_name()
        update_user_form.email.data = user.get_email()
        update_user_form.subject.data = user.get_subject()
        update_user_form.details.data = user.get_details()

    return render_template('update_feedback.html',user_list = feedback_list,form=update_user_form)



@app.route('/retrieveUsers')
def retrieveUsers():
    feedback_dict = {}
    db = shelve.open('storage.db', 'r')
    feedback_dict = db['feedback']
    db.close()
    feedback_list = []
    for key in feedback_dict:
        feedback_item = feedback_dict.get(key)
        feedback_list.append(feedback_item)

    return render_template('retrieveData.html', count=len(feedback_list), users_list=feedback_list)


@app.route('/replyUser/<int:id>/', methods=['GET', 'POST'])
def replyUser(id):
    feedback_dict = {}
    db = shelve.open('storage.db', 'c')
    feedback_dict = db['feedback']

    feedback = feedback_dict.get(id)
    replies = Reply(request.form)

    if request.method == 'POST':
        action = request.form["txtAction"]

        if action == "dosave":
            # Process the reply and update the feedback's reply field
            feedback.reply = replies.reply.data  # Assuming you have a field named 'reply' in your Feedback class
            db['feedback'] = feedback_dict
            db.close()
            return redirect(url_for('retrieveUsers'))

        elif action == "dodelete":
            if id in feedback_dict:
                del feedback_dict[id]
                db['feedback'] = feedback_dict
                db.close()
                return redirect(url_for('retrieveUsers'))

    db.close()
    return render_template('replyUser.html', user_list=[feedback], id=id, reply=replies)


@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    feedback_dict = {}
    db = shelve.open('storage.db', 'c')
    feedback_dict = db['feedback']

    if id in feedback_dict:
        del feedback_dict[id]
        db['feedback'] = feedback_dict
        db.close()

    return redirect(url_for('retrieveUsers'))

def delete_user(id):
    feedback_dict = {}
    db = shelve.open('storage.db', 'w')
    try:
        feedback_dict = db['feedback']
    except KeyError:
        pass  # Handle the case where 'feedback' key doesn't exist

    if id in feedback_dict:
        feedback_dict.pop(id)
        db['feedback'] = feedback_dict
    db.close()

    return redirect(url_for('retrieveUsers'))


# COURSE SECTION

@app.route('/createCourse', methods=["GET", 'POST'])
def create_course():
    create_course_form = CreateCourseForm(request.form)  # course form
    # print(create_course_form.validate())
    if request.method == 'POST' and create_course_form.validate():
        # print("2")
        course_dict = {}
        course_db = shelve.open('course_storage.db', 'c')
        # print(create_course_form.course_image.data)

        try:
            course_dict = course_db['Courses']  # getting the courses
        except:
            print("Error in retrieving Courses from course_storage.db.")

        # the stuff below is from the form data
        img_file = request.files['course_image']
        print("image file: ",img_file)
        if img_file != None and str(img_file) != "<FileStorage: '' ('application/octet-stream')>":  # Check if a file was actually uploaded
            print("img uploaded")
            filename = secure_filename(img_file.filename)
            save_path = os.path.join(app.static_folder, "files", filename)  # creating the absolute path to static/files
            img_file.save(save_path) # saving the files
            # print(save_path[:43])
            save_path = save_path[43:]  # removing the front part so only the file name remains
            print(save_path)
        else:
            save_path = "Course.jpeg"


        rating = create_course_form.course_rating.data
        rating = int(rating)  # changing rating to an integer

        # managing course ids
        courses_lst = []
        for key in course_dict:
            course = course_dict.get(key)
            course_id = course.get_course_id()
            courses_lst.append(course_id)
        print("course list:",courses_lst)

        if len(courses_lst) == 0:
            print("no courses")
            course_id = 1
        else:
            highest_id = max(courses_lst)
            print("highest id:", highest_id)
            for i in range(1, highest_id+1):
                if i not in courses_lst:
                    print("havent found yet")
                    course_id = i
                    break
                else:
                    print("stopped")
                    course_id = i +1

        print(course_id)



        course = Course.Course(course_id, create_course_form.course_name.data, create_course_form.course_type.data,
                               rating, create_course_form.course_date.data, create_course_form.course_price.data,
                               save_path, create_course_form.course_company.data, create_course_form.course_language.data,
                               create_course_form.course_people_in_charge.data, create_course_form.course_commitment.data,
                               create_course_form.course_overview.data, create_course_form.course_objective.data,
                               create_course_form.course_content.data, create_course_form.course_requirement.data,
                               create_course_form.course_capacity.data)

        course_dict[course_id] = course  # course_id is from the course class
        course_db['Courses'] = course_dict  # i think this is adding it to the dictionary

        course_db.close()
        return redirect(url_for('courses'))
    # print("1")
    return render_template('createCourse.html', form=create_course_form, update_check=False)


# courses page
@app.route('/courses')
def courses():
    course_dict = {}
    course_db = shelve.open('course_storage.db', 'r')
    # print("test1")
    course_dict = course_db['Courses']
    # print("test")
    course_db.close()

    courses_lst = []
    for key in course_dict:
        course = course_dict.get(key)
        courses_lst.append(course)
    return render_template("courses.html", iteration=0, count=len(courses_lst), courses_lst=courses_lst) # count=len(courses_lst), courses_lst=courses_lst


# displaying courses
@app.route("/courseDisplay/<int:course_id>")
def courseDisplay(course_id):
    course_dict = {}
    course_db = shelve.open('course_storage.db', 'r')
    course_dict = course_db['Courses']
    specific_course = course_dict.get(course_id)  # getting the correct course
    course_db.close()

    return render_template('courseDisplay.html', course=specific_course)



@app.route('/deleteCourse/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    course_db = shelve.open('course_storage.db', 'w')
    course_dict = course_db['Courses']
    course_dict.pop(course_id)
    course_db['Courses'] = course_dict
    course_db.close()
    return redirect(url_for('retrieve_data'))



@app.route('/updateCourse/<int:course_id>/', methods=['GET', 'POST'])
def updateCourse(course_id):
    update_course_form = UpdateCourseForm(request.form)
    print(request.method, update_course_form.validate())
    if request.method == 'POST' and update_course_form.validate():
        course_dict = {}
        course_db = shelve.open("course_storage.db", 'w')
        course_dict = course_db['Courses']
        specific_course = course_dict.get(course_id)
        print("updating form")

        img_file = request.files['course_image']
        print(img_file)
        if str(img_file) != "<FileStorage: '' ('application/octet-stream')>":  # Check if a file was actually uploaded
            # print("uploading img")
            filename = secure_filename(img_file.filename)
            # print('filename: ',filename)
            save_path = os.path.join(app.static_folder, "files", filename)  # creating the absolute path to static/files
            # print("removing \\")
            save_path = save_path.replace('\\', '/')
            # print('save path:', save_path)
            img_file.save(save_path)  # saving the files
            # print(save_path[:43])
            save_path = save_path[43:]  # removing the front part so only the file name remains
            specific_course.set_course_image(save_path)

        # updating the class values
        specific_course.set_course_name(update_course_form.course_name.data)
        specific_course.set_course_bookings(update_course_form.course_bookings.data)
        specific_course.set_course_type(update_course_form.course_type.data)
        specific_course.set_course_rating(int(update_course_form.course_rating.data))
        specific_course.set_course_date(update_course_form.course_date.data)
        specific_course.set_course_price(update_course_form.course_price.data)

        # specific_course.set_course_image(update_course_form.course_image.data)
        specific_course.set_course_company(update_course_form.course_company.data)
        specific_course.set_course_language(update_course_form.course_language.data)
        specific_course.set_course_people_in_charge(update_course_form.course_people_in_charge.data)
        specific_course.set_course_commitment(update_course_form.course_commitment.data)
        specific_course.set_course_overview(update_course_form.course_overview.data)
        specific_course.set_course_objective(update_course_form.course_objective.data)
        specific_course.set_course_content(update_course_form.course_content.data)
        specific_course.set_course_requirements(update_course_form.course_requirement.data)
        specific_course.set_course_capacity(update_course_form.course_capacity.data)

        course_db['Courses'] = course_dict
        course_db.close()
        return redirect(url_for('courses'))
    else:
        course_dict = {}
        print("creating form")
        course_db = shelve.open("course_storage.db", 'r')
        course_dict = course_db['Courses']
        specific_course = course_dict.get(course_id)
        course_db.close()

        update_course_form.course_name.data = specific_course.get_course_name()
        update_course_form.course_bookings.data = specific_course.get_course_bookings()
        update_course_form.course_type.data = specific_course.get_course_type()
        update_course_form.course_date.data = specific_course.get_course_date()
        update_course_form.course_price.data = specific_course.get_course_price()
        update_course_form.course_rating.data = str(specific_course.get_course_rating())  # need put in string cause of the form stuff
        # update_course_form.course_image.data = specific_course.get_course_image()
        update_course_form.course_company.data = specific_course.get_course_company()
        update_course_form.course_language.data = specific_course.get_course_language()
        update_course_form.course_people_in_charge.data = specific_course.get_course_people_in_charge()
        update_course_form.course_commitment.data = specific_course.get_course_commitment()
        update_course_form.course_overview.data = specific_course.get_course_overview()
        update_course_form.course_objective.data = specific_course.get_course_objective()
        update_course_form.course_content.data = specific_course.get_course_content()
        update_course_form.course_requirement.data = specific_course.get_course_requirements()
        update_course_form.course_capacity.data = specific_course.get_course_capacity()

        return render_template('updateCourse.html', form=update_course_form, course=specific_course)


# shopping cart
@app.route("/add_cart/<int:course_id>")
def add_cart(course_id):
    # course_dict = {}
    # course_db = shelve.open('course_storage.db', 'r')
    # course_dict = course_db['Courses']
    # specific_course = course_dict.get(course_id)  # getting the correct course
    # course_db.close()

    cart_db = shelve.open('shopping_cart.db', 'c')
    if 'Cart' not in cart_db:
        cart_db['Cart'] = []
    shopping_lst = cart_db['Cart']
    shopping_lst.append(course_id)
    cart_db['Cart'] = shopping_lst
    cart_db.close()

    print(shopping_lst)

    return redirect(url_for('courses'))


@app.route("/shoppingCart")
def shopping_cart():
    cart_db = shelve.open('shopping_cart.db', 'r')
    shopping_lst = cart_db['Cart']
    cart_db.close()

    courses_db = shelve.open('course_storage.db', 'r')
    course_dict = courses_db['Courses']
    courses_db.close()

    selected_lst = []
    for i in shopping_lst:
        selected_lst.append(course_dict.get(i))

    return render_template('shoppingCart.html', shopping_lst=selected_lst)


@app.route("/paymentMethods/<int:course_id>")
def paymentMethods(course_id):
    course_dict = {}
    course_db = shelve.open('course_storage.db', 'w')  # putting w to make changes
    course_dict = course_db['Courses']
    specific_course = course_dict.get(course_id)  # getting the correct course
    specific_course.increase_bookings()  # increasing the bookings
    course_db['Courses'] = course_dict  # saving changes
    course_db.close()
    return redirect(url_for('courseDisplay', course_id=course_id))


@app.route('/retrieveData')
def retrieve_data():
    # retrieving the user database
    users_dict = {}
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()

    # extracting the user objects
    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    # retrieving course database
    course_dict = {}
    course_db = shelve.open('course_storage.db', 'r')
    course_dict = course_db['Courses']
    db.close()

    # extracting course objects
    course_list = []
    for course_key in course_dict:
        course = course_dict.get(course_key)
        course_list.append(course)

    # ranking the courses
    # number_of_courses = len(course_list)
    # higher_rank = course_list[0].get_course_bookings()
    # iteration = 1

    for i in range(1,len(course_list)):
        print(course_list[i - 1].get_course_name())
        if course_list[i - 1].get_course_bookings() < course_list[i].get_course_bookings():
            store = course_list[i-1]
            course_list[i -1] = course_list[i]
            course_list[i] = store



    return render_template('retrieveData.html', user_count=len(users_list), users_list=users_list, course_count=len(course_list), course_list=(course_list))
    # The users_list list will be used in the Retrieve Users template to retrieve and display the
    # details of all the user objects that were stored in the users_dict dictionary that was stored in
    # shelve.
# Database stuff


@app.route('/contactpage')
def contactpage():
    return render_template('contactpage.html')

if __name__ == '__main__':
    app.run()


