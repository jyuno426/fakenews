# -*- coding:utf-8 -*-

import torch
import gluonnlp as nlp
from kobert.utils import get_tokenizer
from gluonnlp.data import SentencepieceTokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

# input_ids = torch.LongTensor([[31, 51, 99], [15, 5, 0]])
# input_mask = torch.LongTensor([[1, 1, 1], [1, 1, 0]])
# token_type_ids = torch.LongTensor([[0, 0, 1], [0, 1, 0]])
# bert_model, vocab = get_pytorch_kobert_model()
# sequence_output, pooled_output = bert_model(input_ids, input_mask,
#                                             token_type_ids)
# pooled_output.shape

# tok_path = get_tokenizer()
# sp = SentencepieceTokenizer(tok_path)
# sp('한국어 모델을 공유합니다.')
# ['▁한국', '어', '▁모델', '을', '▁공유', '합니다', '.']

# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# model = BertModel.from_pretrained('bert-base-uncased')
# input_ids = torch.tensor(tokenizer.encode("Hello, my dog is cute")).unsqueeze(
#     0)  # Batch size 1
# outputs = model(input_ids)
# last_hidden_states = outputs[
#     0]  # The last hidden-state is the first element of the output tuple

bert_model, vocab = get_pytorch_kobert_model("cuda:0")
bert_tokenizer = nlp.data.BERTSPTokenizer(get_tokenizer(), vocab, lower=False)
transform = nlp.data.BERTSentenceTransform(bert_tokenizer,
                                           max_seq_length=512,
                                           pad=True,
                                           pair=False)

import pdb
pdb.set_trace()

# print(transform("한국어 모델을 공유합니다"))