import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

# index = faiss.IndexFlatL2(384) #384 is the dimension limit for all-MiniLM-L6-v2
# index = faiss.IndexIDMap(index)

model = SentenceTransformer('all-MiniLM-L6-v2')
# index_file = "faiss_index_file.idx"

# text = "ashish is good boy"
# xc = model.encode(text)
# embeddings = np.array([xc]).astype('float32')

# ids = np.array([2], dtype='int64')
# index.add_with_ids(embeddings, ids)

# faiss.write_index(index, index_file) #optional

index = faiss.read_index("../faiss_idx/123.idx")
text = "add 2 number "
xc = model.encode(text)
embeddings = np.array([xc]).astype('float32')
print(index.ntotal)
ids = np.array([3], dtype='int64')
index.add_with_ids(embeddings, ids)
faiss.write_index(index, "../faiss_idx/123.idx")
print(index.ntotal)
