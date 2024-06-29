from .Inference import Sentiment

weight_path: str = "/home/ahmed/sentiment/SentimentGateway/SentimentAnalysisModel/ModelsRepository/model.pt"
model_name: str = 'distilbert-base-uncased'
def infer(samples):
    model = Sentiment(weight_path, model_name)
    outs = model(samples)
    
    return outs
