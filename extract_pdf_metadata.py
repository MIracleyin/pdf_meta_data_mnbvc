import argparse
from datetime import datetime
import pikepdf
import sys
from pathlib import Path
import jsonlines
from tqdm import tqdm

# get the target pdf file from the command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pdf_dir",
        type=str,
        default='./data',
        required=True,
        help="The directory containing the PDF files",
    )
    parser.add_argument(
        "--jsonl_path",
        type=str,
        default='./output/pdf_meta_info.jsonl'
    )
    return parser.parse_args()

def write_meta_info_to_jsonl(pdf_dir, jsonl_path):
    pdf_dir = Path(pdf_dir)
    with jsonlines.open(jsonl_path, 'w') as w:
        for pdf_file in tqdm(pdf_dir.glob("*.pdf")):
            # read the pdf file
            pdfinfo = dict()
            pdfinfo.update({"filename": str(pdf_file)})
            try:
                pdf = pikepdf.Pdf.open(pdf_file)
                docinfo = pdf.docinfo
                for key, value in docinfo.items():
                    pdfinfo.update({key: str(value)})
            except Exception as e:
                pdfinfo.update({'error': str(e)})
            # pdf_meta_info.append(docinfo)
            w.write(pdfinfo)

def main():
    # 主函数
    args = parse_arguments()

    write_meta_info_to_jsonl(args.pdf_dir, args.jsonl_path)

if __name__ == "__main__":
    main()

    