import utility
import shutil
import sys
import os
import json

__author__ = 'Frank'

PRIORITY_PLACEHOLDER = 50


def move_files(source_folder, destination_folder):
    files = utility.get_all_files_in_directory(source_folder)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for filepath in files:
        filename = filepath.split('/')[-1]
        destination = [destination_folder, '/', filename]
        # print(filepath, ''.join(destination))
        shutil.move(filepath, ''.join(destination))
    return


def get_magic_bytes_from_file(file_content, mode='header/trailer', threshold=0.8):
    data = json.load(file_content)
    result = {}
    length = 50
    if mode == 'header/trailer':
        if data is not None:
            data2 = data
            result['header'] = []
            header = result['header']
            result['trailer'] = []
            trailer = result['trailer']
            for i in range(0, length):
                for j in range(0, 256):
                    value = data2['headerdata'][i][j]
                    if value >= threshold:
                        header.append({'x': i, 'y': j, 'v': value, 'char': unichr(j)})
                    value2 = data2['trailerdata'][i][j]
                    if value2 >= threshold:
                        trailer.append({'x': i, 'y': j, 'v': value2, 'char': unichr(j)})
    return result


def get_magic_bytes(folder):
    files = utility.get_all_files_in_directory(folder)
    data = {}
    for json_file in files:
        try:
            with open(json_file) as file1:
                magic_bytes = get_magic_bytes_from_file(file1)
                pure_name = file1.name.split('/')[-1]
                data[pure_name] = magic_bytes
        except Exception as e:
            sys.stderr.write(e.message)
            sys.stderr.write('\n')
    json_data = json.dumps(data, indent=4)
    print(json_data)
    return


def generate_mimetypes_xml_snippets(json_filename):
    output_result = []
    with open(json_filename) as json_file:
        json_data = json.load(json_file)
        for key in json_data.keys():
            output_result.append(key)
            output_result.append('\n')
            for key2 in json_data[key].keys():
                output_result.append(key2)
                output_result.append('\n')

                intermediate_for_type = dict()

                for byte_object in json_data[key][key2]:
                    if byte_object['v'] not in intermediate_for_type:
                        intermediate_for_type[byte_object['v']] = []
                    line = intermediate_for_type[byte_object['v']]
                    if True:
                        line.append(byte_object)
                        # line.append('    <match value=\"\\{0}\" type=\"string\" offset=\"{1}\"/>\n'.format(unicode(byte_object['y']), byte_object['x']))
                    else:
                        output_result.append('    <match value=\"')
                        output_result.append(unichr(byte_object['y']))
                        output_result.append('\" type=\"string\" offset=\"')
                        output_result.append(str(byte_object['x']))
                        output_result.append('\"/>\n')

                for value in intermediate_for_type.keys():
                    output_result.append('<magic priority=\"{0}\">\n'.format(int(value * PRIORITY_PLACEHOLDER)))
                    # output_result.extend(intermediate_for_type[value])
                    byte_objects = []
                    for byte_object in intermediate_for_type[value]:
                        if len(byte_objects) == 0:
                            byte_objects.append(byte_object)
                        else:
                            previous = byte_objects[-1]
                            if previous['x'] + 1 != byte_object['x']:
                                string_list = []
                                for item in byte_objects:
                                    byte_number = item['y']
                                    if byte_number >= 65 and byte_number <= 90\
                                            or byte_number >= 97 and byte_number <= 122:
                                        string_list.append(chr(byte_number))
                                    else:
                                        # string_list.append('\\')
                                        sys.stderr.write(repr(chr(byte_number)))
                                        sys.stderr.write('\n')
                                        string_list.append('\\x' + chr(byte_number).encode('hex'))

                                temp_string = ''.join(string_list)
                                output_result.append('    <match value=\"{0}\" type=\"string\" offset=\"{1}\"/>\n'
                                                     .format(temp_string, byte_objects[0]['x']))
                                byte_objects = []
                            byte_objects.append(byte_object)

                    string_list2 = []
                    for item in byte_objects:
                        byte_number = item['y']
                        if byte_number >= 65 and byte_number <= 90\
                                            or byte_number >= 97 and byte_number <= 122:
                            string_list2.append(chr(byte_number))
                        else:
                            # string_list2.append('\\')
                            string_list2.append('\\x' + chr(byte_number).encode('hex'))
                    temp_string = ''.join(string_list2)
                    output_result.append('    <match value=\"{0}\" type=\"string\" offset=\"{1}\"/>\n'
                                                     .format(temp_string, byte_objects[0]['x']))
                    output_result.append('</magic>\n')
            output_result.append('\n\n')
    # json_result = json.dumps(output_result, indent=4)
    final_string = ''.join(output_result)#.encode('utf-8')

    # post processing
    final_string_list = []

    print(final_string)

    return


def main():
    if len(sys.argv) == 1:
        program = 'python '
        current_script = sys.argv[0]
        print('how to use this program?')
        print(program + current_script + ' move_files source_folder destination_folder')
        print(program + current_script + ' get_magic_bytes source_folder')
        print(program + current_script + ' generate_mimetypes_xml_snippets source_folder')

    elif len(sys.argv) == 3:
        if sys.argv[1] == 'get_magic_bytes':
            get_magic_bytes(sys.argv[2])
        if sys.argv[1] == 'generate_mimetypes_xml_snippets':
            generate_mimetypes_xml_snippets(sys.argv[2])
    elif len(sys.argv) == 4:
        if sys.argv[1] == 'move_files':
            move_files(sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main()
