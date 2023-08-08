from sentence_transformers import SentenceTransformer, util
embedder = SentenceTransformer('bert-base-uncased')
#embedder = SentenceTransformer('xlm-roberta-base')
a = embedder.encode(['I like NY'])
print(a)

from transformers import BertTokenizerFast, BertModel
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")
text_1 = "I like NY"
encoded_text = tokenizer(text_1, return_tensors='pt')
output = model(**encoded_text, return_dict=False)
print(output)