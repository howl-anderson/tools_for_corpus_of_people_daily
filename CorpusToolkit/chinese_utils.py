"""
double-byte: 全角
single-byte: 半角
"""
import copy
import re

double_byte_set_continue = [chr(i) for i in range(0xFF01, 0xFF5E+1)]

double_byte_set_special = [chr(0x3000)]

all_double_byte_chars_list = double_byte_set_continue + double_byte_set_special

double_byte_set_continue_to_single_byte_mapping = {k: chr(ord(k) - 0xfee0) for k in double_byte_set_continue}
double_byte_set_special_to_single_byte_mapping = {chr(0x3000): chr(0x20)}

all_double_byte_string = "".join(all_double_byte_chars_list)

double_byte_to_single_byte_mapping = copy.deepcopy(double_byte_set_continue_to_single_byte_mapping)
double_byte_to_single_byte_mapping.update(double_byte_set_special_to_single_byte_mapping)


def double_byte_to_single_byte(message):
    return re.sub(
        r'([{}])'.format("".join(all_double_byte_string)),
        lambda match_obj: double_byte_to_single_byte_mapping[match_obj.group(0)],
        message
    )


if __name__ == "__main__":
    result = double_byte_to_single_byte('张三，是１个帅哥。')
    print(result)
