import shelve
import datetime
import CourseCategories
import Courses
import User


def create_account(first_name,
                   last_name,
                   password,
                   email,
                   birth_date,
                   admin=False):
    users_dict = {}

    db = shelve.open('storage.db', 'c')
    try:
        users_dict = db['Users']
    except KeyError:
        print("Error in retrieving Users from storage.db.")

    user = User.User(
        first_name, last_name, password, email, birth_date, admin
    )
    users_dict[user.get_user_id()] = user
    db['Users'] = users_dict
    db.close()


def create_course_category(course_title):
    categories_dict = {}

    db = shelve.open('storage.db', 'c')
    try:
        categories_dict = db['Categories']
    except KeyError:
        print("Error in retrieving Categories from storage.db.")

    category = CourseCategories.CourseCategory(course_title)
    categories_dict[category.get_title()] = category
    db['Categories'] = categories_dict
    db.close()


def create_course(course_title, start_time, start_date, course_categories):
    courses_dict = {}

    db = shelve.open('storage.db', 'c')
    try:
        courses_dict = db['Courses']
    except KeyError:
        print("Error in retrieving Courses from storage.db.")

    course = Courses.Course(
        course_title, start_time, start_date
    )

    for category in course_categories:
        CourseCategories.CourseCategory.add_course(db, category, course)
    courses_dict[course.get_course_id()] = course
    db['Courses'] = courses_dict
    db.close()


def set_up_db():
    # Insert placeholder data

    # Create user accounts
    create_account('Amy', 'Ang', 'qwe', 'amyang@test.com', datetime.date.today(), admin=True)
    create_account('Benny', 'Bong', 'qwe', 'bennyb@test.com', datetime.date.today(),)
    create_account('Catherine', 'Cheng', 'qwe', 'catherinec@test.com', datetime.date.today(),)

    # Create course categories
    categories = ['Business', 'Data Analytics', 'Engineering', 'Computer Science']
    for title in categories:
        create_course_category(title)

    # Create courses
    create_course('Accounting and Management', 1830, 7/7/2023, ['Business', 'Data Analytics'])
    create_course('Hotel & Leisure Facilities Management', 1830, 7/7/2023, ['Business'])
    create_course('Finance Management', 1830, 7/7/2023, ['Business'])
    create_course('Predictive Modelling', 1830, 7/7/2023, ['Data Analytics'])
    create_course('Building and Construction', 1830, 7/7/2023, ['Engineering'])
    create_course('Cybersecurity', 1830, 7/7/2023, ['Computer Science'])
    create_course('Applied AI', 1830, 7/7/2023, ['Computer Science'])
