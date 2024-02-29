import pymysql

def mysql_check(check):
    try:
        connection = pymysql.connect(
            host=check['host'],
            user=check['username'],
            password=check['password']
        )
        with connection.cursor() as cursor:
            cursor.execute(check['statement'])
            result = cursor.fetchall()
        connection.commit()
        return 0
    except Exception as e:
        return e
    
if __name__ == '__main__':
    check = {
        "display_name": "mysql :0",
        "service": "mysql",
        "host": "192.168.151.98",
        "username": "root",
        "password": "root",
        "statement": "select user,host from mysql.user"
    }
    print(f'mysql: {mysql_check(check)}')