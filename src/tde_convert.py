#!/usr/bin/env python3

import argparse
import json

from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(description="NTCIR-17 UFO Table Data Extraction サブタスクのtrainデータの形式から、提出用のファイル形式に変換します")
    parser.add_argument("-i", "--input_files", nargs="+", type=str, required=True, help="入力ファイル名を指定します")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="出力ファイル名を指定します")
    args = parser.parse_args()

    result = {}

    for input_file in args.input_files:
        with open(input_file, "r", encoding="utf-8-sig") as fp:
            html_data = fp.read()

        soup = BeautifulSoup(html_data, "html.parser")

        result.update({
            tag["data-ufo-tde-cell-id"]: tag["data-ufo-tde-cell-type"]
            for tag in soup.find_all(attrs={"data-ufo-tde-cell-id": True, "data-ufo-tde-cell-type": True})
        })

    with open(args.output_file, "w", encoding="utf-8") as fp:
        json.dump(result, fp, indent=2)
        fp.write("\n")


if __name__ == "__main__":
    main()
