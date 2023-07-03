#!/usr/bin/env python3

import argparse
import collections
import json
import re

from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(description="NTCIR-17 UFO Table Data Extraction サブタスクのサンプルの推論スクリプト")
    parser.add_argument("-i", "--input_files", nargs="+", type=str, required=True, help="入力ファイル名を指定します")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="出力ファイル名を指定します")
    args = parser.parse_args()

    result = {}

    for input_file in args.input_files:
        with open(input_file, "r", encoding="utf-8-sig") as fp:
            html_data = fp.read()

        soup = BeautifulSoup(html_data, "html.parser")

        for table in soup.find_all("table"):
            # 各テーブルの1行目をheader、2行目以降の1列目をattribute、それ以外をdataと出力します。
            if not table.find(attrs={"data-ufo-tde-cell-id": True}):
                continue

            rows = collections.defaultdict(list)
            cols = collections.defaultdict(list)

            for cell in table.find_all(attrs={"data-ufo-tde-cell-id": True}):
                # print(cell.text.strip())

                cell_id = cell["data-ufo-tde-cell-id"]
                mo = re.match(r"(?P<docid>[^-]+)-(?P<fileid>[^-]+)-tab(?P<table>\d+)-r(?P<row>\d+)c(?P<column>\d+)", cell_id)
                if not mo:
                    raise ValueError(f"Invalid cell ID: {cell_id}")
                rows[int(mo.group("row"))].append(cell_id)
                cols[int(mo.group("column"))].append(cell_id)

                # （2行目以降の2列目以降を）data
                if cell_id in result:
                    raise ValueError(f"Duplicate cell ID: {cell_id}")
                result[cell_id] = "data"

            min_col = min(cols.keys())
            for cell_id in cols[min_col]:
                # （2行目以降の）1列目をattribute
                result[cell_id] = "attribute"

            min_row = min(rows.keys())
            for cell_id in rows[min_row]:
                # 1行目をheader
                result[cell_id] = "header"

    with open(args.output_file, "w", encoding="utf-8") as fp:
        json.dump(result, fp, indent=2)
        fp.write("\n")


if __name__ == "__main__":
    main()
