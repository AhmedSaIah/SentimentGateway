import torch
import numpy as np
from transformers import DistilBertForSequenceClassification
from transformers import DistilBertTokenizer

from SentimentAnalysis.Utils import clean_text


from typing import Union, List

class Sentiment:

    def __init__(self, model_path: str= None):
        self.max_length = 512
        self.model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

        self.model.eval()
        #self.model= torch.load(model_path)

    def pre_processing(self, sample: str= ""):
        assert sample, "Input sample should not be empty text"
        cleaned_text = clean_text(sample)
        encoding = self.tokenizer(
            cleaned_text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten()
        }
        

    def inference(self, input_ids= None, attention_mask= None):

        outputs = self.model(input_ids, attention_mask=attention_mask)
        import pdb; pdb.set_trace()
        return outputs
        #raise NotImplemented("This method is not implemented yet")
    
    def post_process(self, outputs= None):
        preds = torch.argmax(outputs.logits, dim=1)

        return preds
        #raise NotImplemented("This method is not implemented yet")
    
    def __call__(self, sample: Union[List, str]= None):
        assert isinstance(sample, str), "Inputs should either string or list"

        input_ids, attention_mask = self.pre_processing(sample)
        model_outputs = self.inference(input_ids = input_ids, attention_mask= attention_mask)
        sample_class, sample_props = self.post_process(model_outputs)

        return sample_class, sample_props


        