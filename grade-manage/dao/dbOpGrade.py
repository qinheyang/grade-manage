from dao.dbConfig import localSourceConfig as localConfig
import pymysql


class Grade:
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

    def gradeList(self, **params):
        try:
            str1 = "SELECT sys_user.user_code,sys_user.user_name,sys_class.class_name,sys_user.profession,sys_grade.score,sys_grade.grade_id from sys_grade "
            str2 = "LEFT JOIN  sys_user on sys_user.user_id=sys_grade.user_id "
            str3 = "LEFT JOIN sys_class on sys_class.class_id=sys_grade.class_id where 1=1 "
            sql = str1+str2+str3
            param_list = []
            if params["class_id"] and params["class_id"] != "":
                sql += " and sys_class.class_id = %s "
                param_list.append(params["class_id"])
            if params["user_name"] and params["user_name"] != "":
                sql += ' and  sys_user.user_name like "%%"%s"%%"'
                param_list.append(params["user_name"])
            self.cursor.execute(sql, param_list)
            return self.cursor.fetchall()

        except Exception as e:
            print(e)
            return None


    def gradeSave(self, **grade):
        try:
            if grade["grade_id"]:
                self.cursor.execute(
                    "update  sys_grade set score = %s,user_id=%s,class_id =%s  where grade_id=%s",
                    (grade['score'],grade['user_id'], grade['class_id'], grade['grade_id']))

            else:
                self.cursor.execute(
                    "insert into sys_grade (user_id,class_id,score) values(%s,%s,%s)",
                    (grade['user_id'], grade['class_id'], grade['score']))

            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return None


    def gradeDetail(self, gradeId):
        try:
            self.cursor.execute("select * from sys_grade where grade_id =%s ", (gradeId))
            return self.cursor.fetchone()
        except Exception as e:
            print(e)
            return None


    def gradeDetele(self,gradeId):
        try:
            self.cursor.execute("delete from sys_grade where grade_id =%s ",(gradeId))
            self.db.commit()
        except Exception as e:
            print(e)
            return None


    def getGradeCount(self):
        try:
            self.cursor.execute("select region,count(*) as num from sys_grade left join tmp on sys_grade.score between tmp.lower and tmp.upper group by region  ")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
    def getGradeuUserCount(self):
        try:
            self.cursor.execute("select count(*) as num ,(select  class_name from sys_class where sys_class.class_id =sys_grade.class_id) as label from sys_grade GROUP BY class_id")
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None
