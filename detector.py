# -*- coding:utf-8 -*-

import os
import regex
import pdb
import gensim
import torch
import json
import numpy as np
# import gluonnlp as nlp
# from kobert.utils import get_tokenizer
# from gluonnlp.data import SentencepieceTokenizer
# from kobert.pytorch_kobert import get_pytorch_kobert_model
from gensim.models.keyedvectors import KeyedVectors
from pykospacing import spacing
from konlpy.tag import Kkma

import warnings
warnings.filterwarnings("ignore")
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

kkma = Kkma()
model_bin = KeyedVectors.load("ko.bin")
cos = torch.nn.CosineSimilarity(dim=0)
# print(len(model_bin["안녕"]))

my_dict = {}


def koreanize(string):
    return regex.sub(u"[^ \r\n\p{Hangul}.?!]", " ", string).strip()


def word_segment(sentence):
    return [word for word, _ in kkma.pos(sentence)]


with open("res.txt", "r") as f:
    for i, line in enumerate(f.readlines()):
        print(i)
        id, title, _, _ = line.strip().split("@@@@")

        if os.path.exists("articles/" + id + ".txt"):
            sentence_list = [title.strip()]

            with open("articles/" + id + ".txt", "r") as g:
                sentences = g.readlines()
                if len(sentences) < 3:
                    continue
                for sentence in sentences:
                    sentence_list.append(sentence.strip())

            tensor_list = []
            new_sentence_list = []
            for sentence in sentence_list:
                word_list = word_segment(spacing(koreanize(sentence)))
                new_sentence_list.append(" ".join(word_list))
                if len(word_list) > 0:
                    vec_list = []
                    for word in word_list:
                        if word in model_bin.vocab:
                            vec_list.append(model_bin[word])
                        elif word in my_dict:
                            vec_list.append(my_dict[word])
                        else:
                            random_vector = np.random.rand(200)
                            my_dict[word] = random_vector
                            vec_list.append(random_vector)

                    vector = torch.sum(torch.tensor(vec_list),
                                       dim=0) / len(word_list)
                    tensor_list.append(vector)
                else:
                    tensor_list.append("invalid")

            if tensor_list[0] == "invalid":
                continue

            with open("detects/" + id + ".txt", "w") as g:
                g.write(sentence_list[0] + "@@@@" + new_sentence_list[0] +
                        "\n")
                scored_sentence_list = []
                for j in range(1, len(tensor_list)):
                    if tensor_list[j] != "invalid":
                        score = float(cos(tensor_list[0], tensor_list[j]))
                        scored_sentence_list.append(
                            str(score) + " @@@@" + sentence_list[j] + "@@@@" +
                            new_sentence_list[j])

                for scored_sentence in reversed(sorted(scored_sentence_list)):
                    g.write(scored_sentence + "\n")

            # batch = []
            # len_info = []
            # for sentence in sentence_list:
            #     batch.append(transform(sentence)[0])
            #     len_info.append(len(bert_tokenizer(sentence)))
            # batch = torch.LongTensor(batch).to(device)
            # with torch.no_grad():
            #     output = bert_model(batch)[0]

            # batch_vectors = []
            # for i in range(len(batch)):
            #     # batch_vectors.append(output[i][1:1 + len_info[i], :])
            #     # pdb.set_trace()
            #     batch_vectors.append(
            #         torch.sum(output[i][1:1 + len_info[i], :], dim=0) /
            #         len_info[i])

            # pdb.set_trace()

with open("my_dict.json", "w") as f:
    json.dump(my_dict, f)