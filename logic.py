'''Connection layer between the routes and the CSV handling layer.
It should have functions which can be called from the routing layer,
and they should call persistence layer functions.'''
import persistence
import util
import os.path
from operator import itemgetter
from datetime import datetime


def get_id(list_dict):
    highest = 0
    for row in list_dict:
        if int(row['id']) > highest:
            highest = int(row['id'])
    return highest + 1


def answer_dict(question_id, answer):
    answer_dict = {
        'id': get_id(persistence.get_all_items('answer')),
        'submission_time': str(datetime.now()),
        'vote_number': 0,
        'question_id': question_id,
        'message': answer,
    }

    return answer_dict


def question_dict(title, question):
    ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    question_dict = {
        'id': get_id(persistence.get_all_items('question')),
        'submission_time': str(datetime.now()),
        'view_number': 0,
        'vote_number': 0,
        'title': title,
        'message': question,
    }
    return question_dict


def comment_dict(comment, question_id='null', answer_id='null'):
    ['id', 'question_id', "answer_id", 'message', 'submission_time', 'count']
    comment_dict = {
        'id': get_id(persistence.get_all_items('comment')),
        'question_id': question_id,
        'answer_id': answer_id,
        'submission_time': str(datetime.now()),
        'message': comment,
        'edited_count': 0,
    }
    return comment_dict


def sort_list_of_dicts_by_time(dict_list):
    return sorted(dict_list, key=itemgetter('submission_time'))


def get_list_of_headers(dict_list):
    if dict_list == []:
        return []
    example_dict = dict_list[0]
    key_list = []
    for key in example_dict.keys():
        key_list.append(key)
    return key_list


def get_answers_in_question(dict_list, id_question):
    answers_list = []
    for item in dict_list:
        if int(item['question_id']) == int(id_question):
            answers_list.append(item)
    return answers_list


def vote_question(question_id, vote):
    '''

    :param question_id: id of the question (int)
    :param vote: value of True or False; if false vote down, if true vote up
    :return: void (just changes the database itself)
    '''

    questions = persistence.get_all_questions()
    for question in questions:
        if int(question['id']) == int(question_id):
            if vote is True:
                question['vote_number'] = int(question['vote_number']) + 1
            elif vote is False:
                question['vote_number'] = int(question['vote_number']) - 1
            persistence.update_question_vote(question)
            break


def vote_answer(answer_id, vote):
    answers = persistence.get_all_answers()
    for answer in answers:
        if int(answer['id']) == int(answer_id):
            if vote is True:
                answer['vote_number'] = int(answer['vote_number']) + 1
            elif vote is False:
                answer['vote_number'] = int(answer['vote_number']) - 1
            persistence.update_answer_vote(answer)
            break
