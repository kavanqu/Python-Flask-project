class CourseCategory:
    count_id = 0

    def __init__(self, title):
        CourseCategory.count_id += 1
        self.__category_id = CourseCategory.count_id
        self.__title = title
        self.__courses = []

    def get_category_id(self):
        return self.__category_id

    def get_title(self):
        return self.__title

    def get_courses(self):
        return self.__courses

    def set_category_id(self, category_id):
        self.__category_id = category_id

    def set_title(self, title):
        self.__title = title

    @staticmethod
    def add_course(db, category_name, course):
        categories_dict = db['Categories']
        category = categories_dict[category_name]
        category.get_courses().append(course)
        categories_dict[category_name] = category
        db['Categories'] = categories_dict
        course.set_category(category)
