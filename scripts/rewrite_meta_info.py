import jsonlines
from tqdm import tqdm


save_meta_info = ['file_name',
 'file_size',
 '/Author',
 '/CreationDate',
 '/Creator',
 '/Producer',
 '/Title',
 '/ModDate',
 '/Keywords']

with jsonlines.open("output/result.jsonl", "r") as reader:
    with jsonlines.open("output/all_metainfo_230916.jsonl", "w") as writer:
        for pdfinfo in tqdm(reader):
            newinfo = {}
            otherinfo = ""
            count = 0
            for k, v in pdfinfo.items():
                count += 1
                if k in save_meta_info:
                    newinfo.update({
                        k: v
                    })
                else:
                    otherinfo += f"{k}:{v};"
            newinfo.update({"others": otherinfo})
            newinfo.update({"num_meta": count})
            writer.write(newinfo)
            del newinfo