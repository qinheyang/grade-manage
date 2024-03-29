from dao.dbOpUser import User


def _initUser(u):
    global user
    user = u


def get_user():
    global user
    return user


def set_save_user_id(userId):
    global save_user_id
    save_user_id = userId
    return save_user_id


def get_save_user_id():
    global save_user_id
    return save_user_id


def set_save_course_id(courseId):
    global save_course_id
    save_course_id = courseId
    return save_course_id


def get_save_course_id():
    global save_course_id
    return save_course_id


def set_save_grade_id(gradeId):
    global save_grade_id
    save_grade_id = gradeId
    return save_grade_id


def get_save_grade_id():
    global save_grade_id
    return save_grade_id
