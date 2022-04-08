import json
import base64
import torch
import numpy as np
import requests
from typing import *
from transformers import BertTokenizer, DistilBertTokenizer
from torch.nn.utils.rnn import pad_sequence


AWS_API_GATEWAY = "https://5bx950umvl.execute-api.us-east-2.amazonaws.com/prod"


class OnlineToxicScorer():

    def __init__(self, bert_model_name='distilbert-base-uncased'):
        if bert_model_name.startswith('bert'):
            self.tokenizer = BertTokenizer.from_pretrained(bert_model_name, do_lower_case=True)
        elif bert_model_name.startswith('distilbert'):
            self.tokenizer = DistilBertTokenizer.from_pretrained(bert_model_name, do_lower_case=True)

    def inference(self, texts: List[str]) -> np.ndarray:
        '''
        input:
            texts: list of strings, no more than 4 strings
        output:
            preds: predicted toxic labels of each text
        '''
        token_tensors = [self._to_tensor(text) for text in texts]
        tensor = pad_sequence(token_tensors, batch_first=True, padding_value=self.tokenizer.pad_token_id)
        predictions = self._call_inference_service(tensor)
        return predictions

    def _to_tensor(self, text: str):
        tokens = self.tokenizer.encode(text, add_special_tokens=True, truncation=True, max_length=128)
        x = torch.LongTensor(tokens)
        return x

    def _call_inference_service(self, data: torch.Tensor) -> Union[np.ndarray, None]:
        '''
        input:
            data: preprocessed torch
        output:
            data: numpy array of shape [Batch, Seqlen] or None
        '''
        tensor = base64.b64encode(np.array(data.reshape(-1), dtype=np.int64))
        tensor_shape = base64.b64encode(np.array(data.shape, dtype=np.int64))
        body = {
            'data': {
                "tensor": tensor.decode('utf-8'),
                "shape": tensor_shape.decode('utf-8')
            }
        }
        response = requests.post(AWS_API_GATEWAY, json=body)
        try:
            prediction = np.array(response.text[1:-1].split(','), dtype=np.float64)
            res = prediction.reshape(-1, 6)
        except Exception as e:
            print(e)
            res = None
        return res
