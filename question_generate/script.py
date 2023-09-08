from google.colab import drive
drive.mount('/content/drive')

import torch
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from gensim.utils import simple_preprocess
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix

import torch.nn as nn
from torch.optim import AdamW
from torch.utils.data import Dataset, DataLoader

from transformers import get_linear_schedule_with_warmup, AutoTokenizer, AutoModel, logging

import warnings
warnings.filterwarnings("ignore")

logging.set_verbosity_error()

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

import py_vncorenlp

py_vncorenlp.download_model(save_dir='/content/')
rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='/content/')

model_checkpoint = "vinai/phobert-base"
tokenizer_intent = AutoTokenizer.from_pretrained(model_checkpoint, use_fast=False)

class SentimentClassifier(nn.Module):
    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = AutoModel.from_pretrained(model_checkpoint)
        self.drop = nn.Dropout(p=0.3)
        self.fc = nn.Linear(self.bert.config.hidden_size, n_classes)
        nn.init.normal_(self.fc.weight, std=0.02)
        nn.init.normal_(self.fc.bias, 0)

    def forward(self, input_ids, attention_mask):
        last_hidden_state, output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            return_dict=False # Dropout will errors if without this
        )

        x = self.drop(output)
        x = self.fc(x)
        return x
    
label_intent = ['groupMonthOverall',
 'oneKPI',
 'crossView',
 'ChildInferenceMom',
 'viewStat',
 'groupMonthDetail',
 'viewDetermineTrend',
 'viewPredict',
 'viewExplainResult',
 'viewOneKPIStat',
 'viewCtyDescribe',
 'viewOneGroupKPIStat'
]

l2i_intent = {ele.split('.')[0] : i for i,ele in enumerate(label_intent)}
i2l_intent = {i : ele.split('.')[0] for i,ele in enumerate(label_intent)}

model_intent = SentimentClassifier(n_classes=13)
model_intent.to(device)
model_intent.load_state_dict(torch.load(f'/content/drive/MyDrive/largeProject/code/predictIntent/phobert_fold_latest.pth'))

def infer_intent(text, max_len=32, top_k=3, verbose=True):
    model_intent.eval()
    text = rdrsegmenter.word_segment(text)[0]
    print(text)
    encoded_review = tokenizer_intent.encode_plus(
        text,
        max_length=max_len,
        truncation=True,
        add_special_tokens=True,
        padding='max_length',
        return_attention_mask=True,
        return_token_type_ids=False,
        return_tensors='pt',
    )

    input_ids = encoded_review['input_ids'].to(device)
    attention_mask = encoded_review['attention_mask'].to(device)

    output = model_intent(input_ids, attention_mask)
    # print(output)
    topk_output = torch.topk(output,top_k)[1][0].cpu().numpy()
    # print(topk_output)

    _, y_pred = torch.max(output, dim=1)

    pred = y_pred[0].cpu().numpy()
    if verbose == True:
      print(f'Text: {text}')
      print(f'Sentiment: {i2l_intent[int(pred)]}')

    return i2l_intent[int(pred)],topk_output

from torchcrf import CRF
import transformers

import pickle

with open('/content/drive/MyDrive/largeProject/code/NER/l2i_new.pkl','rb') as f:
  l2i_ner = pickle.load(f)

with open('/content/drive/MyDrive/largeProject/code/NER/i2l_new.pkl','rb') as f:
  i2l_ner = pickle.load(f)
  
import torch.nn.functional as F
log_soft = F.log_softmax

MAX_LEN = 128
tokenizer_ner = transformers.AutoTokenizer.from_pretrained(model_checkpoint, do_lower_case=True)

import torch

class EntityDataset:
    def __init__(self, texts, tags):
        self.texts = texts
        self.tags = tags

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, item):
        text = self.texts[item]
        tags = self.tags[item]

        ids = []
        target_tag = []

        for i, s in enumerate(text):
            inputs = tokenizer_ner.encode(s, add_special_tokens=False)
            input_len = len(inputs)
            ids.extend(inputs)
            target_tag.extend([tags[i]] * input_len)

        ids = ids[:MAX_LEN - 2]
        target_tag = target_tag[:MAX_LEN - 2]

        ids = [0] + ids + [2] # : 0, : 2, : 1
        target_tag = [12] + target_tag + [12] # O: 12

        mask = [1] * len(ids) # 1: not masked, 0: masked
        token_type_ids = [0] * len(ids)

        padding_len = MAX_LEN - len(ids)

        ids = ids + ([1] * padding_len) # padding
        mask = mask + ([0] * padding_len) # 1: not masked, 0: masked
        token_type_ids = token_type_ids + ([0] * padding_len)
        target_tag = target_tag + ([12] * padding_len) # O: 12

        return {
            "ids": torch.tensor(ids, dtype=torch.long),
            "mask": torch.tensor(mask, dtype=torch.long),
            "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
            "target_tag": torch.tensor(target_tag, dtype=torch.long),
        }

