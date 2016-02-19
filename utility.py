import os
import sys
import json
import cbor
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


def generate_own_json(path_to_file):
    with open(path_to_file) as file1:
        data = {}
        files = {}
        folder = {}
        i = 0
        for line in file1:
            if i == 0:
                data['total_count'] = line.split()[0]
            else:
                # line = file1[i]
                words = line.split('.')
                if len(words) == 2:
                    key = line.split('\n')[0]
                    files[key] = {'key': words[0].replace('/', '_')}
            i += 1
        data['files'] = files
        folder[file1.name.split('.')[0]] = data
        json_data = json.dumps(folder, indent=4)
        print(json_data)
        return


def get_content_type(directory):
    files = get_all_files_in_directory(directory)
    hasp_map = {}
    for item in files:
        with open(item) as file2:
            data = cbor.load(file2)
            json_data = json.loads(data)
            content_type_array = json_data['response']['headers'][1]
            hasp_map[json_data['key']] = {content_type_array[0]: content_type_array[1]}
    result = json.dumps(hasp_map, indent=4)
    return result


def print_content_type(directory):
    print(get_content_type(directory))


def merge_type_and_key(content_type_file_name, key_file_name):
    with open(content_type_file_name) as content_type_file, open(key_file_name) as key_file:
        file_name_list = key_file.name.split('.')
        if len(file_name_list) >= 1:
            original_file_name = file_name_list[0]
            metadata_json = json.load(key_file)
            content_type_json = json.load(content_type_file)

            files = metadata_json[original_file_name]['files']

            data = {}
            for path in files.keys():
                key = files[path]['key']
                content_type = content_type_json[key]['Content-Type']
                real_type = content_type.split(';')[0]
                if real_type in data:
                    temp = data[real_type]
                    temp[path] = '1'
                else:
                    temp = dict()
                    temp[path] = '1'
                    data[real_type] = temp
            # print(data)
            result = json.dumps(data, indent=4)
            print(result)


def main():
    if len(sys.argv) == 1:
        program = 'python '
        current_script = sys.argv[0]
        print('how to use this program?')
        print(program + current_script + ' print path_to_directory')
        print(program + current_script + ' load_json path_to_json')
        print(program + current_script + ' generate_json path_to_json')
        print(program + current_script + ' get_content_type path_to_directory')
        print(program + current_script + ' merge_type_and_key file1 file2')
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'print':
            # print_all_files('/Users/Frank/windows10/awang-acadis-1')
            print_all_files(sys.argv[2])
        elif sys.argv[1] == 'load_json':
            read_original_json(sys.argv[2])
        elif sys.argv[1] == 'generate_json':
            generate_own_json(sys.argv[2])
        elif sys.argv[1] == 'get_content_type':
            print_content_type(sys.argv[2])
    elif len(sys.argv) == 4:
        if sys.argv[1] == 'merge_type_and_key':
            merge_type_and_key(sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()
