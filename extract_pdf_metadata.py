import argparse
from datetime import datetime
import pikepdf
import sys
from pathlib import Path
import jsonlines
from tqdm import tqdm
from loguru import logger

# get the target pdf file from the command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pdf_dir",
        type=str,
        default='./data',
        help="The directory containing the PDF files",
    )
    parser.add_argument(
        "--jsonl_path",
        type=str,
        default='./output/pdf_meta_info.jsonl',
        help="The result file path",
    )
    parser.add_argument(
        "--log_dir",
        type=str,
        default="./logs",
        help="The directory containing the log files",
    )
    return parser.parse_args()

def write_meta_info_to_jsonl(pdf_dir, jsonl_path):
    pdf_dir = Path(pdf_dir)
    readable, faild = 0, 0
    with jsonlines.open(jsonl_path, 'w') as w:
        for pdf_file in tqdm(pdf_dir.iterdir()):
            pdf_file = pdf_file.with_suffix(pdf_file.suffix.lower())
            if pdf_file.suffix != '.pdf':
                continue
            # read the pdf file and get simple meta info
            pdfinfo = dict()
            pdfinfo.update({
                "file_name": str(pdf_file),
                "file_size": str(pdf_file.stat().st_size)
            })
            try:
                pdf = pikepdf.Pdf.open(pdf_file)
                docinfo = pdf.docinfo
                for key, value in docinfo.items():
                    pdfinfo.update({key: str(value)})
                if len(pdfinfo.items()) == 2:
                    logger.warning(f"{pdf_file} Don't have any meta data")
                readable += 1
            except Exception as e:
                pdfinfo.update({'error': str(e)})
                logger.error(f"Error while load PDF {pdf_file}: {e}")
                faild += 1
            # pdf_meta_info.append(docinfo)
            w.write(pdfinfo)
            
    return readable, faild


def main():
    # 主函数
    args = parse_arguments()

    # 获取时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # 配置logger
    logger.remove(handler_id=None) # don't log in console
    logger.add(f"{args.log_dir}/pdf_meta_info_{timestamp}.log", rotation="500 MB") 

    r, f = write_meta_info_to_jsonl(args.pdf_dir, args.jsonl_path)
    logger.info(f"{args.pdf_dir}: all {r}, error {f}")

if __name__ == "__main__":
    main()

    