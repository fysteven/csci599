import yaoner
import os
import sys
import utility

__author__ = 'Frank'


def generate_by_type(ratio_index, file_type_index, output_filename):
    # with open(output_filename, 'w') as output_file:
    with open(ratio_index) as ratio_index_file, open(file_type_index) as file_type_index_file:
        file_type_map = dict()
        for line in file_type_index_file:
            words = line.split()
            filename = words[0]
            filetype = words[1]
            file_type_map[filename] = filetype

        result_map = dict()
        count = 0
        for line in ratio_index_file:
            words = line.split()
            filename = words[0]
            file_ratio = words[1]
            if filename in file_type_map:
                filetype = file_type_map[filename]
                if filetype not in result_map:
                    result_map[filetype] = list()
                file_list = result_map[filetype]
                file_list.append((filename, file_ratio))
            else:
                print(count, filename)
                count += 1

        type_list = list()
        min_list = list()
        max_list = list()
        average_list = list()
        for entry in result_map.keys():
            # output_file_final_name = output_filename + entry + '.tsv'
            # utility.create_parent_folder_if_needed_for_output_file(output_file_final_name)
            # with open(output_file_final_name, 'w') as output_file2:
            #     for item in result_map[entry]:
            #         output_file2.write('\t'.join(item))
            #         output_file2.write('\n')
            the_list = result_map[entry]
            if len(the_list) < 2:
                continue
            type_list.append(entry)
            # print(the_list[1])
            min_value = float(the_list[0][1])
            max_value = float(min_value)
            average_value = max_value
            for i in range(1, len(the_list)):
                value = float(the_list[i][1])
                if value < min_value:
                    min_value = value
                elif value > max_value:
                    max_value = value
                average_value = (i / float(i + 1)) * average_value + (1 / float(i + 1)) * value
            min_list.append(min_value)
            max_list.append(max_value)
            average_list.append(average_value)
        # with open(output_filename, 'w') as output_file:
        print(type_list)
        print(min_list)
        print(max_list)
        print(average_list)
    return


def generate_ratio_of_metadata_to_file(metadata_index, file_index, output_filename):
    utility.create_parent_folder_if_needed_for_output_file(output_filename)
    with open(output_filename, 'w') as output_file:
        with open(metadata_index) as metadata_index_file, open(file_index) as file_index_file:
            content = list()
            content.append('filename\tratio')
            file_dictionary = dict()
            for line in file_index_file:
                words = line.split()
                filename = words[0]
                filesize = words[1]
                file_dictionary[filename] = float(filesize)
            for line in metadata_index_file:
                words = line.split()
                filename = words[0]
                metadata_json_size = float(words[1])
                if filename in file_dictionary:
                    content.append('\t'.join([filename, str(metadata_json_size / file_dictionary[filename])]))

            for entry in content:
                output_file.write(entry)
                output_file.write('\n')

    return


def combine_shell_ls_output(filename_list, output_name):
    # to combine the metadata size of JSON files
    content = list()
    with open(output_name, 'w') as output_file:

        for filename in filename_list:
            with open(filename) as input_file:
                for line in input_file:
                    words = line.split()
                    if len(words) == 9:
                        file_size = words[4]
                        file_hash_id = words[8].split('.')[0]
                        this_line = ' '.join([file_hash_id, file_size])
                        content.append(this_line)

        for line in content:
            output_file.write(line)
            output_file.write('\n')
    return


def run_for_file_size(output_name):
    index_file = '/Users/Frank/PycharmProjects/599assignment1/geo-topic-parser-folder/geo-topic-all-files.txt'
    base_directory = '/Users/Frank/Desktop/fulldump/raw-dataset/'

    with open(output_name, 'w') as output_file:
        file_list = yaoner.read_index_file(index_file, base_directory)

        file_size_list = list()

        for file_path in file_list:
            file_size = os.path.getsize(''.join([base_directory, file_path]))
            # file_name = os.path.basename(file_path)
            file_size_list.append(file_size)

        for idx, val in enumerate(file_size_list):
            entry = str(file_size_list[idx])
            file_name = os.path.basename(file_list[idx])
            output_file.write(' '.join([file_name, entry]))
            # output_file.write(' '.join([val[0], val[1]]))
            output_file.write('\n')


def main():
    # run_for_file_size('/Users/Frank/working-directory/filesize/file-size1.txt')
    # combine_shell_ls_output(sys.argv[1:], '/Users/Frank/working-directory/filesize/metadata-file-size.txt')
    # generate_ratio_of_metadata_to_file('/Users/Frank/working-directory/filesize/metadata-file-size.txt',
    #                                    '/Users/Frank/working-directory/filesize/file-size.txt',
    #                                    '/Users/Frank/working-directory/filesize/ratio-of-metadata-to-file.tsv')
    generate_by_type('/Users/Frank/working-directory/filesize/ratio-of-metadata-to-file.tsv',
                     '/Users/Frank/working-directory/fulldump/file-type-java.txt',
                     '/Users/Frank/working-directory/filesize/output/')
    return


if __name__ == '__main__':
    main()
