from langchain.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.schema import Document
import pandas as pd
import tempfile
import os

def load_uploaded_file(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    if suffix == "xlsx":
        df = pd.read_excel(tmp_path)
        text = df.to_string(index=False)
        docs = [Document(page_content=text)]
    elif suffix == "csv":
        df = pd.read_csv(tmp_path)
        text = df.to_string(index=False)
        docs = [Document(page_content=text)]
    elif suffix == ".txt":
        loader = TextLoader(tmp_path)
        docs = loader.load()
    
    elif suffix == ".pdf":
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
    elif suffix == ".docx":
        loader = Docx2txtLoader(tmp_path)
        docs = [Document(page_content=text)]
    else:
        raise ValueError("Unsupported file type")

    docs = loader.load()
    return docs