def loss_fn(output, target, mask, num_labels):
    lfn = torch.nn.CrossEntropyLoss()
    active_loss = mask.view(-1) == 1
    active_logits = output.view(-1, num_labels)
    active_labels = torch.where(
        active_loss,
        target.view(-1),
        torch.tensor(lfn.ignore_index).type_as(target)
    )
    loss = lfn(active_logits, active_labels)
    return loss

class EntityModel(torch.nn.Module):
    def __init__(self, num_tag):
        super(EntityModel, self).__init__()
        self.num_tag = num_tag
        self.bert = transformers.AutoModel.from_pretrained(model_checkpoint,return_dict=False)
        # unfreeze bert
        for param in self.bert.parameters():
            param.requires_grad = False
        self.bert_drop = torch.nn.Dropout(0.3)
        self.out_tag = torch.nn.Linear(768, self.num_tag)
        self.crf = CRF(self.num_tag, batch_first = True)

    def forward_custom(self, ids, mask, token_type_ids, target_tag):
        o, _ = self.bert(ids, attention_mask=mask, token_type_ids=token_type_ids)
        bo_tag = self.bert_drop(o)
        tag = self.out_tag(bo_tag)

        loss = -self.crf(log_soft(tag, 2), target_tag, mask=mask.type(torch.uint8), reduction='mean')
        prediction = self.crf.decode(tag, mask=mask.type(torch.uint8))
        return prediction, loss

    def forward(self, ids, mask, token_type_ids, target_tag):
        o, _ = self.bert(ids, attention_mask=mask, token_type_ids=token_type_ids)
        bo_tag = self.bert_drop(o)
        tag = self.out_tag(bo_tag)
        loss = loss_fn(tag, target_tag, mask, self.num_tag)

        return tag, loss
    
meanDesc = ['mean','trung bình','bình quân','giá trị trung bình','trung bình cộng']
minDesc = ['giá trị nhỏ nhất','min','giá trị bé nhất','giá trị tối thiểu','giá trị thấp nhất']
maxDesc = ['giá trị lớn nhất','max','giá trị tối đa','giá trị bự nhất','giá trị to nhất']
datList = ['đạt','ổn','tốt','hoàn thành','như mong đợi']
koDatList = ['chưa đạt','không đạt','không ổn','chưa tốt','không hoàn thành','chưa hoàn thành','chưa ổn','không ổn','không như mong đợi','chưa như mong đợi']
allList = ['tất cả','toàn bộ','các','đầy đủ','bao gồm']
detailList = ["liệt kê","chi tiết","sâu hơn","tường tận","cặn kẽ","tỉ mỉ","đầy đủ","tường minh","rõ ràng"]
overallList = ["khái quát","tổng quan","tổng thể","cơ bản","tổng hợp","tóm tắt"]
nextMonthList = ["tháng tiếp theo","tháng kế tiếp","tháng sau","tháng <tháng+1>","vào tháng tới"]
seasonList = ["2020 đến"]
year = ["2020","2021","2022","2023"]
quarter = ["Q","q","quý","quý"]

dictList = {
    "<mean>": meanDesc,
    "<min>": minDesc,
    "<max>": maxDesc,
    "<đạt>": datList,
    "<không đạt>": koDatList,
    "<tất cả>": allList,
    "<chi tiết>": detailList,
    "<tổng quan>":overallList,
    "<tháng tiếp theo>":nextMonthList,
    "<mùa>":seasonList,
    "<năm>":year,
    "<quarter>":quarter
}

model_ner = EntityModel(num_tag=len(l2i_ner))
model_ner.load_state_dict(torch.load('/content/drive/MyDrive/largeProject/code/phobert_fold_crf_new.pth'))
model_ner.to(device)

