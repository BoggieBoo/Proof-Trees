import json
import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer, util

forml4_path = 'data/FormL4/basic_test.json'
embed_path = 'data/embeddings/basic_nl_embeddings.pt'

with open(forml4_path, 'r') as file:
    data = json.load(file)
nl_embeddings = torch.load(embed_path)

model = SentenceTransformer('paraphrase-MPNet-base-v2')

def nl_rag(query_statement):
    query_statement = "This is the statement"
    query_embedding = model.encode(query_statement, convert_to_tensor=True)

    cosine_similarities = F.cosine_similarity(query_embedding, nl_embeddings)
    top_5 = torch.topk(cosine_similarities, 5).indices
    for i, v in enumerate(top_5):
        print(i + 1, data[v]['nl_problem'])
        print()

if __name__ == "__main__":
    statement = 'Actual: If a and b are even integers, then a + b is also even.'
    print()
    print('Actual:', statement)
    print()
    nl_rag(statement)
