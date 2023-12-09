# -*- coding: utf-8 -*-:
import json
import jsonlines
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no_transfer_jsonl_path",
        type=str,
        default='./output/all_metainfo_230916.jsonl',
        help="This is not a transferred jsonl file",
    )
    parser.add_argument(
        "--transfer_jsonl_path",
        type=str,
        default='./output/new.jsonl',
        help="This is a transferred jsonl file",
    )
    return parser.parse_args()

def remove_empty_values(data):
    new_data = {}
    for k, v in data.items():
        if v != "" and v != "nan":
            new_data.update({"" + str(k): "" + str(v)})
    return new_data

def clean_jsonl_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf8') as f_in, jsonlines.open(output_file, 'w') as f_out:
        for line in f_in:
            json_data = json.loads(line)
            cleaned_data = remove_empty_values(json_data) # 删除值为空字符串的键值对
            f_out.write(cleaned_data)
    f_in.close()
    f_out.close()


if __name__ == '__main__':
    args = parse_arguments()
    clean_jsonl_file(args.no_transfer_jsonl_path, args.transfer_jsonl_path)