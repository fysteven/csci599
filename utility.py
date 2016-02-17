import os
import sys
import json
# from os.path import isfile, join

__author__ = 'Frank'


def get_all_the_files(mypath):
    #onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyfiles = os.listdir(mypath)
    return onlyfiles


def get_all_files_in_directory(directory):
    files2 = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name == '.DS_Store':
                pass
            else:
                files2.append(os.path.join(root, name))
        # for name in dirs:
            # files2.append(os.path.join(root, name))
    return files2


def print_all_files(directory):
    files = get_all_files_in_directory(directory)
    print(len(files))
    for name in files:
        print(name)


def read_original_json(path_to_file):
    """
    to read a JSON file provided by TREC DD dataset
    :param path_to_file: the path to the file
    :return: a JSON object
    """
    with open(path_to_file) as file1:
        data = json.load(file1)
        count = 0
        for obj in data:
            count += int(obj['count'])
            print('mimeType', obj['mimeType'], 'count', obj['count'])
        print('total', count)
    return


def main():
    if len(sys.argv) == 1:
        program = 'python '
        current_script = sys.argv[0]
        print('how to use this program?')
        print(program + current_script + ' print path_to_directory')
        print(program + current_script + ' load_json path_to_json')
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'print':
            # print_all_files('/Users/Frank/windows10/awang-acadis-1')
            print_all_files(sys.argv[2])
        elif sys.argv[1] == 'load_json':
            read_original_json(sys.argv[2])


if __name__ == '__main__':
    main()
