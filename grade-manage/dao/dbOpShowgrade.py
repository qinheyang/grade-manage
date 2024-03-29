from dao.dbConfig import localSourceConfig as localConfig
import pymysql


class ShowGrade:
    def __init__(self, config=localConfig):
        self.db = pymysql.connect(host=config['host'], port=config['port'], user=config['user'],
                                  passwd=config['passwd'], db=config['db'], charset=config['charset'],
                                  )
        if config['cursorclass'] is not None:
            self.cursor = self.db.cursor(config['cursorclass'])
        else:
            self.cursor = self.db.cursor()
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()

    def show_gradeList(self,**params):
        try:

            str1="SELECT sys_user.user_code,sys_user.user_name,sys_class.class_code,sys_class.class_name,sys_grade.score from sys_grade "
            str2="  LEFT JOIN sys_user  on sys_user.user_id=sys_grade.user_id "
            str3=" LEFT JOIN sys_class on sys_class.class_id=sys_grade.class_id where 1=1"
            sql=str1+str2+str3
            param_list = []
            if params["class_id"] and params["class_id"] != "":
                sql += " and sys_class.class_id = %s "
                param_list.append(params["class_id"])

            self.cursor.execute(sql, param_list)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            self.cursor.close()
            self.db.close()
            return None

    def showGradeListByUserId(self, **params):
        try:

            str1 = "SELECT sys_user.user_code,sys_user.user_name,sys_class.class_code,sys_class.class_name,sys_grade.score from sys_grade "
            str2 = "  LEFT JOIN sys_user  on sys_user.user_id=sys_grade.user_id "
            str3 = " LEFT JOIN sys_class on sys_class.class_id=sys_grade.class_id where 1=1"
            sql = str1 + str2 + str3
            param_list = []
            if params["class_id"] and params["class_id"] != "":
                sql += " and sys_class.class_id = %s "
                param_list.append(params["class_id"])
            if params["user_code"] and params["user_code"] != "":
                sql += " and sys_user.user_code = %s "
                param_list.append(params["user_code"])
            self.cursor.execute(sql, param_list)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            self.cursor.close()
            self.db.close()
            return None
