from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.embeddings import SentenceTransformerEmbeddings

model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "mps"}
encode_kwargs = {"normalize_embeddings": True}
emb_func = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

# emb_func = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# loader = DirectoryLoader("./output")

# documents = loader.load()

# # print(len(docs))

# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)

# db = Chroma.from_documents(docs, emb_func, persist_directory="./chroma_db")

db = Chroma(persist_directory="./chroma_db", embedding_function=emb_func)
docs = db.similarity_search("Symptoms of Anxiety")

print(docs)
