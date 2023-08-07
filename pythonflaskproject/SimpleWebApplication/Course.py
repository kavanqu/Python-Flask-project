class Course:

    # course_id = 0

    def __init__(self, course_id, course_name, course_type, course_rating, course_date, course_price, course_image, course_company,
                 course_language, people_in_charge, course_commitment, course_overview, course_objective, course_content,
                 course_requirements, course_capacity):

        # Course.course_id += 1

        # course key details
        self.__course_id = course_id
        self.__course_bookings = 0   # number of times booked
        self.__course_name = course_name
        self.__course_type = course_type
        self.__course_rating = course_rating
        self.__course_date = course_date
        self.__course_price = course_price
        self.__course_image = course_image
        self.__course_capacity = course_capacity

        # other details
        self.__course_company = course_company
        self.__course_language = course_language
        self.__course_people_in_charge = people_in_charge
        self.__course_commitment = course_commitment

        # heavy content
        self.__course_overview = course_overview
        self.__course_objective = course_objective
        self.__course_content = course_content
        self.__course_requirements = course_requirements

    # setter methods
    def set_course_id(self, course_id):
        self.__course_id = course_id

    def set_course_bookings(self, course_bookings):
        self.__course_bookings = course_bookings

    def set_course_name(self, course_name):
        self.__course_name = course_name

    def set_course_type(self, course_type):
        self.__course_type = course_type

    def set_course_rating(self, course_rating):
        self.__course_rating = course_rating

    def set_course_date(self, course_date):
        self.__date = course_date

    def set_course_price(self,course_price):
        self.__course_price = course_price

    def set_course_image(self, course_image):
        self.__course_image = course_image # trying to see if i can put a img link here and then put it in the html part

    def set_course_company(self, course_company):
        self.__course_company = course_company

    def set_course_language(self, course_language):
        self.__course_language = course_language

    def set_course_people_in_charge(self, course_people_in_charge):
        self.__course_people_in_charge = course_people_in_charge

    def set_course_commitment(self, course_commitment):
        self.__course_commitment = course_commitment

    def set_course_overview(self, course_overview):
        self.__course_overview = course_overview

    def set_course_objective(self, course_objective):
        self.__course_objective = course_objective

    def set_course_content(self, course_content):
        self.__course_content = course_content

    def set_course_requirements(self, course_requirements):
        self.__course_requirements = course_requirements

    def set_course_capacity(self, course_capacity):
        self.__course_capacity = course_capacity

    # getter methods
    def get_course_id(self):
        return self.__course_id

    def get_course_bookings(self):
        return self.__course_bookings

    def get_course_name(self):
        return self.__course_name

    def get_course_type(self):
        return self.__course_type

    def get_course_rating(self):
        return self.__course_rating

    def get_course_date(self):
        return self.__course_date

    def get_course_price(self):
        return self.__course_price

    def get_course_image(self):
        return self.__course_image

    def get_course_company(self):
        return self.__course_company

    def get_course_language(self):
        return self.__course_language

    def get_course_people_in_charge(self):
        return self.__course_people_in_charge

    def get_course_commitment(self):
        return self.__course_commitment

    def get_course_overview(self):
        return self.__course_overview

    # def get_course_(self):
    #     return self.__course_

    def get_course_objective(self):
        return self.__course_objective

    def get_course_content(self):
        return self.__course_content

    def get_course_requirements(self):
        return self.__course_requirements

    def get_course_capacity(self):
        return self.__course_capacity

    def get_course_bookings(self):
        return self.__course_bookings

    # other function

    def increase_bookings(self):
        self.__course_bookings += 1




