from langdetect import DetectorFactory, detect
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


def match_keyword(reviews, keyword):
    matched_reviews = []
    keyword = keyword.lower()
    for review in reviews:
        if keyword in review.lower():
            matched_reviews.append(review)

    return matched_reviews
