# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from CorpusToolkit.ply_parser.parser import make_parser
from CorpusToolkit.ply_parser.token import Token
from CorpusToolkit.chinese_utils import double_byte_to_single_byte
from CorpusToolkit.unit import Unit
import utils


class DataParserAndTranslator:
    def __init__(self, input_file, output_file):
        self.input_fd = open(input_file)
        self.output_fd = open(output_file, 'wt')

        self.parser = None

    def process(self, merge_sub_token=False,
                remove_geta_symbol=True,  # geta symbol is 〓, SIGHAN 2005 bakeoff PKU gold corpus removed it.
                extract_first_token_as_document_id=False,
                merge_family_name=True, merge_time=True,
                replace_double_byte_punctuation=True,
                output_doc_id=False):

        self.parser = make_parser(merge_sub_token)

        for raw_line in self.input_fd:
            # removing head and tail invisible char
            line = raw_line.strip()

            if not line:
                # skip empty line
                continue

            unit = Unit(self.parse_line(line))

            if remove_geta_symbol:
                unit = self.remove_geta_symbol(unit)

            if extract_first_token_as_document_id:
                unit = self.extract_first_token_as_document_id(unit)

            if merge_family_name:
                unit = self.merge_family_name(unit)

            if merge_time:
                unit = self.merge_time(unit)

            if replace_double_byte_punctuation:
                self.replace_double_byte_punctuation(unit)

            self.extract_ner(unit)

            pinyin_free_line = self.to_str(unit, output_doc_id)

            self.output_fd.write(pinyin_free_line + '\n')

    def parse_line(self, line_text):
        try:
            # TODO: add option to merge the `[]` or not
            result = self.parser.parse(line_text)
        except Exception:
            print(line_text)
            raise

        return result

    @staticmethod
    def merge_family_name(token_list):
        new_token_list = Unit([])
        new_token_list.id = token_list.id

        tokens_need_merge = []
        for token in token_list:
            if token.pos == 'nrf':
                tokens_need_merge.append(token)
            elif token.pos == 'nrg':
                tokens_need_merge.append(token)

                if len(tokens_need_merge) > 1:  # everything is fine
                    token = Token()
                    new_token_text = "".join([i.token for i in tokens_need_merge])
                    token.token = new_token_text
                    token.pos = 'nr'

                    new_token_list.append(token)
                else:  # something goes wrong, get all tokens back
                    new_token_list.extend(tokens_need_merge)

                # reset
                tokens_need_merge = []

            else:
                # just in case, in the bad case, reset
                tokens_need_merge = []

                new_token_list.append(token)

        # try got all tokens back, if not it will lost
        new_token_list.extend(tokens_need_merge)

        return new_token_list

    @staticmethod
    def merge_time(token_list):
        new_token_list = Unit([])
        new_token_list.id = token_list.id

        tokens_need_merge = []
        for token in token_list:
            if token.pos == 't':
                tokens_need_merge.append(token)
            elif len(tokens_need_merge) and token.pos != 't':
                new_token = Token()
                new_token_text = "".join([i.token for i in tokens_need_merge])
                new_token.token = new_token_text
                new_token.pos = 't'

                new_token_list.append(new_token)

                # reset
                tokens_need_merge = []

                # append current token
                new_token_list.append(token)
            else:
                new_token_list.append(token)

        # try merge at end
        if len(tokens_need_merge) > 1:
            new_token = Token()
            new_token_text = "".join([i.token for i in tokens_need_merge])
            new_token.token = new_token_text
            new_token.pos = 't'

            new_token_list.append(new_token)

        return new_token_list

    def extract_ner(self, token_list):
        def render_tag(tag):
            return "{}".format(tag)

        for token in token_list:
            if token.pos == "t":
                token.ner = render_tag('DATE')
            if token.pos == "nr":
                token.ner = render_tag("PERSON")
            if token.pos == "ns":
                token.ner = render_tag("GPE")
            if token.pos == "nt":
                token.ner = render_tag("ORG")

    @staticmethod
    def to_str(token_list, output_doc_id):
        token_str_list = []

        # append document id
        doc_id = token_list.id
        if output_doc_id and doc_id:
            token_str_list.append('# {}'.format(doc_id))

        for token_id, token in enumerate(token_list, start=1):
            token_str = "{}\t{}\t{}\t{}\t{}".format(token_id, token.token, token.pos, token.ner, token.pinyin)
            token_str_list.append(token_str)

        sentence_str = "\n".join(token_str_list)

        return sentence_str + "\n"

    @staticmethod
    def replace_double_byte_punctuation(token_list):
        for token in token_list:
            token.token = double_byte_to_single_byte(token.token)

    @staticmethod
    def extract_first_token_as_document_id(token_list):
        first_token = token_list[0]
        doc_id = first_token.token

        new_unit = Unit(token_list[1:])
        new_unit.id = doc_id
        return new_unit

    @staticmethod
    def remove_geta_symbol(token_list):
        return Unit(filter(lambda x: x.token != '〓', token_list))


def project_one():
    option = {
        'merge_sub_token': False,
        'remove_geta_symbol': True,
        'extract_first_token_as_document_id': True,
        'merge_family_name': False,
        'merge_time': False,
        'replace_double_byte_punctuation': False,
        'output_doc_id': False
    }

    parse_data(option)


def project_two():
    option = {
        'merge_sub_token': False,
        'remove_geta_symbol': True,
        'extract_first_token_as_document_id': True,
        'merge_family_name': True,
        'merge_time': True,
        'replace_double_byte_punctuation': True,
        'output_doc_id': False
    }

    parse_data(option)


def parse_data(option):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    input_file = os.path.join(current_dir, 'data', 'raw_data.txt')

    conllu_dir = os.path.join(current_dir, 'data', 'conllu')
    utils.create_if_dir_not_exists(conllu_dir)

    output_file = os.path.join(
        conllu_dir,
        'data_{}.conllu'.format('-'.join([str(i) for i in option.values()]))
    )

    data_cleaner = DataParserAndTranslator(input_file, output_file)
    data_cleaner.process(**option)


if __name__ == "__main__":
    project_one()
    project_two()
