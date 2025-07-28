# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>｣

import csv
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox

app = QApplication([])

# ﾌｧｲﾙ選択ﾀﾞｲｱﾛｸﾞを作成
dialog = QFileDialog()
dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
dialog.setNameFilter("CSV (*.csv)")
if dialog.exec() == QFileDialog.DialogCode.Accepted:
    filename = dialog.selectedFiles()[0]

    # CSVﾌｧｲﾙを読み込む
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # 'Lifetime Amount'が0の行を除外
    data = [row for row in data if float(row['Lifetime Amount']) > 0]

    # 'Lifetime Amount'と'Patronage Since Date'に基づいて並べ替え
    data.sort(key=lambda row: (-float(row['Lifetime Amount']), datetime.strptime(row['Patronage Since Date'], '%Y-%m-%d %H:%M:%S')))

    # 並べ替えた結果から名前を取得
    names = [row['Name'] for row in data]

    # 名前をQMessageBoxに表示
    msgBox = QMessageBox()
    msgBox.setText("\n".join(names))
    msgBox.exec()

    # ﾕｰｻﾞｰがﾎﾞﾀﾝを押すと､名前をｸﾘｯﾌﾟﾎﾞｰﾄﾞにｺﾋﾟｰ
    clipboard = QApplication.clipboard()
    clipboard.setText("\n".join(names))