def infer(sentence,verbose=True):
  token_test = rdrsegmenter.word_segment(sentence)[0]
  model_ner.eval()
  segmented_sentence = token_test.replace("( ","(").replace(" )",")") \
                          .replace(" / ","/").replace("/ ","/").replace(" /","/") \
                          .replace("24 h","24h").replace("4 h","4h").replace("2 h","2h") \
                          .replace(" ,",",").replace(" ?","?").replace("10 K","10K") \
                          .replace("1 TTB","1TTB").replace("tỉ","Tỉ").split(' ')

  test_dataset = EntityDataset(texts=[segmented_sentence], tags=[[0] * len(segmented_sentence)])
  # print(segmented_sentence)
  # model = EntityModel(num_tag=num_tag)
  # model.load_state_dict(torch.load(MODEL_PATH))
  # model.to(device)

  with torch.no_grad():
    data = test_dataset[0]
    for k, v in data.items():
      data[k] = v.to(device).unsqueeze(0)
    tag, _ = model_ner.forward_custom(**data)
    tags = []
    for ele in tag[0]:
      tags.append(i2l_ner[ele])

    decoded_sentence = []
    for tokenized_word in test_dataset[0]["ids"]:
      decoded_word = tokenizer_ner.decode([tokenized_word])
      decoded_sentence.append(decoded_word.replace("Tỉ","tỉ"))

    if verbose == True:
      print("{:15} {:5}".format("Word", "Tag"))
      print("="*30)
      for w, t in zip(decoded_sentence, tags):
        if w == "": break
        print("{:15}:{:5}".format(w, t))

    return decoded_sentence[1:len(tags)-1], tags[1:-1]

from collections import defaultdict

def get_ner(sentence,verbose=False):
  decoded_sentences, tags = infer(sentence,verbose)
  new_decode = []
  new_tag = []

  temp_token = []
  flag = False
  prev_tag = ""
  for token, tag in zip(decoded_sentences, tags):
      if "@@" in token:
        flag = True
        temp_token.append(token)
      elif flag == True:
        if prev_tag != tag:
          temp_str = ""
          for tk in temp_token:
            tk = tk.replace("@@","")
            temp_str += tk
          new_tag.append(prev_tag)
          new_decode.append(temp_str)
          temp_token = []
          flag = False
          new_decode.append(token)
          new_tag.append(tag)
        else:
          temp_token.append(token)
          temp_str = ""
          for tk in temp_token:
            tk = tk.replace("@@","")
            temp_str += tk
          new_tag.append(tag)
          new_decode.append(temp_str)
          temp_token = []
          flag = False
      elif flag == False:
        new_tag.append(tag)
        new_decode.append(token)
      prev_tag = tag
  dict_ner = defaultdict(list)
  prev_label = "O"
  temp_token = []
  for token,tag in zip(new_decode,new_tag):
    if tag == "O": label = tag
    else: label = tag.split('_')[1]
    if label != prev_label:
      if prev_label != "O":
        temp_str = " ".join(temp_token)
        dict_ner[prev_label].append(temp_str.replace("_"," "))
      temp_token = []
    temp_token.append(token)
    prev_label = label

  if len(temp_token) != 0 and label != "O":
    temp_str = " ".join(temp_token)
    dict_ner[prev_label].append(temp_str.replace("_"," "))

  templateGen = " ".join(new_decode).replace("_"," ")
  for key in dictList.keys():
      list_ele = dictList[key]
      for ele in list_ele:
          idx = templateGen.rfind(ele)
          if idx != -1:
              if ele not in dict_ner[key]:
                dict_ner[key].append(ele)

  return dict_ner

data_link = "/content/drive/MyDrive/largeProject/code/combine/saved_dictionary.pkl"

with open(data_link, 'rb') as f:
    loaded_dict = pickle.load(f)

def loadParentSet(loaded_dict,company='VTS',all=False):
    groupKPISet = set()
    if all == False:
      for oneKPI in loaded_dict['01/2020']['month'][company]:
          comp = loaded_dict['01/2020']['month'][company][oneKPI]['KPI MẸ']
          groupKPISet.add(comp)
    else:
      for company in ['VTS','VTT','VDS','VTPOST']:
        for oneKPI in loaded_dict['01/2020']['month'][company]:
            comp = loaded_dict['01/2020']['month'][company][oneKPI]['KPI MẸ']
            groupKPISet.add(comp)

    return list(groupKPISet)

def listingGroupKPI(loaded_dict,company='VTPOST',kpi_mom='Tỷ lệ xử lý phản ánh của KH',):
    listOneKPI = []
    for oneKPI in loaded_dict['01/2020']['month'][company]:
        comp = loaded_dict['01/2020']['month'][company][oneKPI]['KPI MẸ']
        if comp == kpi_mom:
            listOneKPI.append(oneKPI)
    return listOneKPI

