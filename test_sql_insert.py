import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='test_python', charset='utf8')


#conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test_python', charset='utf8')
#conn.autocommit(False)
cursor = conn.cursor()

username="username"
password="password"

sql = "INSERT INTO user VALUES(%(username)s, %(password)s, %(email)s)"

value = {"username":username,
         "password":password,
         "email":"123456@ouvps.com"}
cursor.execute(sql, value)


sql2 = "INSERT INTO user VALUES('ssss', 'sdfsd', 'sdfsdf');"
cursor.execute(sql2)
conn.commit()
cursor.close()
conn.close()

print("insert finished")