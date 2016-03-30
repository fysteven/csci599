from utility import get_all_files_in_directory
import json
import os
import datetime

__author__ = 'Frank'


class MeasurementStorage:
    def __init__(self, directory):
        self.measurement_list = []
        self.next = 0
        self.get_measurement_objects_from(directory)

    def get_measurement_objects_from(self, directory):
        files = get_all_files_in_directory(directory)

        for entry in files:
            with open(entry) as input_file:
                self.measurement_list.extend(json.load(input_file))

    def has_next_measurement_object(self):
        if self.next < len(self.measurement_list):
            return True
        else:
            return False

    def get_next_measurement_object(self):
        if not self.has_next_measurement_object():
            return None
        dictionary_object = self.measurement_list[self.next]
        self.next += 1
        filename = dictionary_object.keys()[0]
        measurement_metadata = {'measurement': dictionary_object[filename]}
        return filename, measurement_metadata


class SweetStorage:
    def __init__(self, json_input):
        self.sweet_list = []
        self.next = 0
        self.get_sweet_objects_from(json_input)

    def get_sweet_objects_from(self, json_input):
        with open(json_input) as input_file:
            json_data = json.load(input_file)
            for key in json_data.keys():
                self.sweet_list.append({key: json_data[key]})

    def has_next_sweet_object(self):
        if self.next < len(self.sweet_list):
            return True
        else:
            return False

    def get_next_sweet_object(self):
        if not self.has_next_sweet_object():
            return None
        sweet_object = self.sweet_list[self.next]
        self.next += 1
        filename = sweet_object.keys()[0]
        sweet_metadata = {'sweet': sweet_object[filename].keys()}
        return filename, sweet_metadata


class GeoTopicStorage:
    def __init__(self, directory):
        self.geo_topic_list = []
        self.next = 0
        self.get_geo_topic_objects_from(directory)

    def get_geo_topic_from_single_json(self, directory):
        files = get_all_files_in_directory(directory)
        for entry in files:
            with open(entry) as input_file:
                filename = os.path.basename(input_file.name).split('.')[0]
                metadata = json.load(input_file)
                self.geo_topic_list.append({filename: metadata})

    def get_geo_topic_objects_from(self, directory):
        files = get_all_files_in_directory(directory)

        for entry in files:
            with open(entry) as input_file:
                self.geo_topic_list.extend(json.load(input_file))

    def has_next_geo_topic_object(self):
        if self.next < len(self.geo_topic_list):
            return True
        else:
            return False

    def get_next_geo_topic_object(self):
        if not self.has_next_geo_topic_object():
            return None
        geo_topic_object = self.geo_topic_list[self.next]
        self.next += 1
        filename = geo_topic_object.keys()[0]
        geo_topic_metadata = geo_topic_object[filename]
        return filename, geo_topic_metadata


def main():
    time1 = datetime.datetime.now()
    measurement_storage = MeasurementStorage('/Users/Frank/working-directory/ner-measurement-mentions/')
    print(measurement_storage.get_next_measurement_object())
    print(measurement_storage.get_next_measurement_object())

    sweet_storage = SweetStorage('/Users/Frank/working-directory/filename-sweet/filename-sweet.json')
    print(sweet_storage.get_next_sweet_object())
    print(sweet_storage.get_next_sweet_object())

    geo_topic_storage = GeoTopicStorage('/Users/Frank/working-directory/geo-topic-parser-folder-output/')
    print(geo_topic_storage.get_next_geo_topic_object())
    print(geo_topic_storage.get_next_geo_topic_object())

    time2 = datetime.datetime.now()
    print(time2 - time1)
    return


if __name__ == '__main__':
    main()
