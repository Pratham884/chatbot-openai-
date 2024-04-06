import os
import sys
import logging
import textwrap

import warnings

warnings.filterwarnings("ignore")
# stop huggingface warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Uncomment to see debug logs
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.vector_stores.redis import RedisVectorStore
from IPython.display import Markdown, display


import os



os.environ["OPENAI_API_KEY"] = "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"

loader = SimpleDirectoryReader(r"NEW FAQs.pdf")
documents = loader.load_data()
for file in loader.input_files:
    print(file)

# print(RedisVectorStore.__init__.__doc__)

from llama_index.core import StorageContext

vector_store = RedisVectorStore(
    index_name="chatbot",
    index_prefix="llama",
    redis_url="redis://localhost:6379",  # Default
    overwrite=True,
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

import redis
r = redis.Redis()
index_name = "poker log reader"
r.set(f"added:{index_name}", "true")


query_engine = index.as_query_engine()
response = query_engine.query("how many users won the game")
print(textwrap.fill(str(response), 100))

vector_store.persist(persist_path="")

