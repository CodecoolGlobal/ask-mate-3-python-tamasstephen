import connection


def get_unused_tags(question_id):
    all_tags = get_all_tags()
    used_tags = [item["tag_id"] for item in get_tags_in_use(question_id)]
    tags = [item for item in all_tags if item["id"] not in used_tags]
    return tags


@connection.connection_handler
def get_all_tags(cursor):
    query = """
         SELECT * FROM tag
         """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_tags_in_use(cursor, question_id):
    query = """
        SELECT * FROM question_tag
        WHERE question_id = %(question_id)s 
    """
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


def add_tags_to_question(question_id, tags):
    for tag in tags.values():
        print(tag)
        add_attach_tag_to_question(question_id, tag)


@connection.connection_handler
def add_attach_tag_to_question(cursor, question_id, tag_id):
    query = """
        INSERT INTO question_tag
        (question_id, tag_id) 
        VALUES (%(question_id)s, %(tag_id)s)
    """
    cursor.execute(query, {"question_id": question_id,
                           "tag_id": tag_id})


def get_question_tags(question_id):
    tags = [get_tags_by_tag_id(item["tag_id"]) for item in get_tags_in_use(question_id)]
    print(tags)
    return tags


@connection.connection_handler
def get_tags_by_tag_id(cursor, tag_id):
    query = """
        SELECT * FROM tag
        WHERE id = %(tag_id)s
    """
    cursor.execute(query, {"tag_id": tag_id})
    return cursor.fetchall()


def create_new_tag(tag):
    # later need to validate(wether tag exist or not)
    add_new_tag_to_db(tag)


@connection.connection_handler
def add_new_tag_to_db(cursor, tag):
    query = '''
    INSERT INTO tag
    (name)
    VALUES(%(tag)s)
    '''
    cursor.execute(query, {'tag': tag})


@connection.connection_handler
def delete_tag_from_question_tag_db(cursor, question_id, tag_id):
    query = '''
    DELETE FROM question_tag
    WHERE question_id = %(question_id)s and tag_id = %(tag_id)s
    '''
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})
