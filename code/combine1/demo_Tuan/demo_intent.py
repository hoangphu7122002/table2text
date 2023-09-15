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
import py_vncorenlp

py_vncorenlp.download_model(save_dir='/content/')
rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='/content/')

import warnings
warnings.filterwarnings("ignore")

logging.set_verbosity_error()

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

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

label_intent = [
 'groupMonthOverall',
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

def infer_intent(text, max_len=32, top_k=3, verbose=False):
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

    str_text = ""

    for i,output in enumerate(topk_output):
      if int(output) == 12:
        str_text += f"intent 12: childQuestion\n"
      else:
        str_text += f"intent {i + 1}: {i2l_intent[int(output)]}\n"

    return str_text

