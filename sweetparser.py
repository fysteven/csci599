import json
from utility import get_all_files_in_directory
from xml.etree.ElementTree import parse, fromstring
import argparse
import yaoner
import os
from tika import parser

__author__ = 'Frank'


def parse_owl_file(filename):
    doc = parse(filename)
    # doc = parse(u)
    # doc = xml_text
    root = doc.getroot()

    concept_dictionary = dict()

    for child in root:
        if child.tag.endswith('Class'):
            concept = str()
            for attr in child.attrib:
                if attr.endswith('about'):
                    concept2 = child.attrib[attr]
                    if concept2.startswith('#'):
                        concept = concept2[1:]
            # print(concept)
            subclass_of = []
            for sub_child in child:
                if sub_child.tag.endswith('subClassOf'):
                    for attr in sub_child.attrib:
                        if attr.endswith('resource'):
                            parts = sub_child.attrib[attr].split('#')
                            if parts is not None and len(parts) > 0:
                                subclass_of.append(parts[-1])
            # print(subclass_of)
            concept_dictionary[concept] = subclass_of
    return concept_dictionary


def parse_owl_directory(path):
    file_list = get_all_files_in_directory(path, suffix='.owl')
    entologies = dict()
    for entry in file_list:
        print(entry)
        concept_dictionary = parse_owl_file(entry)
        entologies.update(concept_dictionary)
    dump(entologies, 'sweet_concepts.json')

    categories = transform_to_categories(entologies)
    dump(categories, 'sweet_concept_categories.json')
    return


def transform_to_categories(dictionary):
    categories = dict()

    for key in dictionary:
        value = dictionary[key]
        for item in value:
            if item not in categories:
                categories[item] = dict()
            categories[item][key] = 1

    return categories


def dump(dictionary, output):
    absolute_path = os.path.abspath(os.path.join(output, os.pardir))
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)

    json_data = json.dumps(dictionary)

    with open(output, 'w') as output_file:
        output_file.write(json_data)
    return


def intersect(json_filename, output_name, index_file, start_index=0, end_index=yaoner.MAX_INT_VALUE):
    base_directory = '/Users/Frank/Desktop/fulldump/raw-dataset/'
    if index_file is None:
        index_file = '/Users/Frank/PycharmProjects/599assignment1/geo-topic-parser-folder/geo-topic-all-files.txt'

    with open(json_filename) as json_file:
        json_data = json.load(json_file)

        concept_dictionary = dict()

        for key in json_data.keys():
            concept_dictionary[key.lower()] = {}

        file_list = yaoner.read_index_file(index_file, base_directory, start_index, end_index)

        for idx, val in enumerate(file_list):
            print(start_index + idx)
            parsed = parser.from_file(''.join([base_directory, val]))
            if 'content' in parsed and parsed['content'] is not None:
                content = parsed['content']
                words = content.split()
                for word in words:
                    lowercased = word.lower()
                    if lowercased in concept_dictionary:
                        last_part = os.path.basename(val)
                        concept_dictionary[lowercased][last_part] = 1
        dump(concept_dictionary, output_name + 'from' + str(start_index) + 'to' + str(end_index) + '.json')

    return


def reverse(dir_list, output_name):

    with open(output_name, 'w') as output_file:

        files = []
        for entry in dir_list:
            files.extend(get_all_files_in_directory(entry))

        json_data = {}
        for entry in files:
            with open(entry) as input_json:
                json_data.update(json.load(input_json))
        print(len(json_data))
        filename_sweet_dictionary = {}
        for key in json_data.keys():
            for filename in json_data[key].keys():
                if filename not in filename_sweet_dictionary:
                    filename_sweet_dictionary[filename] = {}
                filename_sweet_dictionary[filename][key] = 1
        print(len(filename_sweet_dictionary))
        # output_file.write(json.dumps(filename_sweet_dictionary))

    return


def main():

    arg_parser = argparse.ArgumentParser('Yao EXIF tool')
    arg_parser.add_argument('--mode', required=True, help='parse_owl, intersect, reverse')
    arg_parser.add_argument('--index', type=str, help='the index file containing all the paths to the file')
    arg_parser.add_argument('--input', nargs='+', required=False, type=str, help='paths to directory containing files')
    arg_parser.add_argument('--output', required=True, help='output file name')
    arg_parser.add_argument('--json', type=str, help='index file')
    arg_parser.add_argument('--start', type=str, help='index start at')
    arg_parser.add_argument('--end', type=str, help='index end at')

    args = arg_parser.parse_args()

    if args.mode == 'parse_owl' and args.input:
        # parse_owl_directory('/Users/Frank/Downloads/2.3/')
        parse_owl_directory(args.input)

    if args.mode == 'intersect' and args.json and args.output:
        if args.start and args.end:
            intersect(args.json, args.output, args.index, int(args.start), int(args.end))
        else:
            intersect(args.json, args.output, args.index)

    if args.mode == 'reverse' and args.input and args.output:
        reverse(args.input, args.output)
    return


if __name__ == '__main__':
    main()