def getGroupKPI(loaded_dict,kpi,company = 'VTS'):
    kpi_mom = loaded_dict['01/2020']['month'][company][kpi]['KPI MẸ']

    return kpi_mom


def allListKPI(loaded_dict):
    listOneKPI = []
    for company in ['VTS','VTT','VDS','VTPOST']:
      for oneKPI in loaded_dict['01/2020']['month'][company]:
        listOneKPI.append(oneKPI)

    return listOneKPI

allKPI = allListKPI(loaded_dict)
allGroupKPI = loadParentSet(loaded_dict,all=True)

allKPI_embedding = []
allGroupKPI_embedding = []

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('keepitreal/vietnamese-sbert').to(device)

allKPI_embedding = model.encode(allKPI, convert_to_tensor=True)
allGroupKPI_embedding = model.encode(allGroupKPI, convert_to_tensor=True)

def query_sim(sentence,corpus_embedding,corpus):
    query_embedding = model.encode(sentence, convert_to_tensor=True).to(device)
    cos_scores = util.cos_sim(query_embedding, corpus_embedding)[0]
    top_results = torch.topk(cos_scores, k=1)

    return corpus[int(top_results[1])]

import sys
sys.path.append('/content/drive/MyDrive/largeProject/code/combine/mapping_dataset.py')
# %cd /content/drive/MyDrive/largeProject/code/combine/
import mapping_dataset

def getComp(loaded_dict,name_kpi='',group_name_kpi=''):
  if name_kpi != '':
    for comp in ['VTS','VTT','VDS','VTPOST']:
      for kpi in loaded_dict['01/2020']['month'][comp].keys():
          if kpi == name_kpi: return comp
  if group_name_kpi != '':
    for comp in ['VTS','VTT','VDS','VTPOST']:
      group_list = loadParentSet(loaded_dict,comp)
      if group_name_kpi in group_list: return comp

  return None

def module_processing_ner(id_ner):
    name_kpi = ""
    name_group_kpi = ""

    # print(id_ner.keys())
    #name kpi
    if '<tên chỉ tiêu>' not in id_ner.keys() and '<tên cụm chỉ tiêu>' not in id_ner.keys():
       return "Not information with <tên chỉ tiêu>!!"
    if '<tên chỉ tiêu>' in id_ner.keys():
       name_kpi = query_sim(id_ner["<tên chỉ tiêu>"][0],allKPI_embedding,allKPI)
    if '<tên cụm chỉ tiêu>' in id_ner.keys():
       name_group_kpi = query_sim(id_ner["<tên cụm chỉ tiêu>"][0],allGroupKPI_embedding,allGroupKPI)

    #view
    view = "month"
    if '<quarter>' in id_ner.keys() or '<quý>' in id_ner.keys(): view = "quarter"
    elif '<tháng>' not in id_ner.keys(): view = "year"

    #time
    if '<năm>' not in id_ner.keys(): return "Not information with <view>!!"
    year = id_ner['<năm>'][0]
    if view == "month": month = id_ner['<tháng>'][0].replace('/','')
    elif view == "quarter":
        if '<quý>' in id_ner.keys(): quarter = id_ner['<quý>'][0].replace('/','')
        if '<tháng>' in id_ner.keys(): quarter = id_ner['<tháng>'][0].replace('/','')
        month = int(quarter) * 3
    if view == "year": month = 12
    if int(month) < 10: month = f'0{month}'
    else: month = f'{month}'
    #tong cong ty
    if '<tên tổng công ty>' not in id_ner.keys():
        company = getComp(loaded_dict,name_kpi,name_group_kpi)
        if company is None: return "Not information with <tên tổng công ty>!!"

    else: company = id_ner['<tên tổng công ty>'][0]

    #other information
    return {
        "company" : company,
        "view" : view,
        "time" : f"{month}/{year}",
        "name_kpi" : name_kpi,
        "name_group_kpi" : name_group_kpi
    }
    
list_mapping = list(l2i_intent.keys())[1:]

