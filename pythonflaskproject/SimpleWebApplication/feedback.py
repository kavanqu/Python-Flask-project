class feedback:
    count_id = 0

    def __init__(self,rating, name,email,subject,detail):
        feedback.count_id += 1
        self.__user_id = feedback.count_id
        self.__rating = rating
        self.__name = name
        self.__email = email
        self.__subject = subject
        self.__detail = detail

    def get_user_id(self):
        return self.__user_id

    def get_rating(self):
        return self.__rating

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_subject(self):
        return self.__subject

    def get_details(self):
        return self.__detail

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_rating(self, rating):
        self.__rating = rating

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_subject(self, subject):
        self.__subject = subject

    def set_detail(self, detail):
        self.__detail = detail


class msg(feedback):
    def __init__(self,rating, name,email,subject,detail, reply):
        super().__init__(rating, name,email,subject,detail)
        self.__reply = reply

    def get_reply(self):
        return self.__detail

    def set_reply(self, reply):
        self.__reply = reply



