import utility
import shutil
import sys
import os
__author__ = 'Frank'


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


def main():
    if len(sys.argv) == 1:
        program = 'python '
        current_script = sys.argv[0]
        print('how to use this program?')
        print(program + current_script + ' move_files source_folder destination_folder')
    elif len(sys.argv) == 4:
        if sys.argv[1] == 'move_files':
            move_files(sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main()
