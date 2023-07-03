#!/usr/bin/env python3

import argparse
import json
import traceback
from pathlib import Path

import sklearn.metrics

GS_FILENAME = "UFO_TDE_v20230703-Gold.json"


class EvaluationException(Exception):
    pass


def main():
    gs_data = (Path(__file__).parents[0] / GS_FILENAME)

    parser = argparse.ArgumentParser(description="NTCIR-17 UFO TDE タスクの評価スクリプト")
    parser.add_argument("-f", "--input-file", required=True, help="入力データを指定します")
    parser.add_argument("-g", "--gs-data", required=(not gs_data.exists()), default=gs_data, help="GSデータを指定します")
    args = parser.parse_args()

    labels = ["header", "attribute", "data", "metadata"]

    # GS読み込み
    with open(args.gs_data, "r", encoding="utf-8-sig") as f:
        gss = json.load(f)
        assert all(v in labels for v in gss.values())

    # 評価対象読み込み
    with open(args.input_file, "r", encoding="utf-8-sig") as f:
        try:
            targets = json.load(f)
        except Exception:
            raise EvaluationException("JSON ファイルのデコードに失敗しました。データを確認してください。")

    # データの確認
    for k, v in gss.items():
        if k not in targets:
            raise EvaluationException(f"入力データで回答されていない項目があります（ID: {k}）。データを確認してください。")
    for k, v in targets.items():
        if k not in gss:
            raise EvaluationException(f"入力データに不明な ID があります（ID: {k}）。データを確認してください。")
        if v not in labels:
            raise EvaluationException(f"入力データの値が不正です（ID: {k}）。データを確認してください。")

    # データの作成
    y_true = []
    y_pred = []
    for k in sorted(gss.keys()):
        y_true.append(gss[k])
        y_pred.append(targets[k])

    result_accuracy = sklearn.metrics.accuracy_score(y_true, y_pred)
    result_f1 = sklearn.metrics.f1_score(y_true, y_pred, average="micro", labels=labels)

    # 出力
    return json.dumps({
        "status": "success",
        "scores": [result_accuracy, result_f1],
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    try:
        print(main())
    except EvaluationException as e:
        print(json.dumps({"status": "failed", "message": e.args[0]}, ensure_ascii=False))
        traceback.print_exc()
    except Exception:
        print(json.dumps({"status": "failed"}, ensure_ascii=False))
        traceback.print_exc()
