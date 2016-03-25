import nltk
from tika import parser
import json
import os
import sys

__author__ = 'Frank'

MAX_INT_VALUE = 10000000

sentence = """At eight o'clock on Thursday morning
... Arthur didn't feel very good.
I have a 8-meter-long.
8 meters
8 meter
10 degrees Celsius
100 foot
100 feet
100 ft
five hundred yards
1001 mile
998 miles
Light meters (more correctly illuminance meters or luxmeters) are typically used to measure interior light levels of a few hundred lux.  The human eye has a very wide dynamic range; one can see objects illuminated with 0.005 lux, at which level outlines can just be perceived, through to the 100,000 lux of direct sunlight.  Light meters are commonly used over the range from 1 lux, the nuisance level from street lighting, to the 10,000 lux required in some surgical situations.  Specific requirements are frequently imposed by legislation, regulations, or contracts; for example 750 lux is required for the inspection of exported meat... (Click the title above for the full article.) (reproduced with permission from Automation and Control, October-November 2004 issue.)
"""


def extract_measurement(text):
    # print(type(text))
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)

    measurement_list = []
    i = 0
    while i < len(tagged) - 1:
        entry = tagged[i]
        next_entry = tagged[i + 1]

        # print(entry)
        if entry[1] == 'CD' and next_entry[1] in ('NN', 'NNS'):
            if next_entry[0] != ']' and next_entry[0] != '[':
                measurement_list.append(' '.join([entry[0], next_entry[0]]))
        i += 1
    return measurement_list


def read_index_file(path, base_dir='', start_index=0, end_index=MAX_INT_VALUE):
    file_list = []

    with open(path) as index_file:
        i = 0
        for line in index_file:
            if i < start_index:
                i += 1
                continue
            if start_index <= i < end_index:
                file_list.append(line.replace(base_dir, '')[:-1])
                i += 1
            else:
                break

    return file_list


def dump_to_json(a_list, output_dir, file_name):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(''.join([output_dir, file_name, '.json']), 'w') as output_file:
        json_data = json.dumps(a_list, indent=4)
        output_file.write(json_data)
    return


def run_ner(start_index=0, end_index=MAX_INT_VALUE):
    index_file = '/Users/Frank/PycharmProjects/599assignment1/geo-topic-parser-folder/geo-topic-all-files.txt'
    base_directory = '/Users/Frank/Desktop/fulldump/raw-dataset/'

    file_list = read_index_file(index_file, base_directory, start_index, end_index)

    measurement_list = []
    index = 0 + start_index
    for entry in file_list:
        print(index)
        parsed = parser.from_file(''.join([base_directory, entry]))
        if 'metadata' in parsed:
            if 'X-TIKA:EXCEPTION:embedded_exception' in parsed['metadata']:
                continue
        if 'content' in parsed:
            if parsed['content'] is not None:
                # print(json.dumps(parsed['metadata'], indent=4))
                measurements = extract_measurement(parsed['content'])
                if measurements is not None and len(measurements) > 0:
                    measurement_list.append({entry.split('/')[-1]: measurements})
        index += 1
    dump_to_json(measurement_list, '/Users/Frank/working-directory/ner-measurement-mentions/',
                 'from' + str(start_index) + 'to' + str(end_index))
    return


def main():
    # measurement_list = extract_measurement(sentence)
    # print(measurement_list)
    # parse_owl_directory('/Users/Frank/Downloads/2.3/')
    # read_index_file('/Users/Frank/PycharmProjects/599assignment1/geo-topic-parser-folder/geo-topic-all-files.txt',
    #                 '/Users/Frank/Desktop/fulldump/raw-dataset/')
    start_index = 0
    end_index = MAX_INT_VALUE
    if len(sys.argv) >= 2:
        start_index = int(sys.argv[1])
    if len(sys.argv) >= 3:
        end_index = int(sys.argv[2])
    print(start_index, end_index)
    run_ner(start_index, end_index)
    return


if __name__ == '__main__':
    main()
