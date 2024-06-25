from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
import streamlit as st
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# template = """Question: {question}

B_INST = "[INST]"
E_INST = "[/INST]"
B_SYS = "<s>"
E_SYS = "<\s>"

st.set_page_config(
    page_title="ZenChat",
    page_icon="🤖",
    layout="wide"
)

# # Answer: Let's work this out in a step by step way to be sure we have the right answer."""


# prompt = PromptTemplate.from_template(template)

# # # Callbacks support token-wise streaming
# callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# n_gpu_layers = -1  # The number of layers to put on the GPU. The rest will be on the CPU. If you don't know how many layers there are, you can use -1 to move all to GPU.
# n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

# @st.cache_resources
# llm = LlamaCpp(
#     model_path="../mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
#     n_gpu_layers=n_gpu_layers,
#     n_batch=n_batch,
#     f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
#     callback_manager=callback_manager,
#     verbose=True,  # Verbose is required to pass to the callback manager
# )

# # llm_chain = prompt | llm
# # question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
# llm.invoke()

def gen_prompt(question: str):
    prompt = ""

    return prompt


model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "mps"}
encode_kwargs = {"normalize_embeddings": True}

@st.cache_resource
def return_db():
    emb_func = HuggingFaceBgeEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )
    db = Chroma(persist_directory="./chroma_db", embedding_function=emb_func)
    return db



db = return_db()

st.title("ZenChat")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey! How are you feeling"}
    ]


# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    docs = db.similarity_search(user_prompt)

    response = "{}\n".format(docs)
    
    with st.chat_message("assistant"):
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

print(type(st.session_state.messages))
#bruhrbruh