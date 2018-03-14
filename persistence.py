'''The layer that have access to any kind of long term data storage.
In this case, we use CSV files, but later on we'll change this to SQL database.
So in the future, we only need to change in this layer.'''

import csv


def write_form_to_file(filename, fieldnames, dict):
    with open(filename, 'a') as f:
        w = csv.DictWriter(f, fieldnames)
        w.writerow(dict)


def list_of_dict_from_file(filename, fieldnames):
    try:
        with open(filename) as f:
            reader = csv.DictReader(f, fieldnames)
            dics = [d for d in reader][1:]
            return dics
    except FileNotFoundError:
        with open(filename, "w") as f:
            w = csv.DictWriter(f, fieldnames)
            w.writeheader()
        return {}


def del_row_in_file(filename, fieldnames, row_number):
    list_dict = list_of_dict_from_file(filename, fieldnames)
    del list_dict[row_number]
    with open(filename, 'w') as f:
        w = csv.DictWriter(f, fieldnames)
        w.writeheader()
        w.writerows(list_dict)


def replace_row_in_file(filename, fieldnames, row_number, dict):
    list_dict = list_of_dict_from_file(filename, fieldnames)
    list_dict[row_number] = dict
    with open(filename, 'w') as f:
        w = csv.DictWriter(f, fieldnames)
        w.writeheader()
        w.writerows(list_dict)