dict_mapping = {
    'oneKPI' : mapping_dataset.mappingOneKPI,
    'ChildInferenceMom' : mapping_dataset.mappingChildInferenceMom,
    'groupMonthOverall' : mapping_dataset.mappingGroupMonthOverall,
    'groupMonthDetail' : mapping_dataset.mappingGroupMonthDetail,
    'crossView' : mapping_dataset.mappingCrossView,
    'viewExplainResult' : mapping_dataset.mappingViewExplainResult,
    'viewStat' : mapping_dataset.mappingViewStat,
    'viewPredict' : mapping_dataset.mappingViewPredict,
    'viewOneKPIStat' : mapping_dataset.mappingViewOneKPIStat,
    'viewOneGroupKPIStat' : mapping_dataset.mappingViewOneGroupKPIStat,
    'viewDetermineTrend' : mapping_dataset.mappingViewDetermineTrend,
    'viewCtyDescribe' : mapping_dataset.mappingCtyDescribe
    }

def get_index_childInferenceMom(ner_dict):
    index = None
    list_key_predict = ['<tháng tiếp theo>','<đạt>','<không đạt>']
    for key in list_key_predict:
        if key in ner_dict:
            index = 1
            break
    if index != 1:
        list_key_listed = ["<tất cả>","<chi tiết>","<tổng quan>"]
        for key in list_key_listed:
            if key in ner_dict:
              index = 0
              break

    return index

import random

def module_response(sentence,top_k=3):
    ner_dict = get_ner(sentence)
    basic_info = module_processing_ner(ner_dict)

    first_intent, intents = infer_intent(sentence,top_k=top_k,verbose=False)

    #retrieve
    #==============================
    company = basic_info["company"]
    view = basic_info["view"]
    timeFind = basic_info["time"]
    name_kpi = basic_info["name_kpi"]
    name_group_kpi = basic_info["name_group_kpi"]
    #==============================

    # if intents[0] == 0:
    #    print("câu hỏi con, xử lý sau")
    if intents[0] in [9,10,6,11]:
       func_mapping = dict_mapping[i2l_intent[int(intents[0])]]
       if intents[0] in [9,10]:
          choose = ""
          if '<mean>' in ner_dict.keys(): choose = "mean"
          elif '<min>' in ner_dict.keys(): choose = "min"
          elif '<max>' in ner_dict.keys(): choose = "max"
          if intent == 10: name_par = name_group_kpi
          else: name_par = name_kpi
          context = func_mapping(loaded_dict,timeFind,view,company,name_par,choose)
       else:
         context = func_mapping(loaded_dict,timeFind,company,name_kpi)
       print(context)
    else:
      # indices = np.where(intents==0)
      # intents = np.delete(intents, indices)

      print(name_group_kpi)
      print
      contexts = []
      # print(timeFind)
      for i,intent in enumerate(intents):
        print(f"intent là: {i2l_intent[int(intent)]} - passage {i+1}")
        print("="*30)
        func_mapping = dict_mapping[i2l_intent[int(intent)]]
        if intent in [1,5,11,6,12]:
           if intent == 1: context = func_mapping(loaded_dict,timeFind,view,company,name_kpi,dict_index={"indexNow":None,"indexBefore":2,"indexYearBefore":1,"index":3})
           else: context = func_mapping(loaded_dict,timeFind,company,name_kpi)
        elif intent in [7,8]:
          choose = ""
          if '<mùa>' in ner_dict.keys(): choose = "season"
          context = func_mapping(loaded_dict,timeFind,company,name_kpi,choose)
        elif intent in [9,10]:
          choose = ""
          if '<mean>' in ner_dict.keys(): choose = "mean"
          elif '<min>' in ner_dict.keys(): choose = "min"
          elif '<max>' in ner_dict.keys(): choose = "max"
          if intent == 10: name_par = name_group_kpi
          else: name_par = name_kpi
          context = func_mapping(loaded_dict,timeFind,view,company,name_par,choose)
        elif intent in [3,4]:
          if name_group_kpi == "":
             print("Câu hỏi này về chỉ tiêu chứ không phải cụm chỉ tiêu")
             continue
          index = None
          if '<tất cả>' in ner_dict.keys() or '<tổng quan>' in ner_dict.keys(): index = 0
          elif '<chi tiết>' in ner_dict.keys(): index = 1
          if intent == 4:
             if '<không đạt>' in ner_dict.keys(): index = 2
             elif '<đạt>' in ner_dict.keys(): index = 1
          context = func_mapping(loaded_dict,timeFind,view,company,name_group_kpi,index)
        else:
          index = get_index_childInferenceMom(ner_dict)
          context = func_mapping(loaded_dict,timeFind,company,name_kpi,index)
        print(context)
        print("="*30)
        contexts.append(context)

