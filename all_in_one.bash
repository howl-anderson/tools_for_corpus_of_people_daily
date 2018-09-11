#!/usr/bin/env bash

python ./convert_encoding.py

python ./parse_data.py

python ./split_data.py

python ./conll_to_crfpp.py

python ./conll_to_char_crfpp.py

python ./split_data_to_token.py

python ./split_token_to_token_conll.py