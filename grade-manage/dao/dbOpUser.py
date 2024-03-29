from dao.dbConfig import localSourceConfig as localConfig
import pymysql


class User:
    def __init__(self, config=localConfig):
        self.db = pymysql.connect(host=config['host'], port=config['port'], user=config['user'],
                                  passwd=config['passwd'], db=config['db'], charset=config['charset'],
                                  )
        if config['cursorclass'] is not None:
            self.cursor = self.db.cursor(config['cursorclass'])
        else:
            self.cursor = self.db.cursor()

        self.role=None

    def userLogin(self, usercode, password):
        try:
            self.cursor.execute("select * from sys_user")
            data = self.cursor.fetchall()
            for row in data:
                if row['user_code'] == usercode and row['password'] == password:
                    self.usercode = usercode
                    self.password = password
                    self.user_id = row['user_id']
                    self.user_code = row['user_code']
                    self.team = row['team']
                    self.profession = row['profession']
                    self.role = row['role']
                    return row['role']
        except Exception as e:
            print(e)
            return False

    def userList(self,**params):
        try:
            sql="select user_code,user_name,team,profession,`role`,user_id from sys_user where 1=1"
            param_list = []
            if params["role"] and params["role"] != "":
                sql += " and sys_user.role = %s "
                param_list.append(params["role"])
            if params["user_name"] and params["user_name"] != "":
                sql += ' and  sys_user.user_name like "%%"%s"%%"'
                param_list.append(params["user_name"])
            self.cursor.execute(sql, param_list)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    def userDetail(self,userId):
        try:
            self.cursor.execute("select * from sys_user where user_id =%s ",(userId))
            return self.cursor.fetchone()
        except Exception as e:
            print(e)
            return None


    def userSave(self, **user):
        try:


            if user["user_id"]:
                self.cursor.execute("select * from sys_user where user_id !=%s and user_code = %s",(user['user_id'],user['user_code']))
                data = self.cursor.fetchall()
                if data:
                    return "工号/学号已存在!"
                self.cursor.execute(
                    "update  sys_user set user_code = %s,team=%s,profession=%s,user_name=%s,password=%s,`role`=%s where user_id=%s",

                    (user['user_code'], user['team'], user['profession'], user['user_name'], user['password'],
                     user['role'], user['user_id']))

            else:
                self.cursor.execute("select * from sys_user where user_code = %s",(user['user_code']))
                data = self.cursor.fetchall()
                if data:
                    return "工号/学号已存在!"
                self.cursor.execute(
                    "insert into sys_user (user_code,team,profession,user_name,password,`role`) values(%s,%s,%s,%s,%s,%s)",
                    (user['user_code'], user['team'], user['profession'], user['user_name'], user['password'],
                     user['role']))

            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return None

    def userDetele(self,userId):
        try:
            self.cursor.execute("delete from sys_user where user_id =%s ",(userId))
            self.db.commit()
        except Exception as e:
            print(e)
            return None

    def userListByRole(self,role):
        try:
            self.cursor.execute("select user_code,user_name,team,profession,`role`,user_id from sys_user where `role`= %s",(role))
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

