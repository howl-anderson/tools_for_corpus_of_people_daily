import os

from tokenizer_tools.transform.plain_token_to_conll import plain_token_to_conll
import utils


current_dir = os.path.dirname(os.path.abspath(__file__))

conllu_dir = os.path.join(current_dir, 'data/split_token')
utils.create_if_dir_not_exists(conllu_dir)

token_dir = os.path.join(current_dir, 'data/token_conll')
utils.create_if_dir_not_exists(token_dir)


def main():
    for root, dirs, files in os.walk(conllu_dir):
        for file_ in files:

            # ignore hidden file
            if os.path.basename(file_).startswith('.'):
                continue

            input_file = os.path.join(root, file_)

            file_name = os.path.splitext(file_)[0] + '.txt'
            output_file = os.path.join(token_dir, file_name)

            plain_token_to_conll(input_file, output_file)


if __name__ == "__main__":
    main()
