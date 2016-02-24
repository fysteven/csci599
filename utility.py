import os
import sys
import json
try:
    import cbor
except ImportError, e:
    pass

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


def generate_move_commands(base_directory):
    files = get_all_files_in_directory(base_directory)
    result = []
    output_folder_name = 'generated_files'
    result.append('mkdir ' + base_directory + '/' + output_folder_name)
    print(''.join(result[0]))
    for filename in files:
        if filename == '.DS_Store':
            print('ds')
            continue
        temp = []
        temp.append('mv \"')
        temp.append(filename)
        temp.append('\" ')
        temp.append(base_directory)
        temp.append('/')
        temp.append(output_folder_name)
        temp.append('/')
        result.append(''.join(temp))
        print(''.join(temp))
    # print(result)
    return


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
    errors = []
    for item in files:
        with open(item) as file2:
            try:
                data = cbor.load(file2)
                json_data = json.loads(data)
                content_type_array = json_data['response']['headers'][1]
                hasp_map[json_data['key']] = {content_type_array[0]: content_type_array[1]}
            except Exception as e:
                errors.append(e.message)
    result = json.dumps(hasp_map, indent=4)
    with open(directory.split('/')[-1] + '.dump', 'w') as dumpfile:
        for item in errors:
            dumpfile.write(item)
            dumpfile.write('\n')
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


def generate_index_for_folder(path_to_folder):
    data = {}
    all_files = get_all_files_in_directory(path_to_folder)
    for item in all_files:
        parent_dir = os.path.dirname(item)
        current_filename = item.split('/')[-1]
        parent_dir_name = parent_dir.split('/')[-1]
        real_type = parent_dir_name
        if real_type in data:
            data[real_type]['count'] += 1
            data[real_type]['files'][current_filename] = '1'
        else:
            data[real_type] = dict()
            data[real_type]['count'] = 1
            data[real_type]['files'] = {current_filename: '1'}
    result = json.dumps(data, indent=4)
    print(result)


def merge_our_json(jsons):
    data = {}
    file_data = []
    for item in jsons:
        with open(item) as file1:
            file_data.append(json.load(file1))

    for json_object in file_data:
        for real_type in json_object.keys():
            if real_type not in data:
                data[real_type] = dict()
                data[real_type]['count'] = 0
                data[real_type]['files'] = dict()
            for file_hash_id in json_object[real_type]['files'].keys():
                if file_hash_id not in data[real_type]['files']:
                    # data[real_type]['files'][file_hash_id] = '1'
                    data[real_type]['count'] += 1

    result = json.dumps(data, indent=4, sort_keys=True)
    print(result)


def count_files(path_to_file):
    count = 0
    with open(path_to_file) as file1:
        json_data = json.load(file1)
        for key in json_data.keys():
            count += int(json_data[key]['count'])
    print(count)
    return count


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
        print(program + current_script + ' generate_mv_commands path_to_directory')
        print(program + current_script + ' generate_index_for_folder path_to_dir')
        print(program + current_script + ' merge_jsons json1 json2 json3 ...')
        print(program + current_script + ' count_files json_file')
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
        elif sys.argv[1] == 'generate_mv_commands':
            generate_move_commands(sys.argv[2])
        elif sys.argv[1] == 'generate_index_for_folder':
            generate_index_for_folder(sys.argv[2])
        elif sys.argv[1] == 'count_files':
            count_files(sys.argv[2])
    elif len(sys.argv) == 4:
        if sys.argv[1] == 'merge_type_and_key':
            merge_type_and_key(sys.argv[2], sys.argv[3])
    if len(sys.argv) > 2:
        if sys.argv[1] == 'merge_jsons':
            merge_our_json(sys.argv[2:len(sys.argv)])

if __name__ == '__main__':
    main()

