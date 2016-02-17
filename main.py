import json
from pprint import pprint
import cbor

__author__ = 'Frank'


def read_file(filename):
    with open(filename) as input_file:
        data = json.load(input_file)
        body = data["response"]['body']
        result = bfd(body)
        print(result)
        return result


def bfd(data):
    if data is None:
        return None
    else:
        letters = [0] * 256
        for char in data:
            letters[ord(char)] += 1
        max_count = 0
        for letter in letters:
            if letter > max_count:
                max_count = letter
        normalized = [0] * 256
        for i in range(len(letters)):
            normalized[i] = letters[i] / float(max_count)
        return {'letters': letters, 'normalized': normalized}


def bfd_correlation(file_content):
    pass


def bfd_correlation_from_file(path_to_file):
    if path_to_file is None:
        print('file')
    letters = [0] * 255
    with open(path_to_file, 'rb') as file:
        while True:
            byte = file.read(1)
            if byte == 0:
                pass

    return letters


def main():
    # read_file('a')
    return

if __name__ == '__main__':
    main()

with open('1409782224000.1') as file2:
    data = cbor.load(file2)
    json = json.loads(data)
    print(json['response']['body'])
