import os
import json
import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer, util

forml4_path = 'data/FormL4/basic_test.json'
embed_path = 'data/embeddings/basic_nl_embeddings.pt'

with open(forml4_path, 'r') as file:
    data = json.load(file)
nl_proofs = [theorem['nl_problem'] for theorem in data]

model = SentenceTransformer('paraphrase-MPNet-base-v2')
nl_embeddings = model.encode(nl_proofs, convert_to_tensor=True)
torch.save(nl_embeddings, embed_pat