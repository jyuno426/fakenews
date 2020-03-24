# -*- coding:utf-8 -*-

# import os
import pdb
import gensim
# import torch
# import gluonnlp as nlp
# from kobert.utils import get_tokenizer
# from gluonnlp.data import SentencepieceTokenizer
# from kobert.pytorch_kobert import get_pytorch_kobert_model
from gensim.models.keyedvectors import KeyedVectors

# print(spaced_sent['sent'])

# pdb.set_trace()

# device = "cuda:0"
# os.environ["CUDA_VISIBLE_DEVICES"] = '0, 1, 2, 3'
# bert_model, vocab = get_pytorch_kobert_model(device)
# bert_model = torch.nn.DataParallel(bert_model, output_device=0)

# bert_tokenizer = nlp.data.BERTSPTokenizer(get_tokenizer(), vocab, lower=False)
# transform = nlp.data.BERTSentenceTransform(bert_tokenizer,
#                                            max_seq_length=512,
#                                            pad=True,
#                                            pair=False)

model_bin = KeyedVectors.load("ko.bin")

print(len(model_bin["안녕"]))

# with open("res.txt", "r") as f:
#     for i, line in enumerate(f.readlines()):
#         id, title, _, _ = line.strip().split("@@@@")

#         sentence_list = [title.strip()]

#         if os.path.exists("articles/" + id + ".txt"):
#             with open("articles/" + id + ".txt", "r") as g:
#                 sentences = g.readlines()
#                 if len(sentences) < 3:
#                     continue
#                 for sentence in sentences:
#                     sentence_list.append(sentence.strip())

#             # batch = []
#             # len_info = []
#             # for sentence in sentence_list:
#             #     batch.append(transform(sentence)[0])
#             #     len_info.append(len(bert_tokenizer(sentence)))
#             # batch = torch.LongTensor(batch).to(device)
#             # with torch.no_grad():
#             #     output = bert_model(batch)[0]

#             # batch_vectors = []
#             # for i in range(len(batch)):
#             #     # batch_vectors.append(output[i][1:1 + len_info[i], :])
#             #     # pdb.set_trace()
#             #     batch_vectors.append(
#             #         torch.sum(output[i][1:1 + len_info[i], :], dim=0) /
#             #         len_info[i])

#             pdb.set_trace()
