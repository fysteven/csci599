from tika import detector
import yaoner
import os

__author__ = 'Frank'


def detect_files(output_name):
    index_file = '/Users/Frank/PycharmProjects/599assignment1/geo-topic-parser-folder/geo-topic-all-files.txt'
    base_directory = '/Users/Frank/Desktop/fulldump/raw-dataset/'

    output_dir = os.path.dirname(output_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_name, 'w') as output_file:
        file_list = yaoner.read_index_file(index_file, base_directory)

        # file_type_map = dict()
        result_list = list()
        for idx, val in enumerate(file_list):
            file_name = os.path.basename(val)
            file_type = detector.from_file(''.join([base_directory, val]))
            # file_type_map[file_name] = file_type
            if file_type is not None:
                result_list.append(file_name)
                result_list.append(' ')
                result_list.append(file_type)
                result_list.append('\n')

        output_file.write(''.join(result_list))
    return


def main():
    detect_files('/Users/Frank/working-directory/fulldump/file-type.txt')


if __name__ == '__main__':
    main()