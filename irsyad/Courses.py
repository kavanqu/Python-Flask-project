class Course:
    count_id = 0

    def __init__(self, title, time, date):
        Course.count_id += 1
        self.__course_id = Course.count_id
        self.__category = None
        self.__title = title
        self.__time = time
        self.__date = date

    def get_course_id(self):
        return self.__course_id

    def get_category(self):
        return self.__category

    def get_title(self):
        return self.__title

    def get_time(self):
        return self.__time

    def get_date(self):
        return self.__date

    def set_course_id(self, course_id):
        self.__course_id = course_id

    def set_category(self, category):
        self.__category = category

    def set_title(self, title):
        self.__title = title

    def set_time(self, time):
        self.__time = time

    def set_date(self, date):
        self.__date = date
