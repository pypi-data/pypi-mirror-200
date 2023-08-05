"""
    關於句子的模型封裝，支援train, predict, save, load等功能
    預設使用transformers模型
"""
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    TextClassificationPipeline, 
)

class Model:
    """
        關於句子的模型封裝，支援train, predict, save, load等功能
    """
    
    def __init__(self, model_name:str=None, tokenizer_name:str=None):
        self.model_name = model_name or "IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment"
        self.tokenizer_name = tokenizer_name or "IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment"
        
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name)
        self.classifer = TextClassificationPipeline(model=self.model, tokenizer=self.tokenizer)
        self.label_list = self.model.config.id2label

    def train(self, sentence_list:list, label_list:list):
        """
            sentence_list: 句子的list
            label_list: 每個句子的標籤
        """
        pass # TODO: 模型訓練
        

    def predict(self, sentence):
        """
            sentence可以是一個句子，也可以是一個句子的list
        """
        if not (isinstance(sentence, str) or isinstance(sentence, list)):
            raise TypeError("sentence must be a string or a list of string")
        
        return self.classifer(sentence)
        
    def save(self):
        pass

    def load(self):
        pass
    
