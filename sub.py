import tkinter as tk
import tkinter.filedialog
import datetime as dt
import re
import os


def convertdate(line:str, start:int, dateitems:list):
    hbcritems = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', line)
    #hbcritems = line.split(',')
    startdatestr = hbcritems[start]
    #エラーチェック
    #startがdateitemsに含まれている場合は何もしない
    if start in dateitems:
        print(f'Error: start index {start} is in dateitems')
        return
    #短すぎる
    if len(hbcritems) < 2:
        print(f'Error: line is too short: {line}')
        return
    #startdaetが空文字列または99999999の場合は何もしない
    if startdatestr in ['', '99999999', '77777777', '88888888']:
#        print(f'Error: The start date {startdate} is empty or invalid. Cannot process line: {line}')
        return
    #エラーチェック終了
    startdate = dt.datetime.strptime(startdatestr, '%Y%m%d')
    #本当は、startdatestrの形式が正しいかどうかもチェックしたいが、ここでは省略
    for i in dateitems:
        #error: hbcritems[i]が空文字列または99999999の場合はエラー
        if hbcritems[i] == '' or int(hbcritems[i][-2:]) > 31:
#            print(f'Warning: {hbcritems[i]} has ambiguous date')
            continue
        try:
            enddate = dt.datetime.strptime(hbcritems[i], '%Y%m%d')
        except:
            return (f"エラー!: {hbcritems[i]} in line {i}")

        #日数を計算
        daycnt = (enddate - startdate).days
        hbcritems[start] = hbcritems[start][:-2] + '00'  # startdateの月日を00にする
        hbcritems[i] = str(daycnt)
    return ','.join(hbcritems)

def fileconvert(source:str, start:str, dateitems:list, outfile:str):
#ファイルの処理
    with open(source, 'r', encoding='cp932') as f:
        i=0
        with open(outfile, 'w', encoding='cp932') as destination:
            with open(os.path.dirname(outfile) + '/log.txt', 'w', encoding='cp932') as log:
                for line in f:
                    i += 1
                    if i==1:
                        destination.write(line)
                        continue
                    out = convertdate(line, start, dateitems)
                    if out is None:
                        log.write(f'Error: line {i} is has a problem: {line}')
                        continue
                    destination.write(out)
    return

def create_list(firstline:list):
    # 日付項目のインデックスをリストで返す
    # startは診断日のインデックス
    # dateitemsは日付項目のインデックスのリスト
    dateitems = [22, 23, 24, 46, 50, 54, 59, 63, 67, 77, 78]
    datelists = []
    start = 0
    for i in range(len(firstline)):
        if firstline[i] == '診断日':
            start= i 
            continue
        if firstline[i] in ['当該腫瘍初診日','他施設診断日','自施設診断日','外科的治療の施行日（自施設）','鏡視下治療の施行日（自施設）','内視鏡的治療の施行日（自施設）','放射線療法の施行日（自施設）','化学療法の施行日（自施設）','内分泌療法の施行日（自施設）','生存最終確認日','死亡日']:
            datelists.append(i)
    if start == 0:
        print("Error: '診断日' not found in the first line.")
        return None, None
    return start,datelists


#test = '施設番号,連番,調査指定年,提出項目パターン,病院等の名称,診療録番号,重複番号,カナ氏名,氏名,性別,生年月日,基本情報《テキスト》,診断時郵便番号,診断時都道府県コード,診断時住所,原発部位《局在コード》,原発部位《テキスト》,側性,病理診断《形態コード》,病理診断《テキスト》,診断根拠,当該腫瘍初診日,他施設診断日,自施設診断日,診断日,診断施設,治療施設,症例区分,来院経路,発見経緯,病名告知の有無,ステージ（治療前・ＵＩＣＣ）,ＴＮＭ分類（ＵＩＣＣ）Ｔ分類,ＴＮＭ分類（ＵＩＣＣ）Ｎ分類,ＴＮＭ分類（ＵＩＣＣ）Ｍ分類,ＴＮＭ分類（ＵＩＣＣ）付加因子,ステージ（術後病理学的・ＵＩＣＣ）,ｐＴＮＭ分類（ＵＩＣＣ）ｐＴ分類,ｐＴＮＭ分類（ＵＩＣＣ）ｐＮ分類,ｐＴＮＭ分類（ＵＩＣＣ）ｐＭ分類,ＴＮＭ分類（ＵＩＣＣ）ｐ付加因子,肝癌の病期（治療前・取扱い規約）,進展度（治療前）,進展度（術後病理学的）,腫瘍情報《テキスト》,外科的治療の有無,外科的治療の施行日（自施設）,外科的治療（他施設）《自施設初回治療開始前》,外科的治療（他施設）《自施設初回治療開始後》,鏡視下治療の有無,鏡視下治療の施行日（自施設）,鏡視下治療（他施設）《自施設初回治療開始前》,鏡視下治療（他施設）《自施設初回治療開始後》,内視鏡的治療の有無,内視鏡的治療の施行日（自施設）,内視鏡的治療（他施設）《自施設初回治療開始前》,内視鏡的治療（他施設）《自施設初回治療開始後》,外科的・鏡視下・内視鏡的治療の範囲,放射線療法の有無,放射線療法の施行日（自施設）,放射線療法（他施設）《自施設初回治療開始前》,放射線療法（他施設）《自施設初回治療開始後》,化学療法の有無,化学療法の施行日（自施設）,化学療法（他施設）《自施設初回治療開始前》,化学療法（他施設）《自施設初回治療開始後》,内分泌療法の有無,内分泌療法の施行日（自施設）,内分泌療法（他施設）《自施設初回治療開始前》,内分泌療法（他施設）《自施設初回治療開始後》,その他の治療の有無,その他の治療（他施設）《自施設初回治療開始前》,その他の治療（他施設）《自施設初回治療開始後》,経過観察の選択の有無（自施設）,症状緩和的な治療の有無（自施設）,初回治療情報《テキスト》,全般情報《テキスト》,生存最終確認日,死亡日,生存状況,生存状況調査方法,追跡期間,データの調査研究利用に関する意思表示,利用に関する最終意思表示日,利用に関するその他の情報《テキスト》,調査研究の連絡に関する意思表示,連絡に関する最終意思表示日,連絡に関するその他の情報《テキスト》,紹介元施設,紹介先施設'.split(',')
#a,b = create_list(test)
#print(a,b)