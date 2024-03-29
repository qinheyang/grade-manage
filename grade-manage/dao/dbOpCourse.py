from dao.dbConfig import localSourceConfig as localConfig
import pymysql

class Course:
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


    def courseList(self):
        try:
            self.cursor.execute("select class_code,class_name,class_id FROM sys_class ")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None


    def getcourseList(self,**params):
        try:
            sql="select class_code,class_name,class_id FROM sys_class where 1=1"
            param_list = []
            if params["class_name"] and params["class_name"] != "":
                sql += ' and  class_name like "%%"%s"%%"'
                param_list.append(params["class_name"])
            self.cursor.execute(sql, param_list)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None


    def courseSave(self, **course):
        try:


            if course["class_id"]:
                self.cursor.execute("select * from sys_class where class_id!=%s and class_code = %s",(course['class_id'],course['class_code']))
                data = self.cursor.fetchall()
                if data:
                    return "课程号已存在!"
                self.cursor.execute(
                    "update  sys_class set class_code = %s,class_name=%s where class_id=%s",

                    (course['class_code'],course['class_name'],course['class_id']))

            else:
                self.cursor.execute("select * from sys_class where class_code = %s",(course['class_code']))
                data = self.cursor.fetchall()
                if data:
                    return "课程号已存在!"
                self.cursor.execute(
                    "insert into sys_class (class_code,class_name) values(%s,%s)",
                    (course['class_code'],course['class_name']))

            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return None
    def courseDetail(self,courseId):
        try:
            self.cursor.execute("select * from sys_class where class_id =%s ",(courseId))
            return self.cursor.fetchone()
        except Exception as e:
            print(e)
            return None
    def courseDetele(self,classId):
        try:
            self.cursor.execute("delete from sys_class where class_id =%s ",(classId))
            self.db.commit()
        except Exception as e:
            print(e)
            return None
