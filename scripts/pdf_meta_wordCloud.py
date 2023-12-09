# -*- coding: utf-8 -*-:
import wordcloud
import pandas as pd
import matplotlib.pyplot as plt
import jsonlines
import argparse
from tqdm import tqdm


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source_path",
        type=str,
        default='../output/result.jsonl',
        help="This is original jsonl file",
    )
    parser.add_argument(
        "--new_path",
        type=str,
        default='../output/new_result.jsonl',
        help="This is new jsonl file",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.01,
        help="This is the reorganized metadata information file",
    )
    parser.add_argument(
        "--figure_path",
        type=str,
        default="../output/wordcloud.png",
        help="This is the figure path",
    )
    return parser.parse_args()


'''
重置jsonl文件中的元数据信息，只保留指定save_meta_info的key元数据信息
'''
def check_data(source_path, new_path, save_meta_info):
    with jsonlines.open(source_path, "r") as reader:
        with jsonlines.open(new_path, "w") as writer:
            for pdfinfo in tqdm(reader):
                newinfo = {}
                for k, v in pdfinfo.items():
                    if k in save_meta_info:
                        newinfo.update({
                            k: v
                        })
                writer.write(newinfo)
                del newinfo
        writer.close()
    reader.close()


def process_data(source_path, new_path, threshold):
    df = pd.read_json(source_path, orient='records', lines=True)
    non_null_count = df.count()
    ratio = non_null_count / len(df)  # 每种元信息的概率分布
    current_radio = ratio[ratio > threshold]  # 选取概率大于threshold的元信息
    save_meta_info = [k for k in current_radio.index]  # 选取的元信息
    check_data(source_path, new_path, save_meta_info)  # 重置元数据信息，保存新数据至new_path

    # 重新计算新数据的概率分布
    new_df = pd.read_json(new_path, orient='records', lines=True)
    new_non_null_count = new_df.count()
    return new_non_null_count / len(new_df)


# 生成词云
def create_wordcloud(source_path, new_path, threshold, figure_path):
    wc = wordcloud.WordCloud(background_color='white',
                             width=1000,
                             height=800,
                             max_words=500)
    # 从单词和频率创建词云
    counts = process_data(source_path, new_path, threshold)
    wc.generate_from_frequencies(counts)
    # wc.generate(txt)  # 根据文本生成词云

    #  显示词云图片
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig(figure_path, dpi=500)
    plt.show()


def main():
    # 主函数
    args = parse_arguments()
    create_wordcloud(args.source_path, args.new_path, args.threshold, args.figure_path)


if __name__ == '__main__':
    main()
