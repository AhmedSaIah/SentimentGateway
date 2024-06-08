from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Setting seed to get consistent results with langdetect
DetectorFactory.seed = 0

def filter_english_reviews(reviews):
    english_reviews = []
    
    for review in reviews:
        try:
            # Detect the language of the review
            if detect(review) == 'en':
                english_reviews.append(review)
        except LangDetectException:
            # If detection fails, skip the review
            continue
    
    return english_reviews

# Example usage
reviews = [
    "I love this product! It works great and is very useful.",
    "Este producto es increíble. Me encanta.",
    "C'est un produit génial, je l'adore.",
    "Ich finde das Produkt super, es ist sehr nützlich."
]

english_reviews = filter_english_reviews(reviews)
print("English Reviews:", english_reviews)
