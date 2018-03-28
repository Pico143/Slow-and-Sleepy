'''The layer that have access to any kind of long term data storage.
In this case, we use CSV files, but later on we'll change this to SQL database.
So in the future, we only need to change in this layer.'''

import psycopg2
import psycopg2.extras
from config import config


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper


@connection_handler



def search(cursor, search):
    cursor.execute("""
                    SELECT * FROM question
      LEFT JOIN answer ON question.id = answer.question_id
    WHERE LOWER(question.title) LIKE LOWER('%{0}%') OR LOWER(answer.message) LIKE LOWER('%{0}%');
    """.format(search['search_questions']))
    matching_questions = cursor.fetchall()
    print("MATCHING QUESTIONS: " , matching_questions)
    return matching_questions



def add_row_to_db(row, table):
    ''' Adds a new row into a given table, provided that dictionary is in a proper form
    (which is to be done by logic.py functions)
    Row - python dictionary to be added
    Table - String with a name of the table to add dictionary values to'''
    connection = open_database()
    cursor = connection.cursor()
    if table == "question":
        query = "INSERT INTO question (id,message,submission_time,title,view_number,vote_number) VALUES (%s, %s, %s, %s, %s, %s)"
    elif table == "answer":
        query = "INSERT INTO answer (id,message,question_id,submission_time,vote_number) VALUES (%s)"
    elif table == "comment":
        query = "INSERT INTO comment (answer_id,id,edited_count,message,question_id,submission_time) VALUES (%s)"
    values = []
    for key in sorted(row.keys()):
        values.append(str(row[key]))
    cursor.execute(query, values)

    '''
    query = ("INSERT INTO {0} (".format(table))
    query = list(query)
    columns = []
    for key in sorted(row.keys()):
        columns.append(str(key))
    columns = ','.join(columns)
    query.append(columns + ") VALUES (")
    values = []
    for key in sorted(row.keys()):
        if not key == 'submission_time':
            values.append("\'" + str(row[key]) + "\'")
        else:
            values.append("\'" + str(row[key]) + "\'")
    values = ','.join(values)
    query.append(values + ")")
    query = ''.join(query)
    '''
    connection.close()


def open_database():
    connection = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        connection.autocommit = True

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return connection


@connection_handler
def get_all_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer;
                   """)
    answers = cursor.fetchall()
    return answers


@connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                   """)
    questions = cursor.fetchall()
    return questions


@connection_handler
def delete_item(cursor, table, _id):
    cursor.execute("""
                    DELETE FROM {0}
                    WHERE id = {1};
                   """.format(table, _id))


@connection_handler
def get_item_by_id(cursor, table, _id):
    cursor.execute("""
                    SELECT *
                    FROM {0}
                    WHERE id = {1};
                   """.format(table, _id))
    question = cursor.fetchall()
    return question


@connection_handler
def get_item_by_question_id(cursor, table, _id):
    cursor.execute("""
                    SELECT *
                    FROM {0}
                    WHERE question_id = {1};
                   """.format(table, _id))
    question = cursor.fetchall()
    return question


@connection_handler
def update_question_vote(cursor, row):
    """

    :param cursor: psycopg2 cursor (provided by connection handler)
    :param row: Dictionary with updated row
    :return:
    """
    cursor.execute("""
                    UPDATE question SET vote_number = {0} WHERE id = {1};
                   """.format(row['vote_number'], row['id']))


@connection_handler
def update_answer_vote(cursor, row):
    """

    :param cursor: psycopg2 cursor (provided by connection handler)
    :param row: Dictionary with updated row
    :return:
    """
    cursor.execute("""
                    UPDATE answer SET vote_number = {0} WHERE id = {1};
                   """.format(row['vote_number'], row['id']))
