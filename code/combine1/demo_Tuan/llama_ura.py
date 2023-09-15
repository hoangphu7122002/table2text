import torch
import transformers
from langchain import HuggingFacePipeline
from langchain.prompts import PromptTemplate
# from hf_embedding import HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import LLMChain
from peft import PeftModel, PeftConfig
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI
from langchain.docstore.document import Document
import requests
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
import pathlib
import subprocess
import tempfile
from langchain import HuggingFacePipeline
from langchain import PromptTemplate,  LLMChain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory

peft_model_id = "hoangphu7122002ai/LLama_URA_vi"

pipeline_kwargs={"temperature":0.1, "max_new_tokens": 200, "repetition_penalty": 1.1}
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

# set quantization configuration to load large model with less GPU memory
# this requires the `bitsandbytes` library
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

model_config = PeftConfig.from_pretrained(peft_model_id)

en_model = transformers.AutoModelForCausalLM.from_pretrained(
        model_config.base_model_name_or_path,
        trust_remote_code=True,
        config=model_config,
        quantization_config=bnb_config,
        device_map='auto'
)
vi_model = PeftModel.from_pretrained(en_model, peft_model_id)
vi_model.eval()
en_model.eval()

tokenizer = transformers.AutoTokenizer.from_pretrained(model_config.base_model_name_or_path)

print(f"Model loaded")

pipeline = transformers.pipeline(
    model=vi_model,
    tokenizer=tokenizer,
    return_full_text=True,  # langchain expects the full text
    task='text-generation',
    **pipeline_kwargs
)

llm = HuggingFacePipeline(pipeline=pipeline)
llm.pipeline.tokenizer.return_token_type_ids = False
llm.pipeline.tokenizer.pad_token = llm.pipeline.tokenizer.eos_token

template = """
  Viết câu trả lời không quá 150 từ"
   "cho câu hỏi dưới đây dựa trên ngữ cảnh được cung cấp."
   "Nếu ngữ cảnh cung cấp không đủ thông tin,"
   'trả lời "Tôi không thể trả lời". '
   "Trả lời bằng giọng điệu khách quan, toàn diện và trang trọng và nội dung chỉ trong ngữ cảnh"
   "Nếu câu hỏi mang tính chủ quan, hãy đưa ra câu trả lời có quan điểm trong 1-2 câu kết luận.\n\n
   "Ngữ cảnh: {context}\n"
   "Câu hỏi: {question}\n"
   "Trả lời: "
"""

qaprompt = PromptTemplate(
    input_variables=["context","question"],
    template=template)