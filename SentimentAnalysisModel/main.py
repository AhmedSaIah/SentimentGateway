from .Inference import Sentiment

def infer(samples):

# fix the path
    weight_path: str = "/home/ahmed/sentiment/SentimentGateway/SentimentAnalysisModel/ModelsRepository/model.pt"
    model_name: str = 'distilbert-base-uncased'
    model = Sentiment(weight_path, model_name)

    
    outs = model(samples)
    
    return outs
