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
def add_row_to_db(row, table):
    ''' Adds a new value into a given table, provided that dictionary is in a proper form
    (which is to be done by logic.py functions)
    Row - python dictionary to be added
    Table - String with a name of the table to add dictionary values to
    '''

    query = "INSERT INTO {0} (".format(table)
    query = list(query)
    for key in sorted(row.keys()):
        query.append(key + ", ")
    query.append(") VALUES (")
    for key in sorted(row.keys()):
        query.append(row[key] + ", ")
    query.append(")")
    ''.join(query)
    cursor.execute(query)


@connection_handler
def del_row_in_file(filename, fieldnames, row_number, row_id):
    list_dict = list_of_dict_from_file(filename, fieldnames)
    new_list = []
    for item in list_dict:
        if not str(item[row_id]) == str(row_number):
            new_list.append(item)
    with open(filename, 'w') as f:
        w = csv.DictWriter(f, fieldnames)
        w.writerows(new_list)

@connection_handler
def replace_row_in_file(filename, fieldnames, row_number, dict):
    list_dict = list_of_dict_from_file(filename, fieldnames)
    list_dict[row_number] = encoding_dict(dict)
    with open(filename, 'w') as f:
        w = csv.DictWriter(f, fieldnames)
        w.writerows(list_dict)


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



