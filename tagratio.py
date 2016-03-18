import unittest


__author__ = 'Frank'


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
    with open(filename) as file1:
        ratio_array = compute_tag_ratio(file1)
        return ratio_array
        # print(ratio_array)


class TagRatioTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(main(), [0.0, 0.0, 0.0, 2.0, 1.5, 1.75, 1.75, 2.25, 1.5,
                          0.0, 3.25, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 3.0, 22, 0, 0.0, 0.0, 7.0])

if __name__ == '__main__':
    main()

