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

import sys
sys.path.append('/content/drive/MyDrive/largeProject/code/combine/mapping_dataset.py')
# %cd /content/drive/MyDrive/largeProject/code/combine/
import mapping_dataset


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
    # print(text)
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
quarter = ["q1","q2","q3","q4","quý","q 1", "q 2", "q 3", "q 4"]

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

import pandas as pd
import numpy as np
import re
import tensorflow as tf
import tensorflow.keras.backend as K
import tensorflow.keras.layers as L
from tensorflow_addons.text import crf_log_likelihood, crf_decode
from tensorflow.keras.preprocessing.text import Tokenizer, tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, TimeDistributed, Input, BatchNormalization, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import initializers, Sequential
import tensorflow.keras.optimizers as Optimizer

pd.set_option('display.max_colwidth', -1)

class CRF(L.Layer):
    def __init__(self,
                 output_dim,
                 sparse_target=True,
                 **kwargs):
        """
        Args:
            output_dim (int): the number of labels to tag each temporal input.
            sparse_target (bool): whether the the ground-truth label represented in one-hot.
        Input shape:
            (batch_size, sentence length, output_dim)
        Output shape:
            (batch_size, sentence length, output_dim)
        """
        super(CRF, self).__init__(**kwargs)
        self.output_dim = int(output_dim)
        self.sparse_target = sparse_target
        self.input_spec = L.InputSpec(min_ndim=3)
        self.supports_masking = False
        self.sequence_lengths = None
        self.transitions = None

    def build(self, input_shape):
        assert len(input_shape) == 3
        f_shape = tf.TensorShape(input_shape)
        input_spec = L.InputSpec(min_ndim=3, axes={-1: f_shape[-1]})

        if f_shape[-1] is None:
            raise ValueError('The last dimension of the inputs to `CRF` '
                             'should be defined. Found `None`.')
        if f_shape[-1] != self.output_dim:
            raise ValueError('The last dimension of the input shape must be equal to output'
                             ' shape. Use a linear layer if needed.')
        self.input_spec = input_spec
        self.transitions = self.add_weight(name='transitions',
                                           shape=[self.output_dim, self.output_dim],
                                           initializer='glorot_uniform',
                                           trainable=True)
        self.built = True

    def compute_mask(self, inputs, mask=None):
        # Just pass the received mask from previous layer, to the next layer or
        # manipulate it if this layer changes the shape of the input
        return mask

    def call(self, inputs, sequence_lengths=None, training=None, **kwargs):
        sequences = tf.convert_to_tensor(inputs, dtype=self.dtype)
        if sequence_lengths is not None:
            assert len(sequence_lengths.shape) == 2
            assert tf.convert_to_tensor(sequence_lengths).dtype == 'int32'
            seq_len_shape = tf.convert_to_tensor(sequence_lengths).get_shape().as_list()
            assert seq_len_shape[1] == 1
            self.sequence_lengths = K.flatten(sequence_lengths)
        else:
            self.sequence_lengths = tf.ones(tf.shape(inputs)[0], dtype=tf.int32) * (
                tf.shape(inputs)[1]
            )

        viterbi_sequence, _ = crf_decode(sequences,
                                         self.transitions,
                                         self.sequence_lengths)
        output = K.one_hot(viterbi_sequence, self.output_dim)
        return K.in_train_phase(sequences, output)

    @property
    def loss(self):
        def crf_loss(y_true, y_pred):
            y_pred = tf.convert_to_tensor(y_pred, dtype=self.dtype)
            log_likelihood, self.transitions = crf_log_likelihood(
                y_pred,
                tf.cast(K.argmax(y_true), dtype=tf.int32) if self.sparse_target else y_true,
                self.sequence_lengths,
                transition_params=self.transitions,
            )
            return tf.reduce_mean(-log_likelihood)
        return crf_loss

    @property
    def accuracy(self):
        def viterbi_accuracy(y_true, y_pred):
            # -1e10 to avoid zero at sum(mask)
            mask = K.cast(
                K.all(K.greater(y_pred, -1e10), axis=2), K.floatx())
            shape = tf.shape(y_pred)
            sequence_lengths = tf.ones(shape[0], dtype=tf.int32) * (shape[1])
            y_pred, _ = crf_decode(y_pred, self.transitions, sequence_lengths)
            if self.sparse_target:
                y_true = K.argmax(y_true, 2)
            y_pred = K.cast(y_pred, 'int32')
            y_true = K.cast(y_true, 'int32')
            corrects = K.cast(K.equal(y_true, y_pred), K.floatx())
            return K.sum(corrects * mask) / K.sum(mask)
        return viterbi_accuracy

    def compute_output_shape(self, input_shape):
        tf.TensorShape(input_shape).assert_has_rank(3)
        return input_shape[:2] + (self.output_dim,)

    def get_config(self):
        config = {
            'output_dim': self.output_dim,
            'sparse_target': self.sparse_target,
            'supports_masking': self.supports_masking,
            'transitions': K.eval(self.transitions)
        }
        base_config = super(CRF, self).get_config()
        return dict(base_config, **config)

