import os
import sys
import json
import csv
from yaoutility import *

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


def main():
    # measurement_storage = MeasurementStorage('/Users/Frank/working-directory/ner-measurement-mentions/')
    # print(measurement_storage.length_of_measurement_list())
    # print(measurement_storage.get_next_measurement_object())
    # print(measurement_storage.get_next_measurement_object())
    run_for_spectrum_all('/Users/Frank/working-directory/spectrum/spectrum-all.tsv')
    return

if __name__ == '__main__':
    main()
