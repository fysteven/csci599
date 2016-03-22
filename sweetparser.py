import json
from utility import get_all_files_in_directory
from xml.etree.ElementTree import parse, fromstring

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
    json_data = json.dumps(dictionary)
    with open(output, 'w') as output_file:
        output_file.write(json_data)
    return


def main():
    parse_owl_directory('/Users/Frank/Downloads/2.3/')
    return


if __name__ == '__main__':
    main()

