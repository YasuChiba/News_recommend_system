# -*- coding: utf-8 -*-

import MeCab
from db_accessor import clsDbAccessor
import fasttext as ft


mecab = MeCab.Tagger ("-Owakati")

data_file_path = "/root/classification/tmp_data.txt"
model_file_path = "/root/classification/tmp_model.bin"

def process_data_for_train():
    dba = clsDbAccessor()
    data = dba.get_joined_train_data()
    
    result_list = []
    for d in data:
        text = d["og_description"]
        if text is None:
            text = d["text"]

        text = mecab.parse (text)
        text = text.replace('\u3000', '')

        categories = d["categories"]
        
        label = ""
        for category in categories:
            label += "__label__" + category + " " 

        result_list.append((label + ' '+text).rstrip("\n"))

    return result_list

def train():

    data = process_data_for_train()
    f = open(data_file_path, 'w',encoding="utf-8")
    for x in data:
        f.write(x + "\n")
    model = ft.train_supervised(data_file_path, lr=0.05, epoch=2000, dim=200)
    model.save_model(model_file_path)

    return model

def predict(model = None):
    #tmp_text = "　「ただで土を入れて水田にしてあげる」。そんな言葉を信じたら1年後には高さ10メートルの建設残土の山が。県も市も警察も頼りにならず、撤去を求める裁判に勝訴したものの変わらない。自腹で撤去したら最低77…"
    #tmp_text = "新型 コロナ ウイルス の 国内 感染 者 は 6 日 、 午後 1 1 時 半 現在 で 新た に 1 4 8 4 人 確認 さ れ 、 3 日 続け て 1 千 人 を 超え た 。 神奈川 県 、 千葉 県 、 山梨 県 、 大阪 府 、 佐賀 県 で 1 日 あたり の 最多 を 更新 し た 。 大 都市 と その 周辺 で 感 … "
    #tmp_text = mecab.parse (tmp_text).replace("\n", "")


    dba = clsDbAccessor()
    data = dba.get_scrape_data()
    data_list = []
    for d in data:
        text = d["og_description"]
        if text is None:
            text = d["text"]

        text = mecab.parse (text).replace("\n", "")
        text = text.replace('\u3000', '')
        data_list.append((text.rstrip("\n"), d["id"]))


    if model is None:
        model = ft.load_model(model_file_path)
    
    for i in range(len(data_list)):
        scrape_id = data_list[i][1]
        res = model.predict(data_list[i][0], k = len(model.labels))

        for j in range(len(res[0])):
            if res[1][j] > (1/len(res[0])) + 0.1:
                category_id = int(res[0][j].replace("__label__", ""))
                probability = round(res[1][j],3)
                dba.insert_predicted_data(scrape_id, category_id, probability)

def start():
    model = train()
    predict(model = model)

if __name__ == '__main__':
    start()
