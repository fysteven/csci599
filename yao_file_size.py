import yaoner
import os

__author__ = 'Frank'


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
    run_for_file_size('/Users/Frank/working-directory/filesize/file-size1.txt')

if __name__ == '__main__':
    main()
