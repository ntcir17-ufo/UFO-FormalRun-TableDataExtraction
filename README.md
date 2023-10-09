# NTCIR-17 UFO Table Data Extraction サブタスク（Formal Run）

## 更新情報

- (2023/10/9) Goldデータの公開
- (2023/7/3) リポジトリの公開

## タスク設定

以下をご参照ください。
https://sites.google.com/view/ntcir17-ufo/subtasks/table-data-extraction

## 配布ファイル

このリポジトリには以下のファイルが含まれます。

- `train/*.tde_annotated.html`
    - 各企業が発行した有価証券報告書に情報を追加したもので、train データとして使用します。
- `test/*.tde_test.html`
    - 各企業が発行した有価証券報告書に情報を追加したもので、test データとして使用します。
- `src/tde_baseline.py`
    - サンプルの推論スクリプトです。
    - 各テーブルの 1 行目を header、2 行目以降の 1 列目を attribute、それ以外を data と出力します。
- `src/tde_eval.py`
    - 評価スクリプトです。Accuracy と、4 つの F1-score のマイクロ平均を出力します。
    - 引数として、`-g [Goldデータ.json] -i [システムの出力.json]` を取ります。
- `src/tde_convert.py`
    - train データの形式から、提出用のファイル形式に変換します。
    - train データの一部を dev データとして使用する場合の、評価スクリプトに与える gold データを作成するために使用してください。
- `gold/UFO_TDE_v20230703-Gold.json`
    - 正解データです。

## 入力ファイル形式

各企業が発行した有価証券報告書（HTML 形式）に、必要なアノテーションを行ったものを利用します。

### train データ

`*.tde_annotated.html` は、各企業が発行した有価証券報告書に、以下の修正を加えたものです。

- `th` タグ、`td` タグ（テキストが空でないものに限る）に `data-ufo-tde-cell-id` 属性および `data-ufo-tde-cell-type` 属性を追加。
    - `data-ufo-tde-cell-type` はアノテータにより選択された `header`/`attribute`/`data`/`metadata` のいずれかの値を持ちます。
    - `data-ufo-tde-cell-id` はセルを一意に識別する文字列で、`[書類管理番号]-[ファイル名]-tab[テーブル連番]-r[行]c[列]` の形式です。
    - アノテータが分類できないと判断したセルが 1 つでも含まれているテーブルは、その全セルに属性を追加していません。
- `h1` から `h6` タグ、`p` タグに `data-ufo-tde-paragraph-type` 属性を追加。
    - `data-ufo-tde-paragraph-type` はアノテータにより選択された `header`/`attribute`/`data`/`metadata` のいずれかの値を持ちます。
    - 指す先のテーブルがどれかはアノテートされていません。
    - 分類できなかったセルを含む（すなわち `data-ufo-tde-cell-type` 属性を持たない）テーブルに関連する情報である場合もあります。
- `head` 要素内に出典のコメントと UFO TDE のための `style` 要素を追加。
    - 上記の `data-ufo-tde-cell-type`、`data-ufo-tde-paragraph-type` にあわせてセルまたは段落等の背景色を変更するものです。

### test データ

`*.tde_test.html` は、`*.tde_annotated.html` と同一の形式ですが、`data-ufo-tde-cell-type` と `style` 要素が追加されていません。

## 出力ファイル形式

- JSON で `{"セルID": "クラス", ...}` 形式のオブジェクト（dict）とします。
    - セル ID は test データに含まれる `data-ufo-tde-cell-id` の値、クラスは `header`/`attribute`/`data`/`metadata` のいずれかの値です。
    - test データに含まれるすべての `data-ufo-tde-cell-id` 属性を持つセルについて回答する必要があります。

## 出典

- `train` ならびに `test` ディレクトリ内のファイルは、EDINET 閲覧（提出）サイト（※）をもとに NTCIR-17 UFO タスクオーガナイザが作成したものです。
    - （※）例えば書類管理番号が `S100ISN0` の場合、当該ページの URL は `https://disclosure2.edinet-fsa.go.jp/WZEK0040.aspx?S100ISN0` となります。書類管理番号は、`train`/`test` ディレクトリ内の各ファイル名の先頭 8 文字です。
    - 各「提出本文書」の「第一部」を使用しています。
