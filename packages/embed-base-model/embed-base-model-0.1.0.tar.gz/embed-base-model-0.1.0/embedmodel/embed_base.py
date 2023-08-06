import os
import torch
from torch.nn import functional as F
from abc import ABCMeta, abstractmethod


class EmbedModelBase(metaclass=ABCMeta):

    ROUND_LEN = 4

    def __init__(self, model_path: str):
        assert os.path.isdir(model_path)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = self._load_tokenizer(model_path)
        self.model = self._load_model(model_path)
    
    @abstractmethod
    def _load_model(self, model_path: str):
        return None
    
    @abstractmethod
    def _load_tokenizer(self, model_path: str):
        return None
    
    def _get_encode(self, input_text: str):
        _encoded_sentence = self.tokenizer.encode(
            input_text, add_special_tokens=True, return_tensors='pt'
        ).to(self.device)
        _result = None
        with torch.no_grad():
            _output = self.model(_encoded_sentence)
            if _output.hidden_states:
                _embeded_sentence = _output.hidden_states[-1].mean(dim=1)
            else:
                #TODO: catch more exceptions
                _embeded_sentence = _output.last_hidden_state.mean(dim=1)
            _result = torch.squeeze(_embeded_sentence)
        return _result
    
    def _calculate_cosine_similarity(self, encode_text1: torch.Tensor, encode_text2: torch.Tensor):
        _sim_score = F.cosine_similarity(encode_text1, encode_text2, dim=0)
        return round(_sim_score.item(), self.ROUND_LEN)
    
    def calculate_similiarity(self, input_text1: str, input_text2: str):
        _encode1 = self._get_encode(input_text1)
        _encode2 = self._get_encode(input_text2)
        return self._calculate_cosine_similarity(_encode1, _encode2)
