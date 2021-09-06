import bcrypt
import connection


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_word, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_word.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def add_new_account_into_db(cursor, user_name, hashed_password, current_date):
    query = '''
    INSERT INTO user_table(user_name, password, registration_date)
    VALUES(%(user_name)s, %(hashed_password)s, %(current_date)s)
    '''
    cursor.execute(query, {'user_name': user_name, 'hashed_password': hashed_password, 'current_date': current_date})
