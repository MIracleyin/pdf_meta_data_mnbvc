# PDF 元信息提取

该项目是 MNBVC 计划的一部分，旨在提供一个提取 PDF 元信息工具。该工具分为元信息提取与元信息分析两个部分。

## 项目日志
1. 初始化
2. 支持各类 pdf 后缀；打印读取错误日志，打印文件处理数量日志

## 项目目标

对当前全量 pdf 进行统计分析，指定合适的分类策略，支持后续 pdf 解析

## 使用方法

### 元信息提取
建议将多个文件夹软链接到该目录下，然后使用脚本分别运行，提取结果

```bash
ln -s /path/to/real_pdf_path ./pdf_bucket_name
python extract_pdf_metadata.py --pdf_dir /path/to/pdf_dir --jsonl_path /path/to/meta_info.jsonl
```

### 元信息分析

目前仅完成统计部分
