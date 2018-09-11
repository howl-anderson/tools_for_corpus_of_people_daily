import os

from nltk.corpus.reader.conll import ConllCorpusReader
from tokenizer_tools.tagset.NER.BILUO import BILUOEncoderDecoder

from corpus import get_corpus_reader
import utils


current_dir = os.path.dirname(os.path.abspath(__file__))

conllu_dir = os.path.join(current_dir, 'data/split_data')
utils.create_if_dir_not_exists(conllu_dir)

token_dir = os.path.join(current_dir, 'data/split_char_crfpp')
utils.create_if_dir_not_exists(token_dir)

encoder_cache = {}


def main(delimit="  "):
    for root, dirs, files in os.walk(conllu_dir):
        for file_ in files:

            # ignore hidden file
            if os.path.basename(file_).startswith('.'):
                continue

            corpus_reader = get_corpus_reader(
                columntypes=(
                    ConllCorpusReader.IGNORE,
                    ConllCorpusReader.WORDS,
                    ConllCorpusReader.POS,
                    ConllCorpusReader.NE,
                    ConllCorpusReader.IGNORE
                ),
                root=root,
                fileids=[file_]
            )

            output_file = os.path.splitext(file_)[0] + '.txt'

            with open(os.path.join(token_dir, output_file), 'w') as fd:
                for word_tag_pair_list in corpus_reader.tagged_sents():
                    for word, tag in word_tag_pair_list:
                        if tag not in encoder_cache:
                            encoder_cache[tag] = BILUOEncoderDecoder(tag)

                        encoder = encoder_cache[tag]
                        coding = encoder.encode(word)

                        word_coding_pair_list = zip(word, coding)

                        for word_coding_pair in word_coding_pair_list:
                            fd.write(delimit.join(word_coding_pair) + "\n")
                    fd.write('\n')


if __name__ == "__main__":
    main()
