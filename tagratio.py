import unittest
import re

__author__ = 'Frank'


def remove_tags(content):
    current_in_script_state = False
    result_content = []
    for char in content:
        if char == '<':
            current_in_script_state = True
            result_content.append(' ')
        if current_in_script_state:
            pass
        else:
            result_content.append(char)
        if char == '>':
            current_in_script_state = False
    return ''.join(result_content)


def remove_tags2(content):
    current_in_tag_state = False
    current_in_quote_state = False
    current_quote = None
    result_content = []
    for char in content:
        if current_in_tag_state:
            if current_in_quote_state:
                if char == current_quote:
                    current_in_quote_state = False
                    current_quote = None
            else:
                if char == '>':
                    current_in_tag_state = False
                elif char == '\'' or char == '\"':
                    current_quote = char
                    current_in_quote_state = True
        else:
            if char == '<':
                current_in_tag_state = True
                result_content.append(' ')
            else:
                result_content.append(char)
    return ''.join(result_content)


# def remove_script_tags(content):
#     pattern = ur'<script'
#     positions = []
#     for match in re.finditer(pattern, content):
#         # print(match.start(), match.end())
#         positions.append(match.start())
#     return positions


def remove_script_tags2(content):
    positions = []
    current_in_script_state = False
    current_in_tag_state = False
    current_in_closing_tag_state = False
    current_tag_name = None
    script_position_set = set()
    for idx, val in enumerate(content):
        if current_in_tag_state:
            if current_tag_name:
                if val == '>':
                    current_tag_name = None
                    current_in_tag_state = False
                    if current_in_script_state:
                        script_position_set.add(idx)
                        if current_in_closing_tag_state:
                            current_in_script_state = False
                            current_in_closing_tag_state = False
                elif current_tag_name == 'script':
                    script_position_set.add(idx)
            else:
                if val == ' ':
                    pass
                elif val == '/':
                    current_in_closing_tag_state = True
                elif content[idx: idx + 6] == 'script':
                    # if current_in_script_state:
                    #     current_in_tag_state =
                    current_tag_name = 'script'
                    current_in_script_state = True
                    # script_position_set.add()
                    if not current_in_closing_tag_state:
                        for index in range(idx, -1, -1):
                            script_position_set.add(index)
                            if content[index] == '<':
                                break
                else:
                    current_tag_name = 'special_tag'
        else:
            if current_in_script_state:
                script_position_set.add(idx)
                if content[idx: idx + 2] == '</':
                    script_position_set.add(idx + 1)
                    script_position_set.add(idx + 2)
                    current_in_tag_state = True
                    current_in_closing_tag_state = True
            else:
                if val == '<':
                    current_in_tag_state = True
    result = []
    # print(script_position_set)
    for idx, val in enumerate(content):
        if idx not in script_position_set:
            result.append(val)
    return ''.join(result)


def compute_tag_ratio(content):
    ratio_array = []
    for line in content:
        text = 0
        tags = 0.0
        # use float to get float result in the end
        if len(line) > 0:
            index = 0
            last = len(line) - 1
            while line[index] == ' ':
                index += 1
            while last >= 0 and (line[last] == ' ' or line[last] == '\n'):
                last -= 1

            current_in_tag = False
            while index <= last:
                if line[index] == '<':
                    current_in_tag = True
                    tags += 1
                elif line[index] == '>':
                    current_in_tag = False
                elif current_in_tag is False:
                    text += 1
                index += 1
        ratio = float()
        if tags == 0:
            ratio = text
        else:
            ratio = text / tags
        ratio_array.append(ratio)
        print(text, tags, ratio, line)
    return ratio_array


def main():
    filename = './test/html_snippet.html'
    # filename = '/Users/Frank/Desktop/xhtml nested quotes - Google Search.html'
    with open(filename) as file1:
        # ratio_array = compute_tag_ratio(file1)
        # return ratio_array
        # print(ratio_array)
        result = remove_script_tags2(file1.read())
        print(result)

# class TagRatioTest(unittest.TestCase):
#     def test1(self):
#         self.assertEqual(main(), [0.0, 0.0, 0.0, 2.0, 1.5, 1.75, 1.75, 2.25, 1.5,
#                           0.0, 3.25, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 3.0, 22, 0, 0.0, 0.0, 7.0])

if __name__ == '__main__':
    main()

