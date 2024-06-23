from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from llama_cpp import Llama

# # llm = LlamaCpp(model_path="/Users/vishwa-21387/Documents/code/zenchat/server/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf")


# template = """Question: {question}

# # Answer: Let's work this out in a step by step way to be sure we have the right answer."""

# prompt = PromptTemplate.from_template(template)

# # # Callbacks support token-wise streaming
# callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# n_gpu_layers = -1  # The number of layers to put on the GPU. The rest will be on the CPU. If you don't know how many layers there are, you can use -1 to move all to GPU.
# n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

# # # Make sure the model path is correct for your system!
# llm = LlamaCpp(
#     model_path="/Users/vishwa-21387/Documents/code/zenchat/server/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
#     n_gpu_layers=n_gpu_layers,
#     n_batch=n_batch,
#     f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
#     callback_manager=callback_manager,
#     verbose=True,  # Verbose is required to pass to the callback manager
# )

# llm_chain = prompt | llm
# question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"
# llm_chain.invoke({"question": question})from llama_cpp import Llama
model = "/Users/vishwa-21387/Documents/code/zenchat/server/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf"  # instruction model
llm = Llama(model_path=model, n_batch=512, n_threads=7, n_gpu_layers=7, verbose=True)
system = """
Follow the instructions below to complete the task.
"""

user = """
Create a PHP script to scan a directory and print the contents of the directory.
"""

message = f"<s>[INST] {system} [/INST]</s>{user}"
output = llm(message, echo=True, stream=False, max_tokens=4096)
print(output['usage'])
output = output['choices'][0]['text'].replace(message, '')
print(output)