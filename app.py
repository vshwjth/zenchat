from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
import streamlit as st
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# template = """Question: {question}

B_INST = "[INST]"
E_INST = "[/INST]"
B_S = "<s>"
E_S = "<\s>"
B_SYS = "<<SYS>>"
E_SYS = "<</SYS>>"
NL = "\n"
SYSTEM_PROMPT = """You are are a helpful mental health assistant chat bot. Stay helpful and kind while answering. Keep your answers limited to 3-4 sentences. 
If the asked question is not relate to mental health or adjacent topics, tell them you can not answer. There is context given followed by a query. use the context to answer the question. Remain factful and state when the answer is unknown and cannot be inferred."""

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

@st.cache_resource
def return_llm():
    llm=""
    # llm = LlamaCpp(
    #     model_path="../mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
    #     n_gpu_layers=n_gpu_layers,
    #     n_batch=n_batch,
    #     f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    #     callback_manager=callback_manager,
    #     verbose=True,  # Verbose is required to pass to the callback manager
    # )
    return llm

# # llm_chain = prompt | llm
# # question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
# llm.invoke()

def gen_prompt(docs):
    global B_S, B_INST, B_SYS, E_INST, E_S, E_INST, SYSTEM_PROMPT, NL
    print(docs[0])
    context = """
### CONTEXT:
1) {cont1}
2) {cont2}
3) {cont3}

### QUESTION:
""".format(cont1=docs[0].page_content[0:350], cont2=docs[1].page_content[0:350], cont3=docs[2].page_content[0:350])
    msgs = st.session_state.messages
    # print(msgs)
    # print(len(msgs))
    if len(msgs) < 3:   
        prompt = B_S  + B_INST + " " +  B_SYS + NL + SYSTEM_PROMPT + NL + E_SYS + NL + context + NL+ msgs[-1]['content'] + " " + E_INST
    else:
        prompt = B_S  + B_INST + " " +  B_SYS + NL + SYSTEM_PROMPT + NL + E_SYS + NL + msgs[-3]['content'] + E_INST + " " + msgs[-2]['content'] + " " + E_S + " " + B_S + B_INST + " " + NL + context +  msgs[-1]['content'] + E_INST
    print(prompt + "\n")
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

    final_prompt = gen_prompt(docs)
    
    response = "template response"
    
    with st.chat_message("assistant"):
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

# print(type(st.session_state.messages))
#bruhrbruh