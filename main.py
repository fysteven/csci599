import json
import utility
import datetime
import os
from pprint import pprint
try:
    import cbor
except ImportError as e:
    pass
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


def read_file3(filename, fingerprints_data):
    with open(filename) as input_file:
        data = input_file.read()
        result = ''
        if len(data) != 0:
            result = bfd(data)
            fingerprints_data[filename] = result['normalized']
        return result


def function1(filenames, bucket_name, output_result=True):
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
            error_message = [fingerprints_filename, ' ', e.message]
            sys.stderr.write(''.join(error_message))
            sys.stderr.write('\n')
        for filename in filenames:
            if filename not in fingerprints_data:
                read_file2(filename, fingerprints_data)

        if output_result:
            result = json.dumps(fingerprints_data)
            print(result)
        # fingerprints_file.write(result)
        # fingerprints_file.close()
    return fingerprints_data


def function2(filenames, bucket_name, output_result=True):
    """

    :param filenames: relative paths to file
    :param bucket_name:
    :return:
    """
    fingerprints_filename = bucket_name + '.fingerprints'

    fingerprints_data = {}
    try:
        with open(fingerprints_filename, 'rw') as fingerprints_file:
            fingerprints_data = json.load(fingerprints_file)
    except Exception as e:
            # print(e)
        error_message = [fingerprints_filename, ' ', e.message]
        sys.stderr.write(''.join(error_message))
        sys.stderr.write('\n')
        for filename in filenames:
            if filename not in fingerprints_data:
                read_file3(filename, fingerprints_data)

        if output_result:
            result = json.dumps(fingerprints_data)
            print(result)
        # fingerprints_file.write(result)
        # fingerprints_file.close()

    return fingerprints_data


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


def run_cross_correlation(folder_to_work_on):
    files = utility.get_all_files_in_directory(folder_to_work_on)
    folder_name = folder_to_work_on.split('/')[-1]

    # fingerprints are of all the files in the folder
    fingerprints_data = function2(files, folder_name, output_result=False)

    iteration = 0
    matrix = [[0 for _ in range(0, 256)] for _ in range(0, 256)]

    for byte_frequency_distribution in fingerprints_data.keys():
        bfd_fingerprint = fingerprints_data[byte_frequency_distribution]

        for i in range(1, 256):
            for j in range(0, i):
                difference = bfd_fingerprint[i] - bfd_fingerprint[j]
                matrix[i][j] = (matrix[i][j] * iteration + difference) / (iteration + 1)

    data = {'byte_frequency_cross_correlation': matrix, 'type': folder_name, 'files_processed': len(fingerprints_data)}
    print(json.dumps(data, indent=4))

    return


def correlation_strength(input_value):
    return 1 - abs(input_value)


def main():
    # read_file('./new/1409782224000.1')
    if len(sys.argv) == 1:
        program = 'python '
        current_script = sys.argv[0]
        print('how to use this program?')
        print(program + current_script + ' run_bfc path_to_type-files_file')
        print(program + current_script + ' run_cross_correlation folder_of_files')
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'run_bfc':
            read_from_type_files(sys.argv[2])
        elif sys.argv[1] == 'run_cross_correlation':
            start_time = datetime.datetime.now()
            print(start_time)
            run_cross_correlation(sys.argv[2])
            end_time = datetime.datetime.now()
            print(end_time)
            print(end_time - start_time)
    return


if __name__ == '__main__':
    main()

#with open('1409782224000.1') as file2:
 #   data = cbor.load(file2)
  #  json_data = json.loads(data)
   # print(json_data['response']['headers'][1][1])

