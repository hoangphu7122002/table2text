import torch
import transformers
from langchain import HuggingFacePipeline
from langchain.prompts import PromptTemplate
# from hf_embedding import HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import LLMChain

model_id = "meta-llama/Llama-2-7b-chat-hf"
pipeline_kwargs={"temperature":1, "max_new_tokens": 200, "repetition_penalty": 1.1}
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

model_config = transformers.AutoConfig.from_pretrained(
    model_id
)

model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    quantization_config=bnb_config,
    device_map='auto'
)
model.eval()
print(f"Model loaded")

tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_id
)

pipeline = transformers.pipeline(
    model=model,
    tokenizer=tokenizer,
    return_full_text=True,  # langchain expects the full text
    task='text-generation',
    **pipeline_kwargs
)

llm = HuggingFacePipeline(pipeline=pipeline)
llm.pipeline.tokenizer.return_token_type_ids = False
llm.pipeline.tokenizer.pad_token = llm.pipeline.tokenizer.eos_token

template = """
  "Context: {context}\n"
  "Question: {question}\n"
  "Answer: "
"""

qaprompt = PromptTemplate(
    input_variables=["context","question"],
    template=template)

hfe = HuggingFaceEmbeddings(
    model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1",
    encode_kwargs={'normalize_embeddings': True},
    model_kwargs={'device': 'cuda:0'},
)

import sys
sys.path.append('/content/drive/MyDrive/largeProject/code/combine/v1_script.py')
# %cd /content/drive/MyDrive/largeProject/code/combine/
from v1_script import *

import os
os.environ["OPENAI_API_KEY"] = "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"

import streamlit as st
from paperqa import Docs, Doc, PromptCollection
from paperqa.types import Text

def load_docs(docnames, docfiles):
    for i, f in enumerate(docfiles):
        st.session_state.docs.add_file(f, docname=docnames[i], chunk_chars=500)
    print("Documents added")


def answer_query(query):
    answer = st.session_state.docs.query(query)
    print(answer.formatted_answer)
    return answer

st.session_state.docdb = []
st.session_state.docs = Docs(llm=llm, embeddings=hfe)
st.session_state.context = ""

st.title("KPI Q&A")
st.subheader("Contexts")
context = None
st.session_state.context = ""
st.session_state.docs.delete(name="Manual Context")
st.subheader("Question")
question = st.text_input("Enter your question")

context_list = module_response(question,3)
if context_list != ['']:
    context = '\n'.join(context_list)
    st.session_state.context = ""
    st.session_state.docs.delete(name="Manual Context")
    if context != "":
      with st.spinner('Processing contexts...'):
        doc = Doc(docname="Manual Context",
                  citation="", dockey="Manual Context")
        texts = [Text(
            text=context,
            name="Manual Context",
            doc=doc,
        )]
        st.session_state.docs.add_texts(
            texts, doc=doc)
        st.session_state.context = context

st.text_area("Enter context", value=context, height=200, max_chars=500) 
st.subheader('Answer')
if question != "":
    with st.spinner('Finding answers...'):
        answer = answer_query(question)
else:
    answer = ""
st.write(answer)

st.write("Powered by LLaMA-2")

