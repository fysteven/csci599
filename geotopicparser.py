import utility
import sys
import os
import json

try:
    from tika import parser
except ImportError as e:
    sys.stderr(e.message)
    pass

__author__ = 'Frank'


def generate_files_from_directory(path_to_dir):
    files_to_process = utility.get_all_files_in_directory(path_to_dir)
    destination_folder = 'geo-topic-parser-folder'
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    dir_name = os.path.basename(os.path.normpath(path_to_dir))

    with open(destination_folder + '/geo-topic-' + dir_name + '-files.txt', 'w') as output_file2:
        for line in files_to_process:
            output_file2.write(line)
            output_file2.write('\n')

    # with open(path_to_dir + '_allfiles.txt', 'w') as output_file:
    #     for line in files_to_process:
    #         output_file.write(line)
    #         output_file.write('\n')
    return


def generate_files_from_directories(a_list_of_dirs):
    files_to_process = utility.get_all_files_in_directories(a_list_of_dirs, verbose=True)

    destination_folder = 'geo-topic-parser-folder'
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    file_to_output = 'geo-topic-all-files.txt'
    with open(destination_folder + '/' + file_to_output, 'w') as output_file2:
        for line in files_to_process:
            output_file2.write(line)
            output_file2.write('\n')
        print('All the file names in the folders have been written to file: ')
        print('/'.join([destination_folder, file_to_output]))

    return


def parse_geo_topic(path_to_file_index):
    files_to_process = utility.read_lines_from_file(path_to_file_index)
    print('total files: ', len(files_to_process))

    working_folder = path_to_file_index + '_folder'
    if not os.path.exists(working_folder):
        os.mkdir(working_folder)
    for i in range(0, len(files_to_process)):
        if i % 1000 == 0:
            print(i)
        file1 = files_to_process[i]
        filename = file1.split('/')[-1]
        parsed = parser.from_file(file1)
        if 'content' in parsed and parsed['content'] is not None:
            out_file = '/'.join([working_folder, filename + '.txt'])
            with open(out_file, 'w') as output_file:
                output_file.write(parsed['content'].encode('utf-8'))

    return


def main():
    parameters = [
        ['generate_files', 'dir1 dir2 dir3 dir4'],
        ['parse_geo_topic', 'a_file_containing_all_file_names']
    ]
    if len(sys.argv) == 1:
        program = 'python'
        current_script = sys.argv[0]
        print('how to use this program?')
        print(' '.join([program, current_script] + parameters[0]))
        print(' '.join([program, current_script] + parameters[1]))
    elif len(sys.argv) == 3:
        if sys.argv[1] == parameters[1][0]:
            parse_geo_topic(sys.argv[2])
    if len(sys.argv) > 2:
        if sys.argv[1] == parameters[0][0]:
            generate_files_from_directories(sys.argv[2:len(sys.argv)])
    return


if __name__ == '__main__':
    main()

