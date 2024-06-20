from typing import List, Union

import numpy as np
import torch
import torch.nn.functional as F
from transformers import (DistilBertForSequenceClassification,
                          DistilBertTokenizer)

from SentimentAnalysisModel.Utils import clean_text


class Sentiment:

    def __init__(self, weight_path: str = None, model_name: str = None):

        self.index2type_map = {0: "Negative", 1: "Positive"}
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.max_length = 512
        self.model = DistilBertForSequenceClassification.from_pretrained(
            model_name, num_labels=2)
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_name
                                                             )
        self._load_weights(weight_path)
        self.model.eval()
        # self.model= torch.load(model_path)

    def _load_weights(self, weight_path: str):
        """
        Load weights into the model from a .pt file.

        Args:
            weight_path (str): Path to the .pt file containing model weights.
        """

        state_dict = torch.load(weight_path, map_location=self.device)
        self.model.load_state_dict(state_dict)
        print(f"Weights loaded successfully from {weight_path}")

    def pre_processing(self, sample: str = ""):
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

        return encoding['input_ids'].flatten(), encoding['attention_mask'].flatten()

    def inference(self, input_ids=None, attention_mask=None):

        outputs = self.model(input_ids, attention_mask=attention_mask)
        return outputs
        # raise NotImplemented("This method is not implemented yet")

    def post_process(self, outputs=None):
        preds = torch.argmax(outputs.logits, dim=1)

        return preds, outputs.logits
        # raise NotImplemented("This method is not implemented yet")

    def __call__(self, reviews: Union[List, str] = None):
        assert isinstance(
            reviews, Union[List, str]), "Inputs should either string or list"
        outs = []
        if isinstance(reviews, str):
            reviews = [reviews]

        for review in reviews:
            input_ids, attention_mask = self.pre_processing(review)
            model_outputs = self.inference(
                input_ids=input_ids, attention_mask=attention_mask)
            sample_class_index, sample_props = self.post_process(model_outputs)
            # import pdb; pdb.set_trace()
            input_text_class = self.index2type_map[sample_class_index.item()]
            probabilities = F.softmax(sample_props, dim=-1)
            probabilities = probabilities.detach().numpy()[0].tolist()
            outs.append(
                [input_text_class, probabilities[0], probabilities[1]])

        return outs
