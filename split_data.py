import os
import random
random.seed(0)

from nltk.corpus.reader.conll import ConllCorpusReader

from corpus import get_corpus_reader
import utils

current_dir = os.path.dirname(os.path.abspath(__file__))

corpus_reader = get_corpus_reader(
    columntypes=(
        ConllCorpusReader.IGNORE,
        ConllCorpusReader.WORDS,
        ConllCorpusReader.IGNORE,
        ConllCorpusReader.POS,
        ConllCorpusReader.IGNORE
    ),
    fileids=['data_False-True-True-True-True-True-False.conllu']
)


class DataSplitter:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def split_data(self, train=0.90, dev=0.00):
        sent_list = []
        for sent in corpus_reader.tagged_sents():
            sent_list.append(sent)

        random.shuffle(sent_list)

        sent_list_len = len(sent_list)

        train_set_len = int(sent_list_len * train)
        dev_set_len = int(sent_list_len * dev)
        test_set_len = sent_list_len - train_set_len - dev_set_len

        train_set = sent_list[:train_set_len]
        dev_set = sent_list[train_set_len: train_set_len + dev_set_len]
        test_set = sent_list[- test_set_len:]

        self.write_data(train_set, 'train')
        self.write_data(dev_set, 'dev')
        self.write_data(test_set, 'test')

    def write_data(self, data, data_set_name):
        output_file = self.get_output_file(data_set_name)

        with open(output_file, 'w') as fd:
            for sent in data:
                for id, token_and_more in enumerate(sent, start=1):
                    fd.write("\t".join([str(id)] + list(token_and_more)) + "\n")
                fd.write('\n')

    def get_output_file(self, data_set_name):
        return os.path.join(self.output_dir, data_set_name + '.conllu')


if __name__ == "__main__":
    split_data_dir = os.path.join(current_dir, 'data', 'split_data')
    utils.create_if_dir_not_exists(split_data_dir)

    data_splitter = DataSplitter(split_data_dir)

    data_splitter.split_data()
