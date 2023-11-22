# -*- coding: utf-8 -*-:
import pandas as pd
import jsonlines
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--excel_path",
        type=str,
        default='../data/metadata.xlsx',
        help="This is original metadata.xlsx file",
    )
    parser.add_argument(
        "--jsonl_path",
        type=str,
        default='../output/all_metadata_231118.jsonl',
        help="This is new transferred jsonl  file",
    )
    return parser.parse_args()


def xlxs_process(excel_path, jsonl_path):
    df = pd.read_excel(excel_path, sheet_name=0)
    col = list(df.columns)

    with jsonlines.open(jsonl_path, 'w') as w:
        for i in range(0, len(df)):
            meta_dict = {}
            for j in range(1, len(df.columns)):
                if str(df.iloc[i][col[j]]) != '' and str(df.iloc[i][col[j]]) != 'nan':
                    meta_dict.update({str(df.columns[j]): str(df.iloc[i][col[j]])})
            w.write(meta_dict)
    w.close()


if __name__ == '__main__':
    # 主函数(必须指定文件的参数)
    args = parse_arguments()
    xlxs_process(args.excel_path, args.jsonl_path)