from gensim.models import FastText
import pickle
trained = True

model_fasttext = FastText.load('/content/drive/MyDrive/CRF/Data/Fasttext/model_fasttext_gensim.bin')

with open('/content/drive/MyDrive/CRF/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

word_index = tokenizer.word_index
emb_mean, emb_std = -0.5,0.5
embed_size = 100 #Kích thước vector biểu diễn 1 từ
nb_words = len(word_index) + 1
embedding_matrix = np.random.normal(emb_mean, emb_std, (nb_words, embed_size))
for word, i in word_index.items():
    if i >= nb_words:
        continue
    if word in model_fasttext.wv.key_to_index:
        embedding_matrix[i] = model_fasttext.wv.get_vector(word)

with open('/content/drive/MyDrive/CRF/tag_tokenizer.pickle', 'rb') as handle:
    tag_tokenizer = pickle.load(handle)

tag_index = tag_tokenizer.word_index
tag_size = len(tag_index) + 1

def create_model(embeddings_matrix, vocab_size, embedding_dim, max_length):
    crf = CRF(len(tag_index), sparse_target=True)
    input = Input(shape = (max_length, ), dtype='int32', name='input_text')
    x = Embedding(input_dim=vocab_size, output_dim=embedding_dim,
                  weights=[embedding_matrix])(input)
    x = Bidirectional(LSTM(units=max_length, return_sequences=True,
                                recurrent_dropout=0.01))(x)
    x = TimeDistributed(Dense(128, activation='relu', kernel_initializer='he_normal'))(x)
    x = BatchNormalization()(x)
    x = Dropout(rate=0.6)(x)
    x = Dense(len(tag_index), activation='relu', kernel_initializer='he_normal')(x)
    x = BatchNormalization()(x)
    x = Dropout(rate=0.1)(x)
    output = crf(x)
    model_final = Model(input, output)
    model_final.compile(optimizer=Optimizer.Adam(lr=0.001), loss=crf.loss,
                        metrics=[crf.accuracy])

    return model_final

model_ner = create_model(embedding_matrix, nb_words, embed_size, max_length = 100)
model_ner.load_weights("/content/drive/MyDrive/CRF/Data/Fasttext/best_weight.hdf5")

def get_tags(sequences, tag_index):
    sequence_tags = []
    for sequence in sequences:
        sequence_tag = []
        for categorical in sequence:
            sequence_tag.append(tag_index.get(np.argmax(categorical)))
        sequence_tags.append(sequence_tag)
    return sequence_tags

def predict(model, tag_tokenizer, sent):
    tag_index = tag_tokenizer.word_index
    tag_size = len(tag_index) + 1
    pred = model.predict(sent)
    sequence_tags = get_tags(pred, {i: t for t, i in tag_index.items()})
    for idx, each in enumerate(sequence_tags):
        try:
           idx_cut = each.index(None)
        except:
           idx_cut = len(each) + 1
        sequence_tags[idx] = each[:idx_cut]
    return sequence_tags

def match_pair_ner(text, ner):
    dict_ = {}
    text_arr = text.split(' ')
    save_ner, save_words = None, ''
    for i in range(len(text_arr)):
      if ner[i] == 'O' or 'B_' in ner[i] or ('I_' in ner[i] and ner[i - 1] == 'O'):
        if save_ner is not None and save_ner != 'O':
          if save_ner not in dict_:
            dict_[save_ner] = []
          dict_[save_ner].append(save_words.replace('_', ' ').strip())
        save_words = text_arr[i] + ' '
      else:
        save_words += text_arr[i] + ' '
      save_ner = ner[i] if ner[i] == 'O' else ner[i][2:]
    if save_ner is not None and save_ner != 'O':
        if save_ner not in dict_:
            dict_[save_ner] = []
        dict_[save_ner].append(save_words.replace('_', ' ').strip())
    return dict_

month_list = ["t","th","thg","tháng"]
quy_list = ["q","quý"]
number_list = [*range(1,13)]
num_quarter_list = [*range(1,5)]

def infer_ner(text, model, tokenizer, tag_tokenizer, max_length=100):
    text = text.replace('?','').replace('/',' ').replace("\\"," ").replace('.'," ").replace("_","").lower()
    for month_desc in month_list:
      for num in number_list:
        text = text.replace(month_desc + str(num),month_desc + " " + str(num))
    for quy in quy_list:
      for num in num_quarter_list:
        text = text.replace(quy + str(num),quy + " " + str(num))
    word_segment = rdrsegmenter.word_segment(text)
    res_text = tokenizer.texts_to_sequences(word_segment)
    res_text = pad_sequences(res_text, maxlen=max_length, padding='post')
    res_text = predict(model, tag_tokenizer, res_text)
    # print(res_text)
    dict_ = match_pair_ner(word_segment[0], res_text[0])
    return dict_


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

def module_processing_ner_v0(id_ner):
    name_kpi = ""
    name_group_kpi = ""

    # print(id_ner.keys())
    #name kpi
    # if '<tên chỉ tiêu>' not in id_ner.keys() and '<tên cụm chỉ tiêu>' not in id_ner.keys():
    #    return "Not information with <tên chỉ tiêu>!!"
    if '<tên_chỉ_tiêu>' in id_ner.keys():
       name_kpi = query_sim(id_ner["<tên_chỉ_tiêu>"][0],allKPI_embedding,allKPI)
    if '<tên_cụm_chỉ_tiêu>' in id_ner.keys():
       name_group_kpi = query_sim(id_ner["<tên_cụm_chỉ_tiêu>"][0],allGroupKPI_embedding,allGroupKPI)

    #view
    view = "month"
    if '<năm>' in id_ner.keys() and '/' in id_ner['<năm>'][0]:
       year = id_ner['<năm>'][0].split('/')[1]
       month = id_ner['<năm>'][0].split('/')[0]
       id_ner['<năm>'][0] = year
       id_ner['<tháng>'] = list()
       id_ner['<tháng>'].append(month)
      #  print("here")
    elif '<quarter>' in id_ner.keys() or '<quý>' in id_ner.keys(): view = "quarter"
    elif '<tháng>' not in id_ner.keys(): view = "year"

    #time
    if '<năm>' not in id_ner.keys(): return None
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
    if '<tên_tổng_công_ty>' not in id_ner.keys():
        company = getComp(loaded_dict,name_kpi,name_group_kpi)
        if company is None: return None

    else: company = id_ner['<tên_tổng_công_ty>'][0]

    #other information
    return {
        "company" : company.upper(),
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
    ner_dict = infer_ner(sentence,model_ner, tokenizer, tag_tokenizer)
    # print(ner_dict)
    basic_info = module_processing_ner_v0(ner_dict)
    # print(basic_info)
    first_intent, intents = infer_intent(sentence,top_k=top_k,verbose=False)
    if basic_info is None:
      return [""]
    if 10 not in intents:
      if 'name_kpi' not in basic_info.keys() and 'name_group_kpi' not in basic_info.keys():
        return [""]
      if 'time' not in basic_info.keys():
        return [""]
      if 'view' not in basic_info.keys():
        return [""]
    #retrieve
    #==============================

    # print(basic_info)
    company = basic_info["company"]
    view = basic_info["view"]
    timeFind = basic_info["time"]
    name_kpi = basic_info["name_kpi"]
    name_group_kpi = basic_info["name_group_kpi"]
    #==============================
    # print(basic_info)
    # if intents[0] == 0:
    #    print("câu hỏi con, xử lý sau")
    # if intents[0] in [9,11,8,6]:
    #    func_mapping = dict_mapping[i2l_intent[int(intents[0])]]
    #    if intents[0] in [9,11]:
    #       choose = ""
    #       if '<mean>' in ner_dict.keys(): choose = "mean"
    #       elif '<min>' in ner_dict.keys(): choose = "min"
    #       elif '<max>' in ner_dict.keys(): choose = "max"
    #       if intent == 11: name_par = name_group_kpi
    #       else: name_par = name_kpi
    #       context = func_mapping(loaded_dict,timeFind,view,company,name_par,choose)
    #    else:
    #      context = func_mapping(loaded_dict,timeFind,company,name_kpi)
    #    print(context)
    # else:
    # indices = np.where(intents==0)
    # intents = np.delete(intents, indices)

    # print(name_group_kpi)
    # print
    contexts = []
    # print(timeFind)
    for i,intent in enumerate(intents):
      if intent == 12: continue
      print(f"intent là: {i2l_intent[int(intent)]} - passage {i+1}")
      # print("="*30)
      func_mapping = dict_mapping[i2l_intent[int(intent)]]
      if intent in [1,2,6,8,10]:
          if intent == 1: context = func_mapping(loaded_dict,timeFind,view,company,name_kpi,dict_index={"indexNow":None,"indexBefore":2,"indexYearBefore":1,"index":3})
          elif intent == 10: context = func_mapping(loaded_dict,timeFind,view,company)
          else: context = func_mapping(loaded_dict,timeFind,company,name_kpi)
      elif intent in [7,4]:
        choose = ""
        if '<mùa>' in ner_dict.keys(): choose = "season"
        context = func_mapping(loaded_dict,timeFind,company,name_kpi,choose)
      elif intent in [9,11]:
        choose = ""
        if '<mean>' in ner_dict.keys(): choose = "mean"
        elif '<min>' in ner_dict.keys(): choose = "min"
        elif '<max>' in ner_dict.keys(): choose = "max"
        if intent == 11: name_par = name_group_kpi
        else: name_par = name_kpi
        context = func_mapping(loaded_dict,timeFind,view,company,name_par,choose)
      elif intent in [0,5]:
        if name_group_kpi == "":
            # print("Câu hỏi này về chỉ tiêu chứ không phải cụm chỉ tiêu")
            continue
        index = None
        if '<tất cả>' in ner_dict.keys() or '<tổng quan>' in ner_dict.keys(): index = 0
        elif '<chi tiết>' in ner_dict.keys(): index = 1
        if intent == 5:
            if '<không đạt>' in ner_dict.keys(): index = 2
            elif '<đạt>' in ner_dict.keys(): index = 1
        context = func_mapping(loaded_dict,timeFind,view,company,name_group_kpi,index)
      else:
        index = get_index_childInferenceMom(ner_dict)
        context = func_mapping(loaded_dict,timeFind,company,name_kpi,index)
      # print(context)
      # print("="*30)
      contexts.append(context)
    return contexts