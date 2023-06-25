# LineShadowGen
LineShadowGenは線画から陰影をAIによって生成するソフトです。<br>
![新規キャンバス1](https://github.com/tori29umai0123/LineShadowGen/assets/72191117/77f49190-871b-4e1b-9935-134de2c480e4)
https://note.com/tori29umai/n/ne5fc338ae614<br>

# Install
①以下のColabのリンクをクリックしてください<br>
 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tori29umai0123/LineShadowGen/blob/master/LineShadowGen.ipynb)

②Colabのメニューから、『ランタイム』→『ランタイムのタイプを変更』→以下のように設定
![2](https://github.com/tori29umai0123/LineShadowGen/assets/72191117/f8cfa7ac-ed29-4353-bb0c-dd55a1a43137)

②Colabのメニューから、『すべてのセルを実行』（5分位かかります）
![3](https://github.com/tori29umai0123/LineShadowGen/assets/72191117/2eb56121-b061-4f26-9503-e078269fd27f)

④public URLをクリック

# Local Install
Python3.10.Xがインストールされている環境前提です。（Python 3.10.8で起動確認済み）<br>
①適当なディレクトリでリポジトリをgit clone<br>
```
cd C:/
git clone https://github.com/tori29umai0123/LineShadowGen.git<br>
```
②install.ps1を右クリック→PowerShellで実行（5分位かかります）<br>
③LineShadowGen_run.batをダブルクリックすると自動でブラウザが立ち上がる。<br>

# Local Upadate
ソフトの更新はLineShadowGen_update.batをダブルクリックする。<br>
更新の有無を聞かれたら『y』と入力。<br>
モデルの更新はLineShadowGen_update_model.batをダブルクリックする。<br>
モデルのアップデートを聞かれたら『y』と入力。5分位かかります。<br>

# Local Uninstall
フォルダごと削除してください

# Usage
LineArtImage：線画を設定<br>
Enter max_size：画像の長辺の最大サイズを入力（大きければ大きいほどPCスペックが必要です）<br>
prompt：画像の内容のタグ<br>
PromptGenerate：タグの自動分析<br>
（Inpaintタブの場合）<br>
MaskImage：マスク画像を設定<br>
MaskGenerate：マスクの自動生成<br>
ShadowGenerate：陰影生成ボタン
