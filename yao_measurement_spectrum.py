import os
import sys
import json
import csv
from yaoutility import *
from yaoner import extract_measurement

__author__ = 'Frank'


class Measurement:
    def __init__(self, number, unit):
        self.unit = unit
        self.min = number
        self.max = number
        self.average = number * 1.0
        self.count = 1

    def insert(self, number, unit):
        if unit.lower() != self.unit.lower():
            return None
        self.average = self.average * self.count / (self.count + 1.0) + number * 1.0 / (self.count + 1)
        self.count += 1
        if number < self.min:
            self.min = number
        elif number > self.max:
            self.max = number

    def to_json(self):
        return json.dumps(self.get_result_set())

    def get_result_set(self):
        return {'unit': self.unit, 'count': self.count, 'min': self.min, 'max': self.max, 'average': self.average}


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def run_for_spectrum_all(output_name):
    measurement_storage = MeasurementStorage('/Users/Frank/working-directory/ner-measurement-mentions/')
    measurement_dict = dict()

    output_dir = os.path.dirname(output_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_name, 'w') as output_file:
        csv_writer = csv.writer(output_file, delimiter='\t')
        csv_writer.writerow(['unit', 'count', 'min', 'max', 'average'])
        while measurement_storage.has_next_measurement_object():
            measurement_object = measurement_storage.get_next_measurement_object()
            for entry in measurement_object[1]['measurement']:
                measurement_mention = entry.split(' ')
                number = measurement_mention[0]
                unit = measurement_mention[1]
                if is_number(number):
                    number = float(number)
                    if unit not in measurement_dict:
                        measurement_dict[unit.lower()] = Measurement(number, unit)
                    else:
                        measurement = measurement_dict[unit.lower()]
                        measurement.insert(number, unit)

        intermediate_result = list()
        for entry in measurement_dict.keys():
            measurement = measurement_dict[entry]
            # intermediate_result.append(measurement.to_json())
            # intermediate_result.append('\n')
            intermediate_result.append([measurement.unit.encode('utf-8'), measurement.count, measurement.min, measurement.max,
                                        measurement.average])
        # json_data = json.dumps(measurement_dict)
        # output_file.write(''.join(intermediate_result))
        csv_writer.writerows(intermediate_result)
    return


def run_extract_measurements(input_file_name, output_file_name):
    with open(input_file_name) as input_file, open(output_file_name, 'w+') as output_file:
        string = input_file.read()
        string2 = []
        for char in string:
            if ord(char) < 128:
                string2.append(char)

        result = str()
        try:
            result = extract_measurement(''.join(string2))
        except UnicodeDecodeError as e:
            # sys.stderr(e.message)
            pass
        for entry in result:
            words = entry.split(' ')
            if words[1] == '%' or words[1] == '=' or words[1] == '-':
                continue
            output_file.write(entry)

            output_file.write('\n')
    return


def merge_units_of_measurement(file_list, output_name):
    unit_set = set()
    with open(output_name, 'w') as output_file:
        for input_file in file_list:
            with open(input_file) as file1:
                for line in file1:
                    words = line.split()
                    if len(words) >= 1:
                        unit = words[1].lower()
                        if unit not in unit_set:
                            unit_set.add(unit)

        for unit in unit_set:
            output_file.write(unit)
            output_file.write('\n')
    return


def filter_tsv(tsv_file, unit_list_index):
    with open(tsv_file) as input_file, open(unit_list_index) as unit_list_index_file, open(tsv_file + '.filtered', 'w') as output_file:
        unit_dictionary = set()
        for line in unit_list_index_file:
            words = line.split()
            if len(words) > 0:
                unit_dictionary.add(words[0].lower())

        csv_reader = csv.reader(input_file, delimiter='\t')
        csv_writer = csv.writer(output_file, delimiter='\t')
        count = 0
        for row in csv_reader:
            if count == 0:
                csv_writer.writerow(row)
                count += 1
                continue
            else:
                if row[0].lower() in unit_dictionary:
                    csv_writer.writerow(row)
                count += 1


def print_tsv(tsv_filename):
    with open(tsv_filename) as input_file:
        csv_reader = csv.reader(input_file, delimiter='\t')
        the_list = list()
        count = 0
        for row in csv_reader:
            # print(row)
            if count == 0:
                count += 1
                for _ in range(0, len(row)):
                    the_list.append(list())
                # the_list.append([list() for _ in range(0, len(row))])
                continue
            else:
                for idx, val in enumerate(row):
                    # print(idx)
                    if idx != 0:
                        val = float(val)
                    the_list[idx].append(val)

                count += 1

        for item in the_list:
            print(item)
    return


def main():

    # run_for_spectrum_all('/Users/Frank/working-directory/spectrum/spectrum-all.tsv')
    # run_extract_measurements('/Users/Frank/working-directory/units/nistsp330.txt', '/Users/Frank/working-directory/units/nistsp330-units.txt')
    # merge_units_of_measurement(['/Users/Frank/working-directory/units/nistsp330-units.txt'], '/Users/Frank/working-directory/units/all-units-new.txt')
    # filter_tsv('/Users/Frank/working-directory/spectrum/spectrum-all.tsv', '/Users/Frank/working-directory/units/all-units.txt')
    print_tsv('/Users/Frank/working-directory/spectrum/spectrum-all.tsv.filtered')
    return

if __name__ == '__main__':
    main()
