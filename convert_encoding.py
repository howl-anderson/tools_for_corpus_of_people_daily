#!/usr/bin/env python

import os

import utils


def convert_encoding(input_file, output_file,
                     input_encoding='gbk', output_encoding='utf8'):
    with open(input_file, 'rb') as input_fd, open(output_file, 'wb') as output_fd:
        file_content = input_fd.read()
        unicode_file_content = file_content.decode(input_encoding)
        output_fd.write(unicode_file_content.encode(output_encoding))


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(current_dir, 'data')
    utils.create_if_dir_not_exists(data_dir)

    input_file = os.path.join(data_dir, '1998-01-2003版-带音.txt')
    output_file = os.path.join(data_dir, 'raw_data.txt')

    convert_encoding(input_file, output_file)
