import connection
import bcrypt


@connection.connection_handler
def get_user_password_by_username(cursor, username):
    query = '''
    SELECT password FROM user_table
    WHERE user_name = %(username)s
    '''
    cursor.execute(query, {'username': username})
    return cursor.fetchall()


@connection.connection_handler
def get_user_id_by_username(cursor, username):
    query = '''
    SELECT user_id FROM user_table
    WHERE user_name = %(username)s
    '''
    cursor.execute(query, {'username': username})
    return cursor.fetchall()


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)
