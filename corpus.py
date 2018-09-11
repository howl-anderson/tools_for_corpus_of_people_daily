import os

from nltk.corpus.reader.conll import ConllCorpusReader
import utils


current_dir = os.path.dirname(os.path.abspath(__file__))


root = os.path.join(current_dir, './data/conllu')
utils.create_if_dir_not_exists(root)


def get_corpus_reader(
        fileids,
        columntypes=(
                ConllCorpusReader.WORDS,
                ConllCorpusReader.POS,
                ConllCorpusReader.NE,
                ConllCorpusReader.IGNORE
        ),
        root=root
    ):
    corpus_reader = ConllCorpusReader(
        root,
        fileids,
        columntypes
    )

    return corpus_reader
