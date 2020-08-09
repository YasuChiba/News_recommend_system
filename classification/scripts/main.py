# -*- coding: utf-8 -*-

import MeCab
from db_accessor import clsDbAccessor
import fasttext as ft


mecab = MeCab.Tagger ("-Owakati")

data_file_path = "/root/classification/tmp_data.txt"
model_file_path = "/root/classification/tmp_model.bin"

def process_data():
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
    

    data = process_data()
    f = open(data_file_path, 'w',encoding="utf-8")
    for x in data:
        
        f.write(x + "\n")

    model = ft.train_supervised(data_file_path)
    model.save_model(model_file_path)

    return model

def predict(model = None):
    tmp_text = "　「ただで土を入れて水田にしてあげる」。そんな言葉を信じたら1年後には高さ10メートルの建設残土の山が。県も市も警察も頼りにならず、撤去を求める裁判に勝訴したものの変わらない。自腹で撤去したら最低77…"
   
    tmp_text = mecab.parse (tmp_text).replace("\n", "")

    if model is None:
        model = ft.load_model(model_file_path)
    
    res = model.predict(tmp_text, k = len(model.labels))
    print(res)


    pass
if __name__ == '__main__':
    model = train()
    #predict(model = model)

    #predict()