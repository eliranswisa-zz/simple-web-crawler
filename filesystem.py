import os
import errno
import csv


def create_directory(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def create_file(file):
    open(file, 'w')


def write(file, data):
    file = open(file, 'w', encoding='utf8')
    file.write(data)
    file.close()


def read(file):
    file = open(file, 'r', encoding='utf8')
    data = file.read()
    file.close()

    return data


def append_to_csv(file, data):
    file = open(file, 'a')
    csv_file = csv.writer(file, delimiter='\t')
    csv_file.writerow(data)
