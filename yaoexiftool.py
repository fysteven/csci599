import json
import os
from tika import parser
from tika import detector
import utility
import argparse
import csv

__author__ = 'Frank'


def get_file_list(dir_list):
    result_list = []
    for entry in dir_list:
        result_list.extend(utility.get_all_files_in_directory(entry))

    return result_list


def run_exit_tool_on_known_type(dir_list):
    file_list = get_file_list(dir_list)

    for entry in file_list:
        parser.from_file(entry)

    return


def dump_to_json(output_name, data):
    absolute_path = os.path.abspath(os.path.join(output_name, os.pardir))
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)
    with open(output_name, 'w') as output_file:
        json_data = json.dumps(data, indent=4)
        output_file.write(json_data)
    return


def run_exist_tool(dir_list, output_name, subtype):
    file_list = get_file_list(dir_list)
    data = []
    for idx, val in enumerate(file_list):
        print(idx)
        with open(val) as input_file:
            mime_type = str()
            if subtype is not None:
                mime_type = subtype
            else:
                subtype = ''
                mime_type = detector.from_buffer(input_file)
            if mime_type is not None and mime_type.endswith(subtype):
                parsed = parser.from_buffer(input_file)
                if 'metadata' in parsed and parsed['metadata'] is not None:
                    file_name = val.split('/')[-1]
                    data.append({file_name: parsed['metadata']})

    dump_to_json(output_name, data)
    return


def filter_video_mp4(json_input):
    result = []
    with open(json_input) as json_file:
        json_data = json.load(json_file)

        for entry in json_data:
            key = entry.keys()[0]
            if entry[key]['Content-Type'] == 'video/mp4':
                result.append(entry)
    dump_to_json(json_input + '-filtered.json', result)
    return


def generate_tsv(json_list, output_name):
    with open(output_name, 'w') as output_file:
        csvwriter = csv.writer(output_file, delimiter='\t')
        # tsvparser = csv.writer(output_file, delimiter='\t')
        csvwriter.writerow(['filename', 'movieDataSize'])

        mp4_object_list = []
        rows = []
        for entry in json_list:
            with open(entry) as input_file:
                json_data = json.load(input_file)
                mp4_object_list.extend(json_data)

        field_to_work_on = 'Movie Data Size'
        for entry in mp4_object_list:
            key = entry.keys()[0]
            if field_to_work_on in entry[key]:
                rows.append([key.encode('utf-8'), entry[key][field_to_work_on].encode('utf-8')])

        csvwriter.writerows(rows)
    return


def main():
    arg_parser = argparse.ArgumentParser('Yao EXIF tool')
    arg_parser.add_argument('--mode', required=True, help='parse_mp4, filter_jsons, generate_tsv')
    arg_parser.add_argument('--inputDir', nargs='+', required=False, type=str, help='paths to directory containing files')
    arg_parser.add_argument('--output', required=True, help='output file name ')
    arg_parser.add_argument('--type', help='known type to work on')
    arg_parser.add_argument('--jsons', nargs='+', type=str, help='multiple json files containing mp4 metadata')
    args = arg_parser.parse_args()

    if args.inputDir and args.output and args.mode == 'parse_mp4':
        run_exist_tool(args.inputDir, args.output, args.type)

    if args.output and args.jsons and args.mode == 'generate_tsv':
        generate_tsv(args.jsons, args.output)
    return


if __name__ == '__main__':
    main()
