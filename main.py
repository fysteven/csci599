import json
from pprint import pprint
import cbor
import sys

__author__ = 'Frank'


def read_file(filename):
    with open(filename) as input_file:
        cbor_data = cbor.load(input_file)
        data = json.loads(cbor_data)
        body = data["response"]['body']
        result = bfd(body)
        print(result)
        return result


def read_file2(filename, fingerprints_data):
    with open(filename) as input_file:
        cbor_data = cbor.load(input_file)
        data = json.loads(cbor_data)
        body = data["response"]['body']
        result = ''
        if len(body) != 0:
            result = bfd(body)
            fingerprints_data[filename] = result['normalized']
        return result


def function1(filenames, bucket_name):
    """

    :param filenames: relative paths to file
    :param bucket_name:
    :return:
    """
    fingerprints_filename = bucket_name + '.fingerprints'
    with open(fingerprints_filename, 'rw') as fingerprints_file:
        fingerprints_data = {}
        try:
            fingerprints_data = json.load(fingerprints_file)
        except Exception as e:
            # print(e)
            error_message = []
            error_message.append(fingerprints_filename)
            error_message.append(' ')
            error_message.append(e.message)
            sys.stderr.write(''.join(error_message))
            sys.stderr.write('\n')
        for filename in filenames:
            if filename not in fingerprints_data:
                read_file2(filename, fingerprints_data)

        result = json.dumps(fingerprints_data)
        print(result)
        # fingerprints_file.write(result)
        # fingerprints_file.close()
    return


def read_from_type_files(filename):
    with open(filename) as file1:
        json_data = json.load(file1)
        files_to_process = []
        for key1 in json_data.keys():
            for key2 in json_data[key1].keys():
                files_to_process.append(key2)
        function1(files_to_process, file1.name.split('.')[0])


def bfd(data):
    # print('BFD')
    if data is None:
        return None
    else:
        letters = [0] * 256
        for char in data:
            # print(char)
            number = ord(char)
            if number < 256:
                letters[number] += 1

        max_count = 0
        for letter in letters:
            if letter > max_count:
                max_count = letter
        normalized = [0] * 256
        if max_count == 0:
            print(data)
            print(letters)
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
    read_file('./new/1409782224000.1')
    if len(sys.argv) == 1:
        program = 'python '
        current_script = sys.argv[0]
        print('how to use this program?')
        print(program + current_script + ' run_bfc path_to_type-files_file')
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'run_bfc':
            read_from_type_files(sys.argv[2])
    return


if __name__ == '__main__':
    main()

#with open('1409782224000.1') as file2:
 #   data = cbor.load(file2)
  #  json_data = json.loads(data)
   # print(json_data['response']['headers'][1][1